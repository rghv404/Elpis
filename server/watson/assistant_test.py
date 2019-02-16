from __future__ import print_function, absolute_import
import json
from watson_developer_cloud import AssistantV2

msg = {"hi": "Hello",
       "severe-1": "I feel like killing myself",
       "get_name": "Hello my name is John"}


class Case:
    def __init__(self, name="", location="", problem_description=""):
        self.name = name
        self.location = location
        self.problem_description = problem_description
        return None


class Assistant:
    def __init__(self, apikey, asst_id):
        self.assistant = AssistantV2(version="2019-02-16",
                                     iam_apikey=apikey)

        self.assistant_id = asst_id
        self.session = self.assistant.create_session(assistant_id).get_result()
        self.session_id = self.session["session_id"]
        self.case = Case()
        print("Watson assistant session details: {}".format(json.dumps(self.session)))
        return None

    def ask_assistant(self, message):
        msg = self.assistant.message(
            self.assistant_id,
            self.session_id,
            input={'text': message},
            context={
                'metadata': {
                    'deployment': 'myDeployment'
                }
            }).get_result()
        if not self.case.name:
            name, confidence = Assistant._get_entity(msg["output"], "sys-person")
            if name:
                self.case.name = name
                print("User name is {}".format(self.case.name))
        return msg

    @staticmethod
    def _get_entity(message, entity_name):
        for et in message["entities"]:
            if et["entity"] == entity_name:
                return et["value"], et["confidence"]
        return None, None

    def _set_entity(self, entity_name, value):
        pass


if __name__ == "__main__":
    iam_apikey = "zZgd_U8JM-zH7fsNulDgEXlh-wcBzQs1n7zbmX8Zk8CN"
    assistant_id = "38226af1-7add-488c-9774-e523dd61cbb8"

    assistant = Assistant(iam_apikey, assistant_id)

    # test_message = "I feel like killing myself"
    for val in msg.values():
        print("Message being sent: {}".format(val))
        # test_message = msg["get_name"]
        message = assistant.ask_assistant(val)
        print(json.dumps(message, indent=2))
