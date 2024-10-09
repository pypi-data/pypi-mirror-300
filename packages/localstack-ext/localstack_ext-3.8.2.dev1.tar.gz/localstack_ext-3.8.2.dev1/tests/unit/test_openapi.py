import pytest
from localstack import config
from localstack.aws.handlers.validation import OpenAPIRequestValidator


@pytest.fixture(autouse=True)
def enable_validation_flag(monkeypatch):
    monkeypatch.setattr(config, "OPENAPI_VALIDATE_REQUEST", "1")


@pytest.mark.xfail(reason="Community plugin detection fails")
def test_validator_loading_specs():
    validator = OpenAPIRequestValidator()
    # We know we have at least one core community and a pro spec. Therefore, we expect more than one spec to be loaded.
    assert len(validator.open_apis) > 1, "only one openapi spec detected; there should be more"
