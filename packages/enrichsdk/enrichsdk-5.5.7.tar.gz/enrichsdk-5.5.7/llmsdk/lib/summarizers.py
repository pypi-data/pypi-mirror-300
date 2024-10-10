import json
import hashlib

__all__ = [
    'GoogleNewsSummarizer',
    'DatasetSummarizer'
]

class GoogleNewsSummarizer(object):
    """
    Class to handle summarization of Google News search results
    """

    def __init__(self):
        pass

    def create_id(self, string):
        """
        create a unique identifier from a string
        """
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def load_serp_results(self, file_path):
        """
        Take a json file path and load the results data
        """
        with open(file_path, "r") as fd:
            serp_results = json.load(fd)
        return serp_results

    def summarize_results(self, agent, serp_result, rulespec):
        """
        Construct the LLM prompt and call the agent to summarize
        """
        ## defaults
        default_ruleset = [
            "inlcude the source and URL for all news snippets you use to construct the summary using this format [source; url]"
        ]

        ## get the rules information
        # summary length
        summary_length = int(rulespec.get("summary_length", 100))

        # ruleset
        rule_set = rulespec.get("rule_set", default_ruleset)
        rule_set = [f"{ix}. {rule}" for ix, rule in enumerate(rule_set)]
        rule_set = "\n".join(rule_set)

        # cleaner method
        cleaner = rulespec.get("methods", {}).get("cleaner")
        crawler = rulespec.get("methods", {}).get("crawler")

        ## construct the prompt
        # get the news results
        for name in ['news', 'organic', 'video']:
            label = f"{name}_results"
            if label in serp_result:
                results = serp_result[label]
                break

        print("Results", len(results))
        # get the Google query
        g_query = serp_result["search_parameters"]["q"]
        # run the query cleaner method
        if callable(cleaner):
            g_query = cleaner(g_query)

        # get the snippets
        snippets = []
        count = 0
        for result in results:
            count += 1
            link = result["link"]
            title = result["title"]
            source = result.get("source", "Unknown")
            snippet = result.get("original_snippet")
            if snippet == None:
                snippet = result.get("snippet", "")
            content = result.get("snippet", "")
            # run the crawler method
            if callable(crawler):
                snippet = crawler(link)

            entry = f"""
                [Result Number: {count}]
                Title: {title}
                Snippet: {snippet}
                Source: {source}
                URL: {link}
            """
            # take care of the case where snippet has been overwritten with original_snippet
            if "original_snippet" in result:
                entry = f"""{entry}
                Content: {content}
                """
            snippets.append(entry)
        snippets = "\n\n".join(snippets)

        prompt = {
            "persona": """You are a highly advanced AI capable of summarizing Google News and other search result snippets.""",
            "prompt": f"""
                ## Input
                The following are a set of {len(results)} news results snippets and crawled page content from the results of a Google query:
                {snippets}

                The query terms issued to Google were: {g_query}

                ## Your task is to summarize the news results snippets for a reader in {summary_length} words or less. Pay special attention to the following rules:
                {rule_set}

                ## Your summary:"""
        }

        ## run prompt
        # call the LLM with the prompt
        response = agent.prompt(prompt)

        return response

    def process_results(self, agent, serp_results, rulespec):
        """
        Process all the search results for summarization
        """
        for serp_result in serp_results:

            if not isinstance(serp_result, dict):
                continue

            checks = [f"{name}_results" in serp_result \
                          for name in ['news', 'organic', "video"]]
            if not any(checks):
                continue

            response = self.summarize_results(agent, serp_result, rulespec)
            summary = response["answer"]

            try:
                serp_result["summary"] = json.loads(summary)
            except:
                serp_result["summary"] = summary

        return serp_results

    def dedup_results(self, agent, serp_results):
        """
        De-duplicate the news results
        """

        # create an id for each summary text
        snippets = []
        for r in serp_results:
            summary = r.get('summary', {})
            texts = summary.get('summary', [])
            if not isinstance(texts, list):
                continue
            if len(texts) > 0:
                for text in texts:
                    if not isinstance(text, dict):
                        continue
                    t = text.get('text', "")
                    text['id'] = self.create_id(t)
                    snippets.append({
                        "id": text['id'],
                        "text": t,
                    })

        entries = []
        for s in snippets:
            entry = f"""
                ID: {s['id']}
                Snippet: {s['text']}
            """
            entries.append(entry)
        entries = "\n\n".join(entries)

        prompt = {
            "persona": """You are a highly advanced AI capable of deduplicating snippets of text.""",
            "prompt": f"""
                ## Input
                The following are a set of {len(entries)} text snippets:
                {entries}

                ## Your task is to deduplicate the set of text snippets.
                If there are multiple text snippets with the same meaning, inlcude only the first one in your response.
                If a text snippet contains any variation of the phrase "Nothing Relevant", do not include it in your response.

                Format your response as a list of JSON objects as """ + "{id: ID, text: snippet}" + """
                DO NOT include code tags.

                ## Your response:"""
        }


        ## run prompt
        # call the LLM with the prompt
        response = agent.prompt(prompt)
        try:
            results = json.loads(response['answer'])
        except:
            print("Received unexpected response")
            print(response)
            raise

        valid_stories = {result.get("id"): result.get("text") for result in results}

        # go through the summary texts and drop duplicates
        # duplicate texts will not be found in valid_stories
        for r in serp_results:
            summary = r.get('summary', {})
            texts = summary['summary']
            if not isinstance(texts, list):
                continue
            texts = [t for t in texts if (isinstance(t, dict) and ('id' in t))]
            if len(texts) > 0:
                texts = [text for text in texts if text["id"] in valid_stories]
                summary['summary'] = texts

        return serp_results

    def store_results(self, serp_results, out_file_path):
        """
        Store the summary results
        """
        with open(out_file_path, "w") as fd:
            json.dump(serp_results, fd, indent=4)

class DatasetSummarizer(object):
    """
    Class to handle summarization of dataset
    """
    def load_dataset(self, inputfile):
        """
        Load the dataset. For now it is not doing anything interesting but
        may be it will do something useful in future
        """

        if not inputfile.lower().endswith(".csv"):
            raise Exception("Only csv files supported")

        return open(inputfile).read()

    def process_results(self, agent, data, rulespec):

        ## defaults
        default_ruleset = [
            "Analyze the dataset and summarize observations"
        ]

        # summary length
        summary_length = int(rulespec.get("summary_length", 100))
        description = rulespec.get("description", "")

        # ruleset
        rule_set = rulespec.get("rule_set", default_ruleset)
        rule_set = [f"{ix}. {rule}" for ix, rule in enumerate(rule_set)]
        rule_set = "\n".join(rule_set)

        prompt = {
            "persona": """You are a highly advanced AI capable of analyzing datasets and providing accurate and relevant answers""",
            "prompt": f"""
                {description}

                ## Input
                The following is a set of records in CSV format:
                {data}

                ## Your task is to summarize the records for a reader in {summary_length} words or less. Pay special attention to the following rules:
                {rule_set}

                ## Your summary:"""
        }

        ## run prompt
        # call the LLM with the prompt
        response = agent.prompt(prompt)

        return response

    def store_results(self, result, outputpath):
        """
        Store the summary results
        """
        with open(outputpath, "w") as fd:
            json.dump(result, fd, indent=4)
