import pytest
import unittest

from promptflow.connections import CustomConnection
from llm_structured_json.tools.llm_structured_json import llm_structured_json


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_llm_structured_json(self, my_custom_connection):
        result = llm_structured_json(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()