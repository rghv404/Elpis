import json

from watson_developer_cloud import AssistantV2

from server.watson.case import Case

Questionnaire_Score_Map = {
    "Not_At_All": 0,
    "Several_Days": 1,
    "More_Than_Half_The_Days": 2,
    "Nearly_Everyday": 3
}


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
        self.session = self.assistant.create_session(self.assistant_id).get_result()
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

        # Update name if does not exist
        if not self.case.name:
            name, confidence = Assistant._get_entity(msg["output"], "sys-person")
            if name:
                self.case.name = name
                print("User name is {}".format(self.case.name))

        # Update location if does not exist
        if not self.case.location:
            location, confidence = Assistant._get_entity(msg["output"], "sys-location", ",")
            if location:
                self.case.location = location
                w_str, temp = fetch_weather(self.case.location)
                print("Location is {}".format(self.case.location))
                print("{}, Temp {}".format(w_str, temp))

        # Print the response returned by the assistant, if it exists
        text_msg = Assistant._get_text_response(msg["output"])
        if text_msg:
            print("Response from Assistant: {}".format(text_msg))

        # Calculate severity score at every interaction
        self.case.severity_score += Assistant._get_score(msg["output"])
        return msg

    def bye(self):
        print("Closing assistant session")
        return self.assistant.delete_session(
            assistant_id=self.assistant_id,
            session_id=self.session_id
        )

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

    @staticmethod
    def _get_text_response(message):
        if message['generic']:
            text_msg = [msg["text"] for msg in message["generic"]]
            return "\n".join(text_msg)
        return None

    @staticmethod
    def _get_score(message):
        sev_score = 0
        curr_response_intent = message["intents"][0]["intent"]

        # checking if intent belongs to depression severity maps
        # if yes then calculate the score else move on
        if curr_response_intent in Questionnaire_Score_Map:
            sev_score += Questionnaire_Score_Map[curr_response_intent]
        return sev_score

    def _set_entity(self, entity_name, value):
        pass
