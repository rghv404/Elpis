from __future__ import print_function, absolute_import
import json
from watson_developer_cloud import AssistantV2

if __name__ == "__main__":
    assistant = AssistantV2(version="2019-02-16",
                            iam_apikey="vStMz9hAxwmSPZm3pcaQYp2uMBSN6nqIFtloWNSaaSaq")

    assistant_id = "0b6f795c-82f8-4315-9998-368560192535"
    session = assistant.create_session(assistant_id).get_result()
    session_id = session["session_id"]
    message = assistant.message(
        assistant_id,
        session_id,
        input={'text': 'What\'s the weather like?'},
        context={
            'metadata': {
                'deployment': 'myDeployment'
            }
        }).get_result()
    print(json.dumps(message, indent=2))
    print(json.dumps(session))
