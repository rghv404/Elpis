from __future__ import print_function, absolute_import
import json
from watson_developer_cloud import AssistantV2


class Assistant:
    def __init__(self, apikey, asst_id):
        self.assistant = AssistantV2(version="2019-02-16",
                                     iam_apikey=apikey)

        self.assistant_id = asst_id
        self.session = self.assistant.create_session(assistant_id).get_result()
        self.session_id = self.session["session_id"]
        print("Watson assistant session details: {}".format(json.dumps(self.session)))
        return None

    def ask_assistant(self, message):
        message = self.assistant.message(
            self.assistant_id,
            self.session_id,
            input={'text': message},
            context={
                'metadata': {
                    'deployment': 'myDeployment'
                }
            }).get_result()
        return message


if __name__ == "__main__":
    iam_apikey = "zZgd_U8JM-zH7fsNulDgEXlh-wcBzQs1n7zbmX8Zk8CN"
    assistant_id = "38226af1-7add-488c-9774-e523dd61cbb8"

    assistant = Assistant(iam_apikey, assistant_id)

    test_message = "I feel like killing myself"
    message = assistant.ask_assistant(test_message)
    print(json.dumps(message, indent=2))
