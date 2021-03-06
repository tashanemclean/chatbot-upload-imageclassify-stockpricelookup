from __future__ import print_function
import json
from os.path import join, dirname
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput

tone_analyzer = ToneAnalyzerV3(
    version="2019-06-12",
    iam_apikey="LsbsX4ox9m_u8IxPzE8alIEykpwxk2qqkyOrFy38i5GT",
    url="https://gateway.watsonplatform.net/tone-analyzer/api"
)

# print("\ntone_chat() example 1:\n")
# utterances = [{
#     "text": "Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!",
#     "user": "glenn"
# }, {
#     "text": "It is a good day.",
#     "user": "glenn"
# }]
# tone_chat = tone_analyzer.tone_chat(utterances).get_result()
# print(json.dumps(tone_chat, indent=2))

# print("\ntone() example 2:\n")
# with open(join(dirname(__file__),
#                 'resources/tone.json')) as tone_json:
#     tone = tone_analyzer.tone(json.load(tone_json)['text'], content_type="text/plain").get_result()
# print(json.dumps(tone, indent=2))

# print("\ntone() example 6 with GDPR support:\n")
# with open(join(dirname(__file__),
#                 'resources/tone.json')) as tone_html:
#     tone = tone_analyzer.tone(
#         json.load(tone_html)["text"],
#         content_type="text/html",
#         headers={
#             'Customer-Header': "custom_value"
#         })

# print(tone)
# print(tone.get_headers())
# print(tone.get_result())
# print(tone.get_status_code())

print("\ntone( example 7:\n")
tone_input = ToneInput("I am very happy. It is a good day.")
tone = tone_analyzer.tone(tone_input=tone_input, content_type="application/json").get_result()
print(json.dumps(tone, indent=2))