import os
import json
import pandas as pd

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.callbacks.manager import get_openai_callback

import logging
from logging.config import dictConfig
import time
import hashlib
import unittest

from . import agent_events
from llmsdk.lib import defaults
from llmsdk.lib.enablers import AgentEnablersMixin
try:
    from llmsdk.services.log import *
    logging.config.dictConfig(log_config)
except:
    logging.basicConfig()

__all__ = ['SADLClassifier']

class SADLClassifier(AgentEnablersMixin):
    """
    Class to take in a dataframe and create a data dictionary for it
    """

    def __init__(self,
                 cred={},
                 platform=defaults.LLM_PLATFORM,
                 model=defaults.LLM_MODEL,
                 entities_filepath=None,
                 max_tokens=1024,
                 temperature=0):
        """
        Class to classify data columns using SADL

        Parameters:
        - entities_filepath (str): The file path to the entities mapping file in JSON format. Default is None.
        - temperature (int): Control the temperature of the inference/API
        - max_tokens (int): Control the max_tokens in the inference/API

        Output:
        Use classify_columns method
        """

        start_time = time.time()

        # init
        self.context = None
        self.agent_name = "sadl"
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.data = None
        self.samplesize = 5
        self.platform = platform
        self.model = model


        # init the base entity map
        self.entity_map = self._get_base_entity_mapping()

        # init the base industry list
        self.industries = self._get_base_industries()

        # load additional entities if needed
        if entities_filepath:
            self.entity_map = self.load_entities(entities_filepath)

        # init the llm and embeddings objects
        self.llm, self.embeddings = self._get_llm_objs(platform=self.platform,
                                                          model=self.model,
                                                          embedding_model=self.embedding_model,
                                                          cred=self.cred)

        self.logger = logging.getLogger("app")

        self.agent_id = self._create_id(f"{self.agent_name}_{start_time}")

        # set metadata
        self.metadata = {
            "agent": {
                "name": self.agent_name,
                "id": self.agent_id,
                "platform": self.platform,
                "model": self.model
            },
            "events": []
        }

        # log that the agent is ready
        duration = time.time() - start_time
        event = self._log_event(agent_events._EVNT_READY, duration)


    def _get_base_industries(self):
        """
        give the base industries
        """
        industries = ["Business", "Technology",
                           "Finance", "Healthcare",
                           "Manufacturing", "Retail",
                           "Government", "eCommerce",
                           "Education", "Logistics"]

        return industries

    def _get_base_entity_mapping(self):
        """
        give the default base mapping of entities
        """
        mapping = {
            "person": ["id", "name", "gender", "occupation", "nationality", "age", "marital status", "education level", "salutation", "job title", "relationship", "other"],
            "location": ["id", "city", "state", "province", "country", "address", "postal code", "latitude and longitude", "landmark", "neighborhood", "region", "time zone", "other"],
            "organization": ["id", "type", "industry", "other"],
            "event": ["id", "type", "theme", "other"],
            "product": ["id", "category", "brand", "model", "feature", "other"],
            "service": ["id", "category", "cost", "feature", "other"],
            "date/time": ["id", "date", "day", "month", "year", "timestamp", "time zone", "duration", "other"],
            "identifier": ["id"],
            "metric": ["revenue", "size", "volume", "sales", "measurement", "price", "other"],
            "contact": ["website", "email", "phone number", "social link"]
        }
        return mapping


    ## interfaces

    def load_entities(self, entities):
        """
        load any additional entity mappings and add them to the
        base entity map
        entities: path to entity mappings
        """

        # get the base entity map
        entity_map = self.entity_map

        # check path
        if os.path.exists(entities) and entities.endswith(".json"):
            with open(entities, "r") as fd:
                addl_emap = json.load(fd)
            if isinstance(addl_emap, dict):
                for  e, se in addl_emap.items():
                    # lowercase everything
                    e = e.lower()
                    # we need lists
                    if isinstance(se, str):
                        se = [se.lower()]
                    # lowercase everything
                    if isinstance(se, list):
                        se = [i.lower() for i in se]
                    else:
                        # we cannot add this item, move on
                        continue
                    # we can now add this mapping to the base map
                    entity_map[e].extend(se)
                    # make sure we remove duplicates
                    entity_map[e] = list(set(entity_map[e]))
            # done, we have the updated map
            self.entity_map = entity_map
        else:
            pass

        return self.entity_map

    def generate_prompt_params(self, context=""):
        def construct_promptpartial_from_map(entity_map):
            """
            Take an entity map and construct the entity mapping partial
            that goes into the prompt for the LLM
            """
            # first the entities
            entities = ", ".join(list(entity_map.keys()))
            partial_e = f"Assume the entities available for classification are as follows: \n{entities}"

            # then for the sub-entities
            partial_se = ""
            for e, se in entity_map.items():
                p_se = f"Assume the following are the sub entities for {e}: \n{', '.join(se)}"
                partial_se = f"{partial_se}\n\n{p_se}"

            partial = f"{partial_e}{partial_se}"

            return partial

        def construct_promptpartial_outputformat():
            """
            Construct the output format structure
            for the response from the LLM
            """
            column_label = "column_name"
            label_fields = ['datatype', 'entity', 'sub_entity', 'pii', 'description']

            p = ", ".join([f'"{f}": {f}' for f in label_fields])
            op_format = "{" + column_label + ": {" + p + "}}"

            return op_format


        # construct the prompt partial for the entity mappings
        map_partial = construct_promptpartial_from_map(self.entity_map)

        # get the input column name labels
        labels = ", ".join(list(self.df.columns))

        # output format
        output_format = construct_promptpartial_outputformat()

        resp = {"context": context,
             "map_partial": map_partial,
             "labels": labels,
             "output_format": output_format
            }

        return resp

    def generate_prompt_columns_string(self):
        """
        generate prompt in string format
        """
        prompt = self.generate_prompt_columns()
        params = self.generate_prompt_params()
        prompt_string = prompt.invoke(params)
        return prompt_string

    def generate_prompt_columns(self):
        """
        generate a prompt for labelling a dataframe given some context
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a data entry operator.
                    Your task is to construct a data dictionary for a set of database column names given to you.
                    The database is from a company in {context} industry.""",
                ),
                ("human",

            """{map_partial}

            Classify the following column names into entity and sub_entity using the above mentioned details.
            Also provide the following for each column:
            - datatype
            - true/false indicating whether the column could contain personally identifiable information (PII)
            - description

            Format your output as a nested json dictionary as follows:
            {output_format}

            Here are the input column names:
            {labels}"""),
            ]
        )

        return prompt

    def generate_prompt_industry_params(self, df):
        # get the input labels
        labels = ", ".join(list(df.columns))
        params = {
            "labels": labels,
            "industries": self.industries
        }
        return params

    def generate_prompt_industry(self):
        """
        generate a prompt for identifying the industry of a dataframe given some context
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a data entry operator.
                    Assume you have a list of industries:
                    {industries}""",
                ),
                (
                    "human",

                    """Your task is to identify what industry a dataset belongs to given the columns in the dataset.
                    Respond with EXACTLY one option from the list of industries.

                    Here are the columns in the dataset:
                    {labels}"""),
            ]
        )

        return prompt

    def load_data(self, content, source="df"):
        """
        - source (str): The type of input data. Can be "df" for a DataFrame input or "csv" for a CSV file input. Default is "df".
        - content: data file path (if source=='str') or DataFrame (if source=='df').
        """
        if source == "csv":
            data = pd.read_csv(content,
                                    on_bad_lines='skip',
                                    encoding='unicode_escape')
        elif source == "df" and not content.empty:
            data = content
        else:
            return False

        self.data = {}
        for col in data.columns:
            self.data[col] = list(data[col].astype(str).head(self.samplesize).values)

        return self.data

    def classify_columns(self, context=""):
        """
        Classify the columns.

        Parameters:
        - context (str, optional): The context for classification. If not provided, the default context of the class instance is used.

        Returns:
        - success (bool): Indicates whether the classification was successful.
        - result_type (str): The type of the classification result. Can be 'json' for JSON format or 'str' for string format.
        - result (str or dict): The classification result. If 'result_type' is 'json', it's a dictionary; otherwise, it's a string.
        """

        # set start_time
        start_time = time.time()

        # set the context for this labelling attempt
        context = self.context if context=="" else context

        # get the prompt for the LLM
        prompt = self.generate_prompt_columns()

        params = self.generate_prompt_params(context)

        chain = prompt | self.llm

        try:
            # chain and prompt
            success = True
            resp = chain.invoke(params)
            response = resp.content

            try:
                result = json.loads(response.lower().strip())
                result_type = 'json'
            except:
                result = response.strip()
                result_type = 'str'
        except:
            success = False
            result = ""
            result_type = ""

        # get prompt
        prompt_string = self.generate_prompt_columns_string()

        params = {
            "query": str(prompt_string),
            "mode": self.data_mode,
            "success": success,
            "result_type": result_type,
            "result": result
        }

        # logging the result
        duration = time.time() - start_time

        event = self._log_event(agent_events._EVNT_QUERY, duration, params=params)

        # process the response
        return success, result_type, result

    def classify_industry(self):
        """
        figure out what industry the dataframe is from
        """

        # get the prompt for the LLM
        prompt = self.generate_prompt_industry()

        params = self.generate_prompt_industry_params(self.df)

        chain = prompt | self.llm

        # chain
        resp = chain.invoke(params)
        response = resp.content

        result = response.lower().strip()

        # process the response
        return result

    def map_to_targets(self, data, targets, use_content=False):
        """
        map input column names to a defined set of target classes
        - data: input data to map, must come from the self.load_data(...) method
        - targets: list of target classes
        - use_content: if True, send a sample of data content values to LLM to do the mapping
            set this to True using caution, or data leakage is possible
        """

        def construct_prompt(data, targets, use_content):
            if use_content == False:
                task_subprompt = """You will be given a list of input columns as well as a list of target classes.
                Your task is to map each column in the input dataframe to one entry in the list of target classes.
                """
            if use_content == True:
                task_subprompt = """You will be given a column name, some sample values from that column, as well as a list of target classes.
                Your task is to map the column name to one entry in the list of target classes. Use the sample values to guide your decision.
                """


            # construct the prompt template
            # this is the system message part
            sys_msg = f"""You are a highly advanced, AI-enabled, data mapping tool.
            {task_subprompt}
            Format your output as a json dictionary as follows:
            {{"input": "target"}}
            """

            # this is the human message part
            if use_content == False:
                human_subprompt = f"""Here are the input columns names
                ------ BEGIN COLUMN NAMES ------
                {data}
                ------- END COLUMN NAMES -------
                """
            if use_content == True:
                human_subprompt = f"""Here is the column name and values
                ------ BEGIN COLUMN AND VALUES ------
                {data}
                ------- END COLUMN AND VALUES -------
                """

            human_msg = f"""{human_subprompt}

            Here are the target classes:
            ------ BEGIN TARGET CLASSES ------
            {targets}
            ------- END TARGET CLASSES -------"""

            prompt = [
                SystemMessage(content=sys_msg),
                HumanMessage(content=human_msg),
            ]

            return prompt

        def execute_prompt(prompt):
            try:
                if self.platform in ['openai', 'azure']:
                    with get_openai_callback() as cb:
                        response = self.llm(prompt)
                        response = response.content
                    stats = {
                        "total_tokens": cb.total_tokens,
                        "prompt_tokens": cb.prompt_tokens,
                        "completion_tokens": cb.completion_tokens,
                        "total_cost": round(cb.total_cost, 4)
                    }
                success = True
            except:
                success = False

            result = {
                "success": success,
                "response": response
            }

            return result

        # run the query
        result = {
            "success": False,
            "columns": {}
        }
        if use_content == True:
            for column, values in data.items():
                column_str = f"{column}: {', '.join(values)}"
                prompt = construct_prompt(column_str, targets, use_content)
                res = execute_prompt(prompt)
                if res.get("success"):
                    result["success"] = True
                    d = json.loads(res.get("response"))
                    key = list(d.keys())[0]
                    result['columns'][column] = d.get(key)
        else:
            columns = list(data.keys())
            prompt = construct_prompt(columns, targets, use_content)
            result = execute_prompt(prompt)
            result["success"] = True
            result['columns'] = json.loads(result.get("response"))
            d = result.pop("response")

        return result



class TestSADLClassifier(unittest.TestCase):
    def test_classification_1(self):
        data_mode = "csv"
        data_filepath = "data/Acme-Plan-Data.csv"
        entities_mode = "json"
        emap_file = "emap.json"

        labeller = SADLClassifier(data_mode=data_mode,
                                   data_filepath=data_filepath,
                                   context="",
                                   entities_filepath=emap_file)

        industry = labeller.classify_industry()
        success, result_type, result = labeller.classify_columns(context=industry)

        print("result_type: ", result_type)
        print("type: ", type(result))
        print("###################")
        self.assertTrue(success)
        self.assertIsInstance(result_type, str)
        if result_type == 'str':
            self.assertIsInstance(result, str)
        else:
            self.assertIsInstance(result, dict)

    def test_classification_2(self):
        data_mode = "df"
        data_filepath = "data/Acme-Plan-Data.csv"
        data = pd.read_csv(data_filepath)
        entities_mode = "json"
        emap_file = "emap.json"

        labeller = SADLClassifier(data_mode=data_mode,
                                   data=data,
                                   context="",
                                   entities_filepath=emap_file)

        industry = labeller.classify_industry()
        success, result_type, result = labeller.classify_columns(context=industry)

        print("result_type: ", result_type)
        print("type: ", type(result))
        print("###################")
        self.assertTrue(success)
        self.assertIsInstance(result_type, str)
        if result_type == 'str':
            self.assertIsInstance(result, str)  # Adjust this based on your expected result type
        else:
            self.assertIsInstance(result, dict)

if __name__ == '__main__':
    # # unit tests
    # unittest.main()

    # testbed
    csv = '...'
    targets = [
        "identifier",
        "label",
        "code",
        "gender",
        "datetime",
        "amount",
        "location",
        "category"
    ]
    labeller = SADLClassifier(platform="openai")
    data = labeller.load_data(csv, source="csv")
    mapping = labeller.map_to_targets(data, targets, use_content=True)
    print (json.dumps(mapping, indent=4))
