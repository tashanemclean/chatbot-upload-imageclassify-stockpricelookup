from __future__ import print_function
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from ibm_watson import AssistantV1
import requests
import os
import datetime as dt
from ibm_watson import DiscoveryV1
import discovery
import pandas as pd
import visual_recognition


app = Flask(__name__)
CORS(app)

assistant = AssistantV1(
    version='2019-06-13',
    url='https://gateway.watsonplatform.net/assistant/api',
    iam_apikey='Fftjw_NhK3I-mJNKE-0zqSJe76X9z0uWbyVshoseWvQc'
)

discovery = DiscoveryV1(
    version="2019-06-12",
    url="https://gateway.watsonplatform.net/discovery/api",
    iam_apikey="Zp2aRM112cxTZq_9_NRNMLLWyPVzrD4beCxPHJS1PPoj"
)

@app.route('/chatlog')
def chat_log():
    response = assistant.list_logs(workspace_id='ace10bc5-2a14-440a-97c1-835faf5c46df').get_result()
    return json.dumps(response)

@app.route('/upload', methods=["POST"])
def send_img():
    ss = visual_recognition.image_to_upload_and_classify()
    return ss


@app.route('/sendmessage', methods={"POST"})
def send_message():
    if request.content_type == "application/json":
        post_data = request.get_json()
        userInput = post_data.pop('usrInput')
        response = assistant.message(
        workspace_id='ace10bc5-2a14-440a-97c1-835faf5c46df',
        input={
            'text': f'{userInput}'
        },
        context={
            'metadata': {
                'deployment': 'myDeployment'
            }
        }).get_result()
        lookUpStock = response
        stockLookup = lookUpStock["intents"].pop()["intent"]
        symbol_text = response
        if stockLookup == "General_Connect_to_Agent":
            query_key = discovery.query("49701d2f-c8a3-4a97-92ce-90d475c204f8", "6b9e5228-af9f-49fd-8d52-6c45aba0c43b",
            natural_language_query=f"{userInput}",
            aggregation="term(answer.keywords.text).top_hits(1)",
            )

            query_question = query_key.result["results"][0]["question"]
            query_answer = query_key.result["results"][0]["answer"]
            query_filename = query_key.result["results"][0]["extracted_metadata"]['filename']
            query_question = pd.Series(query_question)
            query_answer = pd.Series(query_answer)
            
            count = 0
            for query_string in query_question:
                count += 1
                if (len(query_string) == len(userInput)):
                    query_string = userInput
                    count -= 1
                    query_ans = query_answer[count]

                    x = response["output"]["text"].pop()
                    x = response["output"]["text"].append(query_ans)
                    return json.dumps(response)
            return json.dumps(response)
            print(json.dumps(response, indent=2))

        else:

            stock_to_look_up = symbol_text["input"].pop('text')
            entity_check = symbol_text["entities"]
            for i in entity_check:
                entity_check = i
                entity_check = entity_check["entity"]
            if stockLookup == "company_stock_symbol":
                stock_to_look_up = userInput
                tNow  = dt.datetime.now()
                tNow -= dt.timedelta(minutes = tNow.minute, seconds = tNow.second, microseconds =  tNow.microsecond)
                tNow += dt.timedelta(hours = -.5)
                stock_symbol = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_to_look_up}&interval=5min&apikey=WJZTZH8OHJ586STD"
                data=requests.get(stock_symbol)
                data=data.json()
                stock_data = data['Time Series (5min)']
                price = stock_data[f"{tNow}"]["1. open"]
                current_price = f"Here is the current market price for {userInput}: " + price
                p = response["output"]["text"].pop()
                p = response["output"]["text"].append(current_price)
                return json.dumps(response)
            return json.dumps(response)
            print(json.dumps(response, indent=2))

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)