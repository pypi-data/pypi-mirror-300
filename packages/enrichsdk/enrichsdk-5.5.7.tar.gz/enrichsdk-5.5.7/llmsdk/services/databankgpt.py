import os
import sys
import json
from fastapi.concurrency import run_in_threadpool

from .basegpt import BaseGPT
from .lib import *
from ..agents import LLMDatabankQuerier

logger = get_logger()

class DatabankQueryGPT(BaseGPT):

    def __init__(self):
        super().__init__()
        self.name = "DatabankQueryGPT"
        self.agentname = os.environ.get('AGENTNAME', 'databankindex')
        self.platform = "azure" if 'AZURE_OPENAI_ENDPOINT' in os.environ else "openai"

        self.model = os.environ.get("MODELNAME", 'gpt-4o-mini')
        self.namespace = self.agentname
        self.index_name = "databank_gpt_index"
        self.router.add_api_route("/load", self.load_data, methods=["POST"])

        self.persist_directory = os.path.join(self.run_dir,
                                              self.agentname,
                                              "index")
        
        stats = get_stats()
        stats.update({
            "model": self.model,
            "platform": self.platform, 
            "agentname": self.agentname,
        })
        
    async def get_llm_agent(self):
        agent = LLMDatabankQuerier(name=self.agentname,
                                   model=self.model,
                                   platform=self.platform)

        logger.debug(f"Built agent for {self.agentname} w/ model {self.model} and platform {self.platform}")

        return {
            "agent": agent
        }

    async def qna_run(self, request_id):
        """
        Execute query against the agend
        :param request_id: Request ID of the request
        :return:
        """
        cache = get_cache()

        if request_id not in cache:
            logger.error(f"Failure",
                         extra={
                             'request_id': "invalid",
                             "source": "service",
                         })
            cache[request_id] = {
                'status': "failure",
                "message": f"Invalid request id"
            }
            return

        # First get the params
        value = cache[request_id]

        try:

            params  = value['params']
            user    = params['user']
            dataset = params['dataset']
            query   = params['query']
            extra   = params['extra']

            stats['query_count'] += 1

            label = f"{user}_{dataset}"

            stats['datasets'][label] = {
                'loaded': datetime.now().replace(microsecond=0).isoformat(),
                'username': user,
                'agent_created': True,
                'agent_status': "Created",
                "query_count": 0,
                "query_success": 0,
                "query_failure": 0,
            }
            
            # First get the agent...
            logger.debug(f"Running Query",
                         extra={
                             "source": "service",
                             "user": user,
                             "dataset": dataset,
                             "request_id": request_id,
                             'data': json.dumps(value, indent=4, cls=SafeEncoder)
                         })

            index_name = self.index_name
            index_path = os.path.join(self.persist_directory, "index")
            if ((self.agent.index is None) and (os.path.exists(index_path))):
                self.agent.load_index(store="chroma",
                                      persist_directory=self.persist_directory,
                                      index_name=index_name)
                logger.debug(f"Loaded index",
                             extra={
                                 "data": json.dumps({
                                     'source': 'service',
                                     'user': 'all',
                                     'dataset': dataset,
                                     'stats': self.agent.get_index_stats()
                                 }, indent=4, cls=SafeEncoder)
                             })            

            result = await run_in_threadpool(lambda: self.agent.query(query,
                                                                      filters=extra.get('filters',{}),
                                                                      topk=extra.get('topk', 3)))

            if result.get("success"):
                key = result.get("key")
                logger.debug(f"Query: {query}\nKEY: {key}\n")
                json_result = json.loads(json.dumps(result, indent=4, cls=SafeEncoder))

                stats['query_success'] += 1
                stats['datasets'][label]['query_count'] += 1
                stats['datasets'][label]['query_success'] += 1
                query_update_result(request_id, {
                    "status": "success",
                    "result": json_result,
                })
            else:
                suggestions = result.get("suggestions")
                logger.debug(f"Query: {query}\nSuggestions: {suggestions}\n")
                json_result = json.loads(json.dumps(result, indent=4, cls=SafeEncoder))
                stats['datasets'][label]['query_count'] += 1
                stats['datasets'][label]['query_failure'] += 1
                query_update_result(request_id, {
                    "status": "success",
                    "result": json_result,
                })

        except Exception as e:
            stats['query_failure'] += 1
            stats['datasets'][label]['query_count'] += 1
            stats['datasets'][label]['query_failure'] += 1
            logger.exception(f"Failed to run query",
                             extra={
                                 "source": "service",
                                 'request_id': request_id,
                                 "user": params.get('user', "unknown"),
                                 "dataset": params.get('dataset', "unknown"),
                             })
            query_update_result(request_id, {
                "status": "failure",
                "answer": f"Unable to construct the answer. Could be an internal agent error. See the agent log",
                "result": {
                    "text": str(e)
                }
            })

    async def load_data(self,
                        data: list[dict]= [],
                        params: dict = {}):
        """
        Load JSON-like structure

        :param data: List of dictionaries
        :param params: Indexing params
        """
        logger.debug(f"Loading data records {len(data)} {params}")

        try:
            loadfunc = lambda: self.agent.load_data(content=data,
                                                    source='json',
                                                params=params)
            data = await run_in_threadpool(loadfunc)
        except Exception as e:
            logger.exception("Failed to turn dicts into docs")
            raise HTTPException(
                status_code=500,
                detail=f'Failed to load data: {e}'
            )

        try:
            print("Loading index", self.index_name, self.persist_directory)
            ## index the data
            # create the index and add data to it
            # this call will flush an existing index if it already exists
            # can be called multiple times
            indexfunc = lambda: self.agent.create_add_index(data=data,
                                                            store="chroma",
                                                            persist_directory=self.persist_directory,
                                                            index_name=self.index_name)
            data = await run_in_threadpool(indexfunc)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Failed to index loaded data: {e}'
            )            

        return {
            "status": "success"
        }
    
app = FastAPI()

##############################################
# Common
##############################################
add_show_cache(app)
add_show_health(app)
databankGpt = DatabankQueryGPT()
app.include_router(databankGpt.router)

# For IDE Debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10892)
