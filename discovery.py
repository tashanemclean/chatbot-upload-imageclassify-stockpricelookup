from __future__ import print_function
import json
from ibm_watson import DiscoveryV1

discovery = DiscoveryV1(
    version="2019-06-12",
    url="https://gateway.watsonplatform.net/discovery/api",
    iam_apikey="Zp2aRM112cxTZq_9_NRNMLLWyPVzrD4beCxPHJS1PPoj"
)

def discovery_query():
    new_col = discovery.query("49701d2f-c8a3-4a97-92ce-90d475c204f8", "6b9e5228-af9f-49fd-8d52-6c45aba0c43b",
        natural_language_query=f"{userInput}",
        count=1,
        return_fields="answer",
        highlight=True,
        similar=True,
        deduplicate_field="result",
        duplicates_removed=5,
    )

    return ""


news_environment_id = "49701d2f-c8a3-4a97-92ce-90d475c204f8"

collections = discovery.list_collections("49701d2f-c8a3-4a97-92ce-90d475c204f8").get_result()
news_collections = [x for x in collections['collections']]
# print(json.dumps(collections, indent=2))

# configurations = discovery.list_configurations(
#     environment_id=news_environment_id).get_result()
# print(json.dumps(configurations, indent=2))
# new_col = discovery.get('')
# query_results = discovery.query(
#     "49701d2f-c8a3-4a97-92ce-90d475c204f8",
#     news_collections[0]['collection_id'],
#     filter='term(question,count:3).term("can i have more than one nominee",count:3)',
#     return_fields='term(question,count:3).term(answer,count:3').get_result()
# print(json.dumps(query_results, indent=2))

# environments = discovery.list_environments().get_result()
# print(json.dumps(environments, indent=2))