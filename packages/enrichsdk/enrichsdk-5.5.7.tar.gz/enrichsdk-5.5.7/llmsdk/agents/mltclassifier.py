import os
import json
import time
import string
import hashlib

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.callbacks.manager import get_openai_callback

from . import agent_events
from llmsdk.lib import defaults
from llmsdk.lib import SafeEncoder
from llmsdk.lib.enablers import AgentEnablersMixin
from llmsdk.services.log import *

__all__ = ['LLMMultiLabelTextClassifier']

class LLMMultiLabelTextClassifier(AgentEnablersMixin):
    """
    A bot to take in some text and perform multi-label classification on it
    """

    def __init__(self,
                 name,
                 cred={},
                 platform=defaults.LLM_PLATFORM,
                 model=defaults.LLM_MODEL):
        """
        init the bot
        name: name of the bot
        cred: credentials object
        platform: name of the platform backend to use
                default to openai platform for now
                will be extended in the future to suuport other platforms
        """

        start_time = time.time()

        # logging
        self.logger = get_logger()

        # defaults
        self.metadata = {}
        self.sanity_entries = {}
        self.max_llm_tokens = 512

        # name
        self.agent_name = name
        self.agent_type = "query-router"

        # creds
        self.cred = cred
        # LLM params
        self.platform = platform
        self.model = model

        # init the llm and embeddings objects
        self.llm, self.embeddings = self._get_llm_objs(platform=self.platform,
                                                          model=self.model,
                                                          cred=self.cred)

        # note metadata for this agent
        self.metadata = {
            "agent": {
                "name": self.agent_name,
                "platform": self.platform,
                "model": self.model,
            },
            "events": []
        }
        # log that the agent is ready
        duration = time.time() - start_time
        event = self._log_event(agent_events._EVNT_READY, duration)

    ## interfaces

    def get_prompt(self, query, label_spec):
        """
        generate a prompt for querying the LLM
        """
        # construct the prompt template

        defualt_persona = """You are a highly advanced, AI-enabled bot, that performs multi-label text classification"""

        # get the bot's persona
        persona = label_spec.get("persona", defualt_persona)

        # get the bot's specified instruction set
        instructions = label_spec.get("instructions", "")

        # get the synonymns
        syns = []
        for term, synonymns in label_spec.get('synonymns', {}).items():
            syn = f"  - {term}: {', '.join(synonymns)}"
            syns.append(syn)
        synonymns = "\n".join(syns)
        if len(synonymns) > 0:
            synonymns = f"""Here is a set of comma-separated synonymns for various phrases that may be asked about:
{synonymns}"""

        # get the output format
        output_format = label_spec.get('output_format', {})
        output_type = output_format.get('type', 'json')
        output_sample = output_format.get('sample', None)

        if output_sample:
            output_format = f"""Always respond by formatting your response as a {output_type} object EXACTLY as follows:
{output_sample}"""
        else:
            output_format = f"""Always respond by formatting your response as a {output_type} object"""

        # construct the system message
        sys_msg = "\n\n".join([persona, instructions, synonymns, output_format])

        # construct the human message
        human_msg = f"""
Here is the question:
------ BEGIN QUESTION ------
{query}
------- END QUESTION -------

Your response:
"""

        messages = [
            SystemMessage(content=sys_msg),
            HumanMessage(content=human_msg),
        ]

        return messages

    def label(self, query, label_spec={}):
        """
        run a prompt against the LLM using the routing spec
        """
        start_time = time.time()

        success = True
        response = None

        # construct the prompt to the policy bot
        prompt = self.get_prompt(query, label_spec)

        # run the query
        try:
            if self.platform in ['openai', 'azure']:
                with get_openai_callback() as cb:
                    response = self.llm(prompt)
                stats = {
                    "total_tokens": cb.total_tokens,
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost": round(cb.total_cost, 4)
                }
            else:
                response = self.llm(prompt)
                stats = {}

            response = json.loads(response.content)

        except:
            success = False

        # log the event
        params = {
            "query": query,
            "mode": "internal",
            "result": response.copy() if response is not None else None,
            "stats": stats,
        }
        duration = time.time() - start_time
        event = self._log_event(agent_events._EVNT_QUERY, duration, params=params)

        return success, response


################### BEGIN TESTBED ###################

def get_sample_profilespec():

    default = {

        "persona": """You are a highly advanced, AI-enabled bot whose job is to take a question from a user and assign two labels to it.
The first label is what kind of insight is being asked about.
The second label is what kind of cohort is being asked about.""",

        "instructions": """The questions will be about the results of a survey across multiple respondent cohorts for multiple products.
Note that sometimes a question can be about all the products in the survey without asking about population cohorts, and sometimes cohort information will be asked.
The three types of population cohorts are: region, gender, age

The following are metrics that could be mentioned in the question:
  - 'reach' a.k.a. 'line insights' a.k.a. 'le'
  - 'voc' a.k.a. 'sentiment score' a.k.a. 'ss'

Here are the rules by which you must perform the insight label assignment:
  - If the question is asking about actionable insights, then assign insight=actionable_insights
  - If the question is asking specifically about best performing or worst performing products, then assign insight=actionable_insights
  - If the question is asking about product metrics with a specific cohort, then assign insight=le_insights
  - If the question is asking about the affinity of a population cohort to products, then assign insight=ss_insights
  - If the question is asking about product features, then assign insight=features_insights
  - If the question is asking about the audience, then assign insight=audience_insights

And here are the rules by which you must perform the cohort label assignment:
  - If the question is asking about groups of respondents, then assign cohort=audience
  - If the question is asking about locations, then assign cohort=region
  - If the question is asking about gender, then assign cohort=gender
  - If the question is asking about age, then assign cohort=age
  - If the question is asking about best, or winners, or hits then assign cohort=best
  - If the question is asking about worst or losers then assign cohort=worst
  - If the question is asking about not liking something, then assign cohort=dislikes
  - If the question is asking about one metric being high and another being low, then assign cohort=mixed""",

        "synonymns": {
            "actionable insights": [
                "survey summary",
                "global summary",
                "overall performance"
            ],
            "line efficiency": [
                "le",
                "reach",
                "cannibalization",
                "incremental reach",
                "cumulative reach",
            ],
            "sentiment score": [
                "ss",
                "voc",
                "voice of consumer",
                "sentiment graph",
                "consumer graph",
                "consumer appetite",
                "consumer sentiment",
            ],
        },

        "output_format": {
            "type": "json",
            "sample": '{"insight": insight, "cohort": cohort}'
        }
    }

    return default


if __name__ == "__main__":

    def query_to_text(agent, query, label_spec, commentary):
        """
        Take a query and a label_spec and use the MLTClassifier agent to get a set of labels
        then use the labels to construct a key
        use the key to lookup the data in the commentary dict
        """
        # default
        err = "Error"
        text = err

        # first, get the route
        success, result = agent.label(query, label_spec)

        if success:
            # construct the key
            keyparts = []
            keyparts.append(result.get('insight', ''))
            keyparts.append(result.get('cohort', ''))
            keyparts = [k for k in keyparts if k!='']
            key = "_".join(keyparts)

            # lookup
            text = commentary.get(key, {}).get('text', err)

        return text

    # vars
    commentaryfile = "..." # /path/to/{survey}-output.json
    agentname = "surveybot"
    platform = "openai"
    labelspec = get_sample_profilespec()

    # load the commentary data
    with open(commentaryfile, "r") as fd:
        commentary_json = json.load(fd)
    commentary = commentary_json.get('commentary', {})

    # create an agent
    surveybot = LLMMultiLabelTextClassifier(name=agentname, platform=platform)

    # query the agent
    query = "How are these products reaching with women?"
    text = query_to_text(surveybot, query, labelspec, commentary)
    print (f"Question: {query}")
    print (f"Answer: {text}")
