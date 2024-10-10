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
from llmsdk.lib.enablers import AgentEnablersMixin
from llmsdk.lib import SafeEncoder
from llmsdk.services.log import *

__all__ = ['LLMPromptAgent']

class LLMPromptAgent(AgentEnablersMixin):
    """
    A geenric agent to run a prompt
    """

    def __init__(self,
                 name,
                 cred={},
                 platform=defaults.LLM_PLATFORM,
                 model=defaults.LLM_MODEL,
                 embedding_model=defaults.LLM_EMBEDDING_MODEL):
        """
        init the bot
        name: name of the bot
        cred: credentials object
        platform: name of the platform backend to use
                default to openai platform for now
                will be extended in the future to suuport other platforms
        model: model name
        """

        start_time = time.time()

        # logging
        self.logger = get_logger()

        # defaults
        self.metadata       = {}
        self.max_llm_tokens = 4000

        # name
        self.agent_name = name
        self.agent_type = "prompter"
        self.agent_id   = self._create_id(f"{self.agent_name}_{start_time}")

        # creds
        self.cred = cred
        # LLM params
        self.platform           = platform
        self.model              = model
        self.embedding_model    = embedding_model

        # init the llm and embeddings objects
        self.llm, self.embeddings = self._get_llm_objs(platform=self.platform,
                                                          model=self.model,
                                                          embedding_model=self.embedding_model,
                                                          cred=self.cred)

        # agent defaults
        self.persona_prompt = "You are a highly advanced AI agent capable of solving tasks that you are presented with."

        self.errs = {
            "human_msg": "No prompt available, cannot call LLM",
        }

        # note metadata for this agent
        self.metadata = {
            "agent": {
                "name": self.agent_name,
                "name": self.agent_type,
                "platform": self.platform,
                "model": self.model,
                "embedding_model": self.embedding_model,
            },
            "events": []
        }
        # log that the agent is ready
        duration = time.time() - start_time
        event = self._log_event(agent_events._EVNT_READY, duration)

    ## interfaces

    def run_prompt(self, sys_msg, human_msg):
        """
        generate a prompt for querying the LLM
        """
        # construct the prompt template
        messages = [
            SystemMessage(content=sys_msg),
            HumanMessage(content=human_msg),
        ]

        # call the LLM
        response = self.llm.invoke(messages)

        return response

    def prompt(self, prompt):
        """
        run a query using llm to answer questions about some text data
        this is useful when looking for answers about some context but without doing RAG
        """
        # construct the prompt
        sys_msg = prompt.get("persona", self.persona_prompt)
        human_msg = prompt.get("prompt")

        if human_msg == None:
            result = { "answer": self.errs["human_msg"] }

        else:
            # run prompt
            response = self.run_prompt(sys_msg, human_msg)
            result = { "answer": response.content }

        return result
