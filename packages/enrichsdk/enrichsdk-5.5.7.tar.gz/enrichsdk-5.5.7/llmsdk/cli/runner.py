#!/usr/bin/env python3
"""

Script to extract tables from pdfs or image files. This will be piped through the textract

"""
import os
import sys
import json
import tempfile
import traceback
import re
import inspect
import importlib
import csv
from collections import defaultdict

import click
import requests

from asgiref.sync import async_to_sync, sync_to_async

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

import llmsdk
from llmsdk.lib import *
from llmsdk.agents import *
from llmsdk.services.lib import get_files, get_agent_details
from llmsdk.services.qna import get_qna_agent, supported_exts as qna_supported_exts
from llmsdk.services.docgen import get_docgen_agent, supported_exts as docgen_supported_exts
from llmsdk.services.datagpt import get_datagpt_agent, supported_exts as datagpt_supported_exts
from llmsdk.services.extractor import get_contract_profilespec, contract_query

from llmsdk.lib.summarizers import *

#####################################
# Helper Functions...
#####################################
def get_chroma_index_summary_generic(indexname, persistdirectory):

    db = Chroma(indexname,
                embedding_function=OpenAIEmbeddings(),
                persist_directory=persistdirectory)

    content = db.get()

    summary = {
        'count': 0,
        'chunks': defaultdict(int)
    }
    metadatas = content['metadatas']
    for entry in metadatas:
        summary['count'] += 1
        if 'sample' not in summary:
            summary['sample' ] = entry
        #chunk = entry['chunk']
        #summary['chunks'][chunk] += 1

    return summary

def get_chroma_index_summary_files(indexname, persistdirectory):

    db = Chroma(indexname,
                embedding_function=OpenAIEmbeddings(),
                persist_directory=persistdirectory)

    content = db.get()

    sample = {
        "source": "/home/pingali/Data/enrich/llm-agents/data/docs/qna-batch-brookfield/October Three RFP/converted/Ste Michelle Bid Specifications 06.21.2023.pdf",
        "file_path": "/home/pingali/Data/enrich/llm-agents/data/docs/qna-batch-brookfield/October Three RFP/converted/Ste Michelle Bid Specifications 06.21.2023.pdf",
        "page": 0,
        "total_pages": 7,
        "format": "PDF 1.5",
        "title": "",
        "author": "Emmy Brown",
        "subject": "",
        "keywords": "",
        "creator": "Writer",
        "producer": "LibreOffice 6.4",
        "creationDate": "D:20230719202934+05'30'",
        "modDate": "",
        "trapped": "",
        "bboxes": "[[264.3999938964844, ...,489.29425048828125]]",
        "file": "Ste Michelle Bid Specifications 06.21.2023.pdf",
        "chunk": 1,
        "id": "922e098a97dd5fcea7343d052317ee71"
        }

    summary = {}
    metadatas = content['metadatas']
    for entry in metadatas:
        filename = entry['file']
        page     = entry['page']
        chunk    = entry['chunk']
        format_  = entry['format']
        if filename not in summary:
            summary[filename] = {
                'pages': [],
                'chunks': [],
                'format': "unknown"
            }
        if page not in summary[filename]['pages']:
            summary[filename]['pages'].append(page)
        summary[filename]['chunks'].append(chunk)
        summary[filename]['format'] = format_

    return summary

@click.group()
def process():
    """
    Run the agent in batch mode with documents
    """

def show_help():
    helptext = """This script needs to run with

export DATA_ROOT="/home/pingali/Data/enrich/llm-agents/data/docs"
export AGENTNAME=default
    """
    print(helptext)


#####################################
# QnA Simple - single command
#####################################
@process.command("qna-simple")
@click.argument("dataset")
@click.argument("question")
def qna(dataset, question):
    """
    Ask a question against a qna agent
    """

    if 'DATA_ROOT' not in os.environ:
        show_help()
        return

    details = async_to_sync(get_agent_details)(namespace="qna",
                                               username="cli",
                                               subdir=dataset,
                                               exts=qna_supported_exts,
                                               get_task_specific_agent=get_qna_agent)

    result = details['agent'].query(question, mode="internal")
    print(json.dumps(result, indent=4))

#####################################
# qna-batch execution
#####################################
def get_path_source(fpath):
    if os.path.isdir(fpath):
        return "dir"
    else:
        return fpath.split('.')[-1]

@process.command("qna-batch")
@click.option("--input", "-i",
              required=True,
              multiple=True,
              help="Path to input docset/file")
@click.option("--queryspec", "-q",
              required=True,
              help="Path to queryspec")
@click.option("--output", "-o",
              required=True,
              help="Path to store output json")
@click.option("--platform", "-p",
              default="openai",
              help="LLM platform backend to use {openai, azure}")
@click.option("--model", "-m",
              default="gpt-4o-mini",
              help="LLM model to use {gpt-3.5-turbo, gpt-4o-mini, gpt-4o}")
@click.option("--agenttype", "-t",
              default="queryextract",
              help="Agent type")
@click.option("--agentname", "-a",
              required=True,
              help="Agent name")
@click.option("--indexname", "-x",
              required=True,
              help="Name of index")
@click.option("--force-reindexing/--no-force-reindexing",
              required=False,
              default=True,
              help="Whether the index should be built")
@click.option("--vectorstore", "-s",
              default="chroma",
              help="Flavour of Vector DB (chroma, faiss)")
@click.option("--persistdirectory", "-p",
              default="chromadb",
              help="Path to directory to persist vector DB")
def qna_batch(agenttype, agentname, indexname,
              input, queryspec,
              output, platform, model, vectorstore,
              persistdirectory, force_reindexing):
    """
    Take a query spec and docset and extract information in batch mode
    """

    # create an agent
    if agenttype == 'queryextract':
        agent = LLMQuerierExtractor(name=agentname,
                                    platform=platform)
    elif agenttype in ['multistep']:
        agent = LLMMultiStepAgent(name=agentname,
                                    platform=platform, model=model)
    elif agenttype in ['hierarchical']:
        agent = LLMMultiStepAgent(name=agentname,
                                    platform=platform, model=model,
                                    chunk_size=5000, chunk_overlap=1000)
    else:
        # default to the older qna agent
        agent = LLMQuerierExtractor(name=agentname, platform=platform)


    # Cleanup the name. max 60 chars, starts and ends with
    # alphanumeric char
    indexname = slugify(indexname)[:60]
    indexname = re.sub(r"^[^a-zA-Z0-9]+","", indexname)
    indexname = re.sub(r"[^a-zA-Z0-9]+$","", indexname)

    print("Index", indexname)
    print("Persist Directory", persistdirectory)
    print("Force reindexing", force_reindexing)

    try:

        stats = None
        create = True

        if not force_reindexing:
            try:
                print("Trying to load index")
                agent.load_index(store=vectorstore,
                                 persist_directory=persistdirectory,
                                 index_name=indexname)
                stats = agent.get_index_stats()
                create = False
            except:
                #traceback.print_exc()
                pass
    except:
        # traceback.print_exc()
        stats = None
        create = True

    if ((stats is not None) and (stats['n_items'] == 0)):
        create = True

    if not create:
        summary = get_chroma_index_summary_files(indexname, persistdirectory)
        print(json.dumps(summary, indent=4))

    if create:
        print("Creating index")
        cnt = 0
        for fpath in input:
            # figure out the source
            source = get_path_source(fpath)

            # load the data
            data = agent.load_data(source=source, content=fpath)

            # add to index
            if cnt == 0:
                # only for the first file
                agent.create_add_index(data=data,
                                       store=vectorstore,
                                       persist_directory=persistdirectory,
                                       index_name=indexname)
            else:
                # for subsequent files
                agent.add_to_index(data=data)

            cnt += 1

    # load query spec
    queryspecfile = queryspec # dont confuse spec with filename of that spec
    if queryspecfile.endswith(".json"):
        with open(queryspecfile, "r") as fd:
            queryspec = json.load(fd)
    elif queryspecfile.endswith(".py"):
        module_name = "queryspecmod"
        spec = importlib.util.spec_from_file_location(module_name, queryspec)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Now get hold of query spec
        queryspec = module.get_queryspec()
    else:
        raise Exception(f"Unable to load the query spec: {queryspecfile}")

    # Limit the questions...for testing..
    # queryspec['query_set'] = queryspec['query_set'][:1]

    # process the spec
    if agenttype in ['queryextract', 'multistep']:
        responses = agent.process_spec(queryspec)
    elif agenttype in ['hierarchical']:
        responses = agent.process_hierarchical_spec(queryspec)
    else:
        responses = agent.process_spec(queryspec)

    # store
    with open(output, "w") as fd:
        json.dump(responses, fd, indent=2)
    print (f"Stored response json at: {output}")

#####################################
# news summarizer execution
#####################################
@process.command("news-summarizer")
@click.option("--agentname", "-a",
              required=True,
              help="Agent name")
@click.option("--action", "-c",
              default="summarize",
              help="Action to perform on news results {summarize, dedup}")
@click.option("--input", "-i",
              required=True,
              help="Path to news results")
@click.option("--rulespec", "-r",
              help="Path to rulespec")
@click.option("--output", "-o",
              required=True,
              help="Path to store output json")
@click.option("--platform", "-p",
              default="openai",
              help="LLM platform backend to use {openai, azure}")
@click.option("--model", "-m",
              default="gpt-4o-mini",
              help="LLM model to use {gpt-3.5-turbo, gpt-4o-mini, gpt-4o}")
def news_summarizer(agentname,
                      action, input, rulespec, output,
                      platform, model):
    """
    Take a summarization rule spec, news results json,
    and execute against a generic prompt LLM agent
    """

    # create a summarizer object
    summarizer = GoogleNewsSummarizer()
    # create an prompter agent
    # we need to pass this agent to the summarizer object
    agent = LLMPromptAgent(name=agentname,
                            platform=platform,
                            model=model)

    # load the news results data
    serp_results = summarizer.load_serp_results(input)

    if action == "summarize":
        # load rule spec
        rulespecfile = rulespec # dont confuse spec with filename of that spec
        if rulespecfile and rulespecfile.endswith(".py"):
            module_name = "queryspecmod"
            spec = importlib.util.spec_from_file_location(module_name, rulespec)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Now get hold of rules spec
            rulespec = module.get_rulespec()
        else:
            raise Exception(f"Unable to load the rule spec: {rulespecfile}")

        # run the summarization
        serp_results = summarizer.process_results(agent, serp_results, rulespec)
    else:
        # run the dedup
        serp_results = summarizer.dedup_results(agent, serp_results)

    # store the results
    summarizer.store_results(serp_results, output)
    print (f"Stored response json at: {output}")

#####################################
# dataset summarizer
#####################################
@process.command("dataset-summarizer")
@click.option("--agentname", "-a",
              required=True,
              help="Agent name")
@click.option("--input", "-i",
              required=True,
              help="Path to csv")
@click.option("--rulespec", "-r",
              required=True,
              help="Path to rulespec")
@click.option("--output", "-o",
              required=True,
              help="Path to store output json")
@click.option("--platform", "-p",
              default="openai",
              help="LLM platform backend to use {openai, azure}")
@click.option("--model", "-m",
              default="gpt-4o-mini",
              help="LLM model to use {gpt-3.5-turbo, gpt-4o-mini, gpt-4o}")
def dataset_summarizer(agentname,
                       input, rulespec, output,
                       platform, model):
    """
    Take a summarization rule spec, dataset csv
    and execute against a generic prompt LLM agent
    """

    # load prompt spec
    rulespecfile = rulespec # dont confuse spec with filename of that spec
    if rulespecfile.endswith(".py"):
        module_name = "queryspecmod"
        spec = importlib.util.spec_from_file_location(module_name, rulespec)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Now get hold of rules spec
        rulespec = module.get_rulespec()
    else:
        raise Exception(f"Unable to load the rule spec: {rulespecfile}")

    # create a summarizer object
    summarizer = DatasetSummarizer()

    # create an prompter agent
    # we need to pass this agent to the summarizer object
    agent = LLMPromptAgent(name=agentname,
                           platform=platform,
                           model=model)
    # load the news results data
    data = summarizer.load_dataset(input)

    # run the summarization
    result = summarizer.process_results(agent, data, rulespec)

    # store the results
    summarizer.store_results(result, output)
    print (f"Stored response json at: {output}")


#####################################
# DocGen
#####################################
@process.command("docgen-run")
@click.argument("dataset")
@click.argument("specification")
@click.option("--output", "-o",
              help="Output file")
def docgen(dataset, specification, output):
    """
    Generate document
    """

    if 'DATA_ROOT' not in os.environ:
        show_help()
        return

    # Load the specification
    spec = json.load(open(specification))

    # Get the agent
    details = async_to_sync(get_agent_details)(namespace="docgen",
                                               username="cli",
                                               subdir=dataset,
                                               exts=docgen_supported_exts,
                                               get_task_specific_agent=get_docgen_agent)

    # Generate the output
    answer   = details['agent'].generate_doc(spec)

    # => Now output the result..
    text = answer # answer not a json
    if output is not None:
        output = os.path.abspath(output)
        with open(output, 'w') as fd:
            fd.write(text)
        print(f"Output: {output}")
    else:
        print(text)

@process.command("docgen-sample-spec")
@click.option("--output", "-o",
              help="Output file")
def docgen_spec(output):
    """
    Generate a sample specification
    """
    profilespec = {
	    "prompt": {
		    "prefix": "write a para about",
		    "suffix": "for this startup company"
	    },
	    "sections": {
		    "about": {
			    "enable": True,
		        "title": "About the Company",
			    "intent": "introducing the startup",
			    "questions": [
				    "industry and specific focus",
				    "key technologies developed",
				    "unique value proposition"
			    ],
			    "collate": False,
		    },
		    "founders": {
			    "enable": True,
			    "title": "Company Founders",
			    "intent": "about the co-founders of the startup",
			    "questions": [
				    "co-founders and the roles they hold",
				    "past experience of co-founders"
			    ],
			    "collate": "rewrite"
		    },
		    "market-analysis": {
			    "enable": True,
			    "title": "Market Analysis",
			    "intent": "about market analysis for this startup",
		        "questions": [
			        "target customer base",
			        "other potential customers",
				    "other comparable companies and startups in this space",
				    "the main competitors",
				    "biggest risk factors",
				    "key differentiators",
				    "market trends for the domain"
			    ],
			    "collate": False
		    }
	    }
    }

    text = json.dumps(profilespec, indent=4)
    if output is not None:
        output = os.path.abspath(output)
        with open(output, 'w') as fd:
            fd.write(text)
        print(f"Output: {output}")
    else:
        print(text)

#####################################
# DataGPT
#####################################
@process.command("datagpt")
@click.argument("dataset")
@click.argument("question")
@click.option("--output", "-o",
              default=None,
              help="Output file")
def datagpt(dataset, question, output):
    """
    Interact with a dataset
    """

    if 'DATA_ROOT' not in os.environ:
        show_help()
        return

    details = async_to_sync(get_agent_details)(namespace="datagpt",
                                               username="cli",
                                               subdir=dataset,
                                               exts=datagpt_supported_exts,
                                               get_task_specific_agent=get_datagpt_agent)

    result = details['agent'].query(question)

    text = json.dumps(result, indent=4)
    if output is not None:
        output = os.path.abspath(output)
        with open(output, 'w') as fd:
            fd.write(text)
        print(f"Output: {output}")
    else:
        print(text)

#####################################
# DATA CLEANER (using SADL)
#####################################
@process.command("data-cleaner")
@click.option("--platform", "-p",
              default="openai",
              help="LLM platform backend to use {openai, azure}")
@click.option("--action", "-a",
              default="map",
              help="Type of action to perform {map, label}")
@click.option("--input", "-i",
              required=True,
              help="Path to input CSV")
@click.option("--targets", "-t",
              default=None,
              help="Path to target classes CSV")
@click.option("--usecontent", "-c",
              default=False,
              help="Whether to use data samples while labelling")
@click.option("--output", "-o",
              default=None,
              help="Output file")
def data_cleaner(platform, action, input, targets, usecontent, output):
    """
    Take a CSV file and label the columns
    Two modes are supported via the action param
        - map: map each column name to a provided list of target classes
        - label: try to guess the column label automatically [not supported right now]
    """

    # init the agent
    labeller = SADLClassifier(platform=platform)

    # check for the input file
    if not os.path.exists(input):
        print("Input file does not exist. Exiting.")
        return

    # load the data
    data = labeller.load_data(input, source="csv")

    if action == "map":
        # check for the targets file
        if not os.path.exists(targets):
            print("Target Classes file does not exist. Exiting.")
            return
        with open(targets, "r") as fd:
            target_classes = fd.readlines()
        # run the mapping
        mapping = labeller.map_to_targets(data, target_classes, use_content=usecontent)

    # store
    with open(output, "w") as fd:
        json.dump(mapping, fd, indent=2)
    print (f"Stored mapping json at: {output}")



#####################################
# Contract processing
#####################################
@process.command("contract-sample-spec")
@click.argument("specfile")
@click.option("--nature", "-n",
              default="contract",
              type=click.Choice(['contract'],
                                case_sensitive=False))
def contract_sample_spec(nature, specfile):
    """
    Get a sample spec for extractor

    Store as llm-runner extractor-sample-spec -n contract 2> .../work/spec.py
    """

    if 'DATA_ROOT' not in os.environ:
        show_help()
        return

    if os.path.exists(specfile):
        print("Specfile exists. Please remove first")
        print(specfile)
        return

    spec = inspect.getsource(get_contract_profilespec)
    spec += "\nget_spec = get_contract_profilespec\n"

    with open(specfile, 'w') as fd:
        fd.write(spec)

    print("Use this with extractor-run")
    print(f"llm-runner extractor-run {specfile} <source-document>")

@process.command("contract-run")
@click.argument("spec")
@click.argument("filename")
@click.option("--output", "-o",
              default=None,
              help="Output file")
def contract_extractor_run(spec, filename, output):
    """
    Run a extractor spec against the input files

    spec is generated using extractor-sample-spec
    """

    if ((os.path.abspath(filename) != filename) or
        (os.path.abspath(spec) != spec) or
        ((output is not None) and
         (os.path.abspath(output) != output))):
        print("This command required absolute paths for spec/inputfile/output")
        return

    if not os.path.exists(filename):
        print(f"Input file is missing: {filename}")
        return

    if not os.path.exists(spec):
        print(f"Profile spec file is missing: {spec}")
        return

    # Load the specification
    modspec = importlib.util.spec_from_file_location("samplemod", spec)
    mod = importlib.util.module_from_spec(modspec)
    modspec.loader.exec_module(mod)
    profilespec = mod.get_spec()

    result, metadata = contract_query(profilespec, filename)

    # output extraction
    text = json.dumps({
        "result": result,
        "metadata": metadata
    }, indent=4)

    if output is not None:
        output = os.path.abspath(output)
        with open(output, 'w') as fd:
            fd.write(text)
        print(f"Output: {output}")
    else:
        print(text)


@process.command("check-chroma-index")
@click.option("--persistdirectory", "-p",
              default="chromadb",
              help="Path to directory to persist vector DB")
@click.option("--indexname", "-x",
              required=True,
              help="Name of index")
@click.option('--nature', '-n',
              type=click.Choice(['files', 'generic']),
              default='generic')
@click.option("--output", "-o",
              required=False,
              help="Output File")
def check_chromadb(persistdirectory, indexname, output, nature):
    """
    Check vector db
    """
    indexname = slugify(indexname)
    if nature == 'files':
        summary = get_chroma_index_summary_files(indexname, persistdirectory)
    else:
        summary = get_chroma_index_summary_generic(indexname, persistdirectory)

    if output is None:
        print(json.dumps(summary, indent=4))
    else:
        with open(output, 'w') as fd:
            fd.write(json.dumps(summary, indent=4))

@click.group()
@click.option("--server", "-s",
              default="http://localhost:9010",
              help="Server")
@click.pass_context
def databank(ctx, server):
    """
    Databank commands
    """
    ctx.ensure_object(dict)
    ctx.obj = {
        "server": server
    }


@databank.command("health")
@click.pass_context
def databank_health(ctx):
    """
    Check databank health
    """

    server = ctx.obj['server']
    url = server + "/health"
    response = requests.get(url)
    response = response.json()
    print(json.dumps(response, indent=4))

@databank.command("load")
@click.argument("csvfile")
@click.argument("columns")
@click.pass_context
def databank_load_data(ctx, csvfile, columns):
    """
    Load data in databank
    """
    assert csvfile.endswith("csv")
    assert isinstance(columns, str) and len(columns) > 0

    columns = columns.split(",")
    reader = csv.DictReader(open(csvfile))
    data = list(reader)
    print(f"Read file with {len(data)} records")
    print(json.dumps(data[:2], indent=4))
    record = data[0]
    missing = [c for c in columns if c not in record]
    if len(missing) > 0:
        print(f"Columns not present in csv: {missing}")
        return
    print(f"All columns present: {columns}")

    server = ctx.obj['server']
    url = server + "/load"
    response = requests.post(url, json={
        "data": data,
        "params": {
            "index_columns": columns
        }
    })
    print("Response status", response.status_code)
    if response.status_code < 400:
        response = response.json()
        print(json.dumps(response, indent=4))
    else:
        print(response.text)

@databank.command("query")
@click.argument("query")
@click.pass_context
def databank_query(ctx, query):
    """
    Query databank
    """
    server = ctx.obj['server']
    url = server + "/qna"
    response = requests.post(url,
                             params={
                                 "query": query,
                                 "dataset": "default",
                                 "user": "anyone",
                             },
                             json={
                                 "policy": {},
                                 "extra": {}
                             })


    print("=> Query")
    print("Response status", response.status_code)
    if response.status_code < 400:
        response = response.json()
        print(json.dumps(response, indent=4))
        request_id = response['request_id']
    else:
        print(response.text)
        return

    url = server + "/qna/status"
    while True:
        print(f"=> Status {request_id}")
        response = requests.get(url, params={
            'request_id': request_id
        })
        if response.status_code < 400:
            response = response.json()
            print(json.dumps(response, indent=4))
            status = response['status']
            if status == 'pending':
                time.sleep(5)
                continue
            else:
                break
        else:
            print(response.text)
            break

process.add_command(databank)

def main():
    process()

if __name__ == "__main__":
    main()
