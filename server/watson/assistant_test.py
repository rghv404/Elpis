from __future__ import print_function, absolute_import
import requests as r
import json
import math
from watson_developer_cloud import AssistantV2

msg = {"hi": "Hello",
       "severe-1": "I feel like killing myself",
       "location-1": "I am in Buffalo",
       "q_location": "Where am I?",
       "q_name": "What is my name?",
       "get_name": "Hello my name is John"}

ApiKeys = {"owm": "6cce1ac5218007fcf2eb6a1a7786be79"}


class Case:
    def __init__(self, name="", location="", problem_description=""):
        self.name = name
        self.location = location
        self.problem_description = problem_description
        return None


def fetch_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}".format(
        location, ApiKeys["owm"]
    )
    response = r.get(url)
    data = response.json()
    w_str = "{}, {}".format(data["weather"][0]["main"], data["weather"][0]["description"])
    temp = round(float(data["main"]["temp"]) - 273, 2)
    return w_str, temp


class Assistant:
    def __init__(self, apikey, asst_id):
        self.assistant = AssistantV2(version="2019-02-16",
                                     iam_apikey=apikey)

        self.assistant_id = asst_id
        self.session = self.assistant.create_session(assistant_id).get_result()
        self.session_id = self.session["session_id"]
        self.case = Case()
        self.context = None
        print("Watson assistant session details: {}".format(json.dumps(self.session)))
        return None

    def ask_assistant(self, message):
        response = self.assistant.message(
            self.assistant_id,
            self.session_id,
            input={
                'text': message,
                'options': {
                    'return_context': True
                }
            },
            # context={
            #     'metadata': {
            #         'deployment': 'myDeployment'
            #     }
            # }
            context=self.context
        )
        msg = response.get_result()
        if not msg["context"]:
            print("Context: {}".format(self.context))
            self.context = msg["context"]
        if not self.case.name:
            name, confidence = Assistant._get_entity(msg["output"], "sys-person")
            if name:
                self.case.name = name
                print("User name is {}".format(self.case.name))
        if not self.case.location:
            location, confidence = Assistant._get_entity(msg["output"], "sys-location", ",")
            if location:
                self.case.location = location
                w_str, temp = fetch_weather(self.case.location)
                print("Location is {}".format(self.case.location))
                print("{}, Temp {}".format(w_str, temp))
        return msg

    @staticmethod
    def _get_entity(message, entity_name, join_char=" "):
        val = []
        confidence = 0.0
        idx = 1
        for et in message["entities"]:
            if et["entity"] == entity_name:
                val.append(et["value"])
                confidence += et["confidence"]
                idx += 1
        if val:
            return "{}".format(join_char).join(val).strip(" "), confidence / idx
        return None, None

    def _set_entity(self, entity_name, value):
        pass


if __name__ == "__main__":
    iam_apikey = "zZgd_U8JM-zH7fsNulDgEXlh-wcBzQs1n7zbmX8Zk8CN"
    assistant_id = "38226af1-7add-488c-9774-e523dd61cbb8"

    assistant = Assistant(iam_apikey, assistant_id)

    # test_message = "I feel like killing myself"
    # for val in msg.values():
    #     print("Message being sent: {}".format(val))
    test_message = msg["location-1"]
    for test_message in [msg["get_name"], msg["q_name"], msg["location-1"], msg["q_location"]]:
        print("Sending", test_message)
        message = assistant.ask_assistant(test_message)
        print(json.dumps(message, indent=2))
