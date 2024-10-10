import pytest
from llmsdk.agents.prompter import LLMPromptAgent

# test cases with expected outputs
test_cases = [
    (
        "What is the first month of the year? Respond with only the month name in all caps.",
        "JANUARY"
    ),
    (
        "What day comes after Sunday? Respond with only the day name in lowercase.",
        "monday"
    ),
    (
        "Is an orange a fruit or a mammal? Respond with only the word fruit or animal in lowercase but with the first letter capitalized.",
        "Fruit"
    ),
]

class TestAgentPrompter:
    """
    Class containing test cases for the Prompter LLM Agent
    """

    # test methods
    @pytest.mark.parametrize("query,truth", test_cases)
    def test_agent_prompter(self, init_llm, query, truth):
        """
        method to create a Prompter Agent, send it a test prompt, and check the response
        """
        # test vars
        self.agentname          = init_llm["agentname"]
        self.platform           = init_llm["platform"]
        self.model              = init_llm["model"]
        self.embedding_model    = init_llm["embedding_model"]

        # create the agent
        agent = LLMPromptAgent(name=self.agentname,
                                 platform=self.platform,
                                 model=self.model,
                                 embedding_model=self.embedding_model)

        # setup the test prompt and expected response
        prompt = {
            "prompt": query
        }
        expected_response = truth

        # run the prompt and get the response
        response = agent.prompt(prompt)
        response = response.get('answer', "")

        # response should be JANUARY to pass
        assert response == expected_response
