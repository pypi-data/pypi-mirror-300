import json
import time
import string
from re import sub

from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks.manager import get_openai_callback

from . import agent_events
from llmsdk.lib import defaults
from llmsdk.lib.enablers import AgentEnablersMixin
from llmsdk.agents.basellmrag import BaseLLMRAGAgent
from llmsdk.lib import SafeEncoder

__all__ = ['LLMDatabankQuerier']
DEFAULT_TOPK = 10

class LLMDatabankQuerier(BaseLLMRAGAgent, AgentEnablersMixin):
    """
    Class to load and index a docset and support running queries against the docset
    for retrieval of most similar matches
    """

    def __init__(self,
                 name,
                 cred={},
                 platform=defaults.LLM_PLATFORM,
                 model=defaults.LLM_MODEL,
                 embedding_model=defaults.LLM_EMBEDDING_MODEL,
                 statestore=defaults.LLM_STATE_STORE):
        """
        init the LLM query agent
        name: name of the agent
        cred: credentials object
        platform: name of the LLM platform backend to use
                default to OpenAI GPT platform for now, Azure is also supported
                will be extended in the future to suuport other models
        memory_size: how many tokens of memory to use when chatting with the LLM
        """

        start_time = time.time()

        # init the base class
        super().__init__(name=name,
                         cred=cred,
                         platform=platform,
                         model=model,
                         embedding_model=embedding_model,
                         agent_type="databank-query",
                         statestore=statestore)

        # defaults
        self.chunk_size = 1000
        self.chunk_overlap = 300
        self.index = None
        self.metadata = {}
        self.vdb_client = None
        self.index_name = None
        self.index_store = None
        self.docs = {}

        # LLM params
        self.platform = platform
        self.model = model
        self.embedding_model = embedding_model

        # init the llm and embeddings objects
        self.llm, self.embeddings = self._get_llm_objs(platform=self.platform,
                                                        model=self.model,
                                                        embedding_model=self.embedding_model,
                                                        cred=self.cred)

        # note metadata for this agent
        self.metadata = {
            "agent": {
                "name": self.agent_name,
                "type": self.agent_type,
                "platform": self.platform,
                "model": self.model,
                "embedding_model": self.embedding_model,
            },
            "events": []
        }
        # log that the agent is ready
        duration = time.time() - start_time
        event = self._log_event(agent_events._EVNT_READY, duration)

    ## helper functions

    def run_query(self, query, filters, topk):
        """
        run a query against an internal docset indexed by the agent
        """

        # get the similar docs
        docs = self.get_similar_docs(query, filters=filters, topk=topk)

        ##
        ## -- TO-DO --
        ## can add more complex processing of returned docs here
        ## e.g. re-ranking, summarization by LLM, etc.
        ## -- END TO-DO --
        ##

        # construct the result
        result = {
            "question": query,
            "sources": [{
                "content": d.page_content,
                "metadata": d.metadata,
                "distance": d.metadata.pop('distance')
            } for d in docs],
        }

        return result

    def query(self, query, filters=None, topk=DEFAULT_TOPK):
        """
        run a query on an index
        query: query string
        topk: number of closest matching docs to return
        """

        start_time = time.time()

        try:
            if self.platform in ['openai', 'azure']:
                with get_openai_callback() as cb:
                    result = self.run_query(query, filters=filters, topk=topk)
                stats = {
                    "total_tokens": cb.total_tokens,
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost": round(cb.total_cost, 4)
                }
            else:
                result = self.run_query(query, filters=filters, topk=topk)
                stats = {}
        except:
            result = {
                "question": query,
                "sources": [],
            }
            stats = {}

        # log the event
        params = {
            "query": query,
            "topk": topk,
            "result": result.copy() if result is not None else None,
            "stats": stats,
        }
        duration = time.time() - start_time
        event = self._log_event(agent_events._EVNT_QUERY, duration, params=params)

        # add the event to the result
        result['metadata'] = {
            "timestamp": event['timestamp'],
            "duration": event['duration'],
        }

        return result


################### BEGIN TESTBED ###################

if __name__ == "__main__":

    # vars
    # cred = get_credentials_by_name('openai-api')
    persist_directory = "chromadb"
    path        = '...'

    agentname   = "broker-querier"
    platform    = "openai"
    model       = "gpt-4o-mini"
    mode        = "load"

    ## create an agent
    # agent to do databank querying
    agent = LLMDatabankQuerier(name=agentname, platform=platform, model=model)

    if mode == "create":
        ## load the data
        # set the params
        # 'index_columns' specifies names of columns in dataset that will be vector indexed
        params = {
            "index_columns": ["name", "summary"]
        }
        # specify source='csv' for CSV datasets
        data = agent.load_data(content=path,
                                source='csv',
                                params=params)

        ## index the data
        # create the index and add data to it
        # this call will flush an existing index if it already exists
        # can be called multiple times
        agent.create_add_index(data=data,
                               store="chroma",
                               persist_directory=persist_directory,
                               index_name=agentname)
    else:
        agent.load_index(persist_directory=persist_directory,
                            index_name=agentname,
                            store='chroma')

    ## run the query
    query = "platform used by MetLife for group insurance operations"
    # set the filters if needed
    # '_fieldtype' is a list containing the fields on which search should be executed
    #       if empty, then search is done across all indexed fields in the databnk
    filters = {
        "_fieldtype": ["name", "summary"]
    }
    # 'topk' specifies the number of results to return from the databank
    result = agent.query(query,
                         filters=filters,
                         topk=3)

    ## display
    print(json.dumps(result, indent=2, cls=SafeEncoder))
