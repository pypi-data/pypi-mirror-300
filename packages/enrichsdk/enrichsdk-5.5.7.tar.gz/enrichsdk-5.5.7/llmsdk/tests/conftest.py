import pytest
from llmsdk.lib import defaults

# common init vars for LLMs

@pytest.fixture
def init_llm():
    # vars for LLM
    params = {
        "agentname": "test_agent",
        "platform": defaults.LLM_PLATFORM,
        "model": defaults.LLM_MODEL,
        "embedding_model": defaults.LLM_EMBEDDING_MODEL,
    }
    return params
