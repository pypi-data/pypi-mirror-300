import os
import json
import time
import hashlib

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import create_structured_chat_agent
from langchain.agents import AgentExecutor
from langchain_core.tools import Tool

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from llmsdk.lib import SafeEncoder

class AgentEnablersMixin(object):
    """
    Basic enabler methods for any LLM agent

    """

    ## helper functions

    def _create_id(self, string):
        """
        create a unique identifier from a string
        """
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def _log_event(self, event_name, duration=0, params={}):
        """
        format an event object to store in the agent's metadata
        event_name: name of the event to log
        duration: how long did this event take, only needed for events
                   that require some waiting (e.g. RTT to LLM APIs)
        params: any other info needed to be logged
        """

        ts = time.time() - duration # to get the actual start time
        event_id = self._create_id(f'{event_name}-{ts}')

        event = {
            "id": event_id,
            "agent": self.agent_name,
            "agent_type": self.agent_type,
            "agent_id": self.agent_id,
            "timestamp": round(ts, 3),
            "duration": round(duration, 3),
            "name": event_name,
            "params": params,
        }
        self.metadata['events'].append(event)

        # log the event
        self.logger.debug(event_name,
                             extra={
                                 'source': self.agent_name,
                                 'data': json.dumps(event, indent=4)
                             })


        return event

    def _get_llm_objs(self, platform=None, model=None, embedding_model=None, cred=None):

        if platform is None:
            platform = self.platform
        if model is None:
            model = self.model
        if cred is None:
            cred = self.cred

        # get the api key from creds
        api_key = self._get_api_key(cred, platform)

        # init the LLM
        if platform == "openai":

            # get the llm object
            llm = ChatOpenAI(temperature=0,
                             model=model,
                             openai_api_key=api_key,
                             request_timeout=20)

            # get the embeddings object
            if embedding_model:
                embeddings = OpenAIEmbeddingFunction(api_key=api_key,
                                                    model_name=embedding_model)
            else:
                embeddings = None

        elif platform == "azure":

            api_type = 'azure'

            # This will keep evolving and dependent on the deployment
            api_version = os.getenv("AZURE_OPENAI_API_VERSION", default='2024-06-01') # this may change in the future

            # get the llm object
            # based on deployment
            api_key = os.getenv("AZURE_OPENAI_KEY")
            api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
            deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT") # this will correspond to the custom name you chose for your deployment when you deployed a model

            llm = AzureChatOpenAI(azure_endpoint=api_base,
                                  api_version=api_version,
                                  deployment_name=deployment_name,
                                  api_key=api_key,
                                  temperature=0,
                                  request_timeout=20)

            # get the embeddings object
            if embedding_model:
                deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING") # this will correspond to the custom name you chose for your deployment when you deployed a model
                embeddings = OpenAIEmbeddingFunction(api_key=api_key,
                                                        api_base=api_base,
                                                        api_type=api_type,
                                                        api_version=api_version,
                                                        deployment_id=deployment_name,
                                                        model_name=embedding_model)
            else:
                embeddings = None

        else:
            llm = None
            embeddings = None

        return llm, embeddings

    def _load_search_agent(self, cred, searchapi, llm):
        """
        setup the search agent
        this agent will be used to run searches against search engines
        useful to get realtime answers to queries
        """
        # get the serpapi key from creds
        api_key = self._get_api_key(cred, searchapi)

        # setup the search tool
        if searchapi == "serpapi":
            searchengine = SerpAPIWrapper(serpapi_api_key=api_key)
        else:
            searchengine = None
        if searchengine == None:
            return None

        tools = [
            Tool(
                name="Search",
                func=searchengine.run,
                description="Useful for when you need to answer questions about current events. Do not try to click on links. Input must be a search query."
            )
        ]

        # get the langchainhub key from creds
        api_key = self._get_api_key(cred, "langchainhub")

        agent_executor = None
        if api_key:
            # search agent prompt
            prompt_endpoint = "hwchase17/structured-chat-agent"
            prompt = hub.pull(owner_repo_commit=prompt_endpoint,
                                api_key=api_key)

            # create the agent
            agent           = create_structured_chat_agent(llm, tools, prompt)
            agent_executor  = AgentExecutor(agent=agent,
                                            tools=tools,
                                            verbose=False,
                                            handle_parsing_errors=True,
                                            max_iterations=5)

        return agent_executor, searchengine

    def _get_path_source(self, fpath):
        """
        infer the format from the content path name
        """
        if os.path.isdir(fpath):
            return "dir"
        else:
            return fpath.split('.')[-1]

    def _get_api_key(self, cred, key):
        """
        get the API key from the cred
        """
        api_key = None

        env_keys = {
            "openai": "OPENAI_API_KEY",
            "serpapi": "SERPAPI_API_KEY",
            "langchainhub": "LANGCHAIN_API_KEY",
        }

        if isinstance(cred, str):
            api_key = cred
        if isinstance(cred, dict) and key in cred:
            api_key = cred[key]
        if isinstance(cred, dict) and key not in cred:
            if env_keys.get(key):
                api_key = os.getenv(env_keys.get(key))
        return api_key

    def _err_msg(self, t):
        msgs = {
            "field": "I'm having trouble understanding. Try another way of wording your query.",
            "search": "I'm having trouble searching online for the answer. Try another time.",
        }
        return msgs.get(t, "Something went wrong, try your query again.")

    def get_metadata(self):
        """
        return metadata collected by the agent
        """
        return self.metadata
