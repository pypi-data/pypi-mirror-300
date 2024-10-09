import base64
import json

import pytest
from jsonschema import validate
from kafka import KafkaProducer
from localstack import config
from localstack.testing.pytest import markers
from localstack.utils import testutil
from localstack.utils.net import wait_for_port_open
from localstack.utils.strings import short_uid, to_bytes, to_str
from localstack.utils.sync import poll_condition, retry

# In lieu of event snapshotting, we can use JSON schema validation to ensure the returned record is correct.
# A different "required" block is set depending on whether a cluster is of type MSK or self-hosted.
_KAFKA_EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "eventSource": {"type": "string"},
        "bootstrapServers": {"type": "string"},
        "records": {
            "type": "object",
            "patternProperties": {
                "^.+$": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string"},
                            "partition": {"type": "integer"},
                            "offset": {"type": "integer"},
                            "timestamp": {"type": "integer"},
                            "timestampType": {"type": "string"},
                            "key": {"type": "string"},
                            "value": {"type": "string"},
                            "headers": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "patternProperties": {
                                        "^.+$": {"type": "array", "items": {"type": "integer"}}
                                    },
                                },
                            },
                        },
                        "required": [
                            "topic",
                            "partition",
                            "offset",
                            "timestamp",
                            "timestampType",
                            "value",
                        ],
                    },
                }
            },
        },
    },
}


KAFKA_EVENT_SCHEMA_MSK = {
    "required": ["eventSource", "bootstrapServers", "eventSourceArn", "records"],
    **_KAFKA_EVENT_SCHEMA,
}

# Note: a self-managed cluster does not have an EventSourceArn
KAFKA_EVENT_SCHEMA_SELF_MANAGED = {
    "required": ["eventSource", "bootstrapServers", "records"],
    **_KAFKA_EVENT_SCHEMA,
}


TEST_LAMBDA_CODE = """
import json
def handler(event, context):
    print(json.dumps(event))
"""


@markers.aws.only_localstack
@markers.only_on_amd64
@pytest.mark.parametrize(
    "generate_cluster_config,expected_event_source,expected_event_schema",
    [
        pytest.param(
            lambda cluster_arn, broker_host: {
                "SelfManagedKafkaEventSourceConfig": {"ConsumerGroupId": "1"},
                "SelfManagedEventSource": {"Endpoints": {"KAFKA_BOOTSTRAP_SERVERS": [broker_host]}},
            },
            "SelfManagedKafka",
            KAFKA_EVENT_SCHEMA_SELF_MANAGED,
            id="self-hosted",
        ),
        pytest.param(
            lambda cluster_arn, broker_host: {
                "AmazonManagedKafkaEventSourceConfig": {"ConsumerGroupId": "1"},
                "EventSourceArn": cluster_arn,
            },
            "aws:kafka",
            KAFKA_EVENT_SCHEMA_MSK,
            id="msk",
            # The assertions fail against ESM v1 where the returned eventSource of an MSK cluster is "SelfManagedKafka"
            marks=pytest.mark.skipif(
                config.LAMBDA_EVENT_SOURCE_MAPPING == "v1",
                reason="ESM v1 response for an MSK cluster is identical to that of self-hosted.",
            ),
        ),
    ],
)
def test_kafka_lambda_event_source_mapping(
    create_lambda_function,
    aws_client,
    msk_create_cluster_v2,
    create_secret,
    kms_create_key,
    create_event_source_mapping,
    generate_cluster_config,
    expected_event_source,
    expected_event_schema,
    cleanups,
):
    msk_client = aws_client.kafka
    func_name = f"kafka-{short_uid()}"
    cluster_name = f"msk-{short_uid()}"
    secret_name = f"AmazonMSK_{cluster_name}"

    # create Lambda function
    create_lambda_function(func_name=func_name, handler_file=TEST_LAMBDA_CODE)

    # create Kafka stream
    create_cluster_result = msk_create_cluster_v2(
        ClusterName=cluster_name,
        Provisioned={
            "KafkaVersion": "3.3.1",
            "BrokerNodeGroupInfo": {
                "ClientSubnets": [],
                "InstanceType": "kafka.m5.large",
                "BrokerAZDistribution": "DEFAULT",
            },
            "NumberOfBrokerNodes": 2,
        },
    )
    cluster_arn = create_cluster_result.get("ClusterArn")

    # wait until cluster becomes ready ...
    def _cluster_ready():
        state = msk_client.describe_cluster(ClusterArn=cluster_arn)["ClusterInfo"]["State"]
        return "ACTIVE" == state

    assert poll_condition(_cluster_ready, timeout=90), "gave up waiting for cluster to be ready"

    brokers = msk_client.get_bootstrap_brokers(ClusterArn=cluster_arn)
    broker_host = brokers["BootstrapBrokerString"]

    port = int(broker_host.split(":")[-1])
    wait_for_port_open(port, sleep_time=0.8, retries=20)

    # Create event source mapping
    secret_arn = create_secret(
        Name=secret_name, SecretString='{"username":"user","password": "123456"}'
    )["ARN"]

    create_event_source_mapping(
        Topics=["topic"],
        FunctionName=func_name,
        SourceAccessConfigurations=[{"Type": "SASL_SCRAM_512_AUTH", "URI": secret_arn}],
        **generate_cluster_config(cluster_arn, broker_host),
    )

    producer = KafkaProducer(bootstrap_servers=broker_host)
    cleanups.append(producer.close)

    messages = []
    message = {"test": "topic"}
    messages.append(message)
    producer.send(
        topic="topic",
        value=to_bytes(json.dumps(message)),
        headers=[
            ("foo", b"bar"),
            ("foo", b"ed"),
            ("baz", b"fizz"),
        ],
    )
    messages_b64 = [to_str(base64.b64encode(to_bytes(json.dumps(msg)))) for msg in messages]

    # assert that Lambda has been invoked
    def check_invoked():
        logs = testutil.get_lambda_log_events(function_name=func_name, delay_time=15)
        logs = [log for log in logs if any(msg in str(log) for msg in messages_b64)]
        assert len(logs) == 1
        return logs

    events = retry(check_invoked, retries=10, sleep=1)

    # TODO: Unsure of AWS behaviour here since ESM v1 poller starts counting partitions from 0 whereas ESM v2 from 1.
    topic_partition_key = "topic-0" if config.LAMBDA_EVENT_SOURCE_MAPPING == "v2" else "topic-1"

    # assert and validate lambda event format
    for event in events:
        validate(instance=event, schema=expected_event_schema)

    record = events[0]["records"][topic_partition_key][0]
    assert record["topic"] == "topic"
    assert record["timestampType"] == "CREATE_TIME"
    assert record["value"] == "eyJ0ZXN0IjogInRvcGljIn0="  # b64 encoded {"test": f"topic"}
    assert record["headers"] == [
        {"foo": [98, 97, 114]},
        {"foo": [101, 100]},
        {"baz": [102, 105, 122, 122]},
    ]

    # TODO validate against AWS
    assert events[0]["eventSource"] == expected_event_source
    assert events[0]["bootstrapServers"] == broker_host


@markers.aws.only_localstack
@markers.only_on_amd64
@pytest.mark.skipif(
    config.LAMBDA_EVENT_SOURCE_MAPPING != "v2",
    reason="Fails in ESM v1",
)
def test_kafka_lambda_event_source_mapping_multi_topics_and_batches(
    create_lambda_function,
    aws_client,
    msk_create_cluster_v2,
    create_secret,
    kms_create_key,
    create_event_source_mapping,
    cleanups,
):
    msk_client = aws_client.kafka
    func_name = f"kafka-{short_uid()}"
    cluster_name = f"msk-{short_uid()}"
    secret_name = f"AmazonMSK_{cluster_name}"

    # Kafka variables
    total_messages_per_topic = 10
    batch_size = 5
    topics = ["topic-A", "topic-B"]

    # create Lambda function
    create_lambda_function(func_name=func_name, handler_file=TEST_LAMBDA_CODE)

    # create Kafka stream
    create_cluster_result = msk_create_cluster_v2(
        ClusterName=cluster_name,
        Provisioned={
            "KafkaVersion": "3.3.1",
            "BrokerNodeGroupInfo": {
                "ClientSubnets": [],
                "InstanceType": "kafka.m5.large",
                "BrokerAZDistribution": "DEFAULT",
            },
            "NumberOfBrokerNodes": 2,
        },
    )
    cluster_arn = create_cluster_result.get("ClusterArn")

    # wait until cluster becomes ready ...
    def _cluster_ready():
        state = msk_client.describe_cluster(ClusterArn=cluster_arn)["ClusterInfo"]["State"]
        return "ACTIVE" == state

    assert poll_condition(_cluster_ready, timeout=90), "gave up waiting for cluster to be ready"

    brokers = msk_client.get_bootstrap_brokers(ClusterArn=cluster_arn)
    broker_host = brokers["BootstrapBrokerString"]

    port = int(broker_host.split(":")[-1])
    wait_for_port_open(port, sleep_time=0.8, retries=20)

    # Create event source mapping
    secret_arn = create_secret(
        Name=secret_name, SecretString='{"username":"user","password": "123456"}'
    )["ARN"]

    create_event_source_mapping(
        Topics=topics,
        FunctionName=func_name,
        SourceAccessConfigurations=[{"Type": "SASL_SCRAM_512_AUTH", "URI": secret_arn}],
        SelfManagedEventSource={"Endpoints": {"KAFKA_BOOTSTRAP_SERVERS": [broker_host]}},
        SelfManagedKafkaEventSourceConfig={"ConsumerGroupId": "1"},
        BatchSize=batch_size,
    )

    producer = KafkaProducer(bootstrap_servers=broker_host, batch_size=batch_size)
    cleanups.append(producer.close)

    for i in range(total_messages_per_topic):
        for topic in topics:
            message = {"test": "topic"}
            producer.send(
                topic=topic,
                value=to_bytes(json.dumps(message)),
                headers=[
                    ("foo", b"bar"),
                    ("foo", b"ed"),
                    ("baz", b"fizz"),
                ],
            )

    # assert that Lambda has been invoked
    def check_invoked():
        logs = testutil.get_lambda_log_events(function_name=func_name, delay_time=15)
        logs = [log for log in logs if "SelfManagedKafka" in str(log)]
        assert len(logs) == (total_messages_per_topic * len(topics) + batch_size - 1) // batch_size
        return logs

    events = retry(check_invoked, retries=10, sleep=1)

    for event in events:
        validate(instance=event, schema=KAFKA_EVENT_SCHEMA_SELF_MANAGED)
        for _, records in event["records"].items():
            for record in records:
                assert record["topic"] in topics
                assert record["timestampType"] == "CREATE_TIME"
                assert (
                    record["value"] == "eyJ0ZXN0IjogInRvcGljIn0="
                )  # b64 encoded {"test": "topic"}
                assert record["headers"] == [
                    {"foo": [98, 97, 114]},
                    {"foo": [101, 100]},
                    {"baz": [102, 105, 122, 122]},
                ]
