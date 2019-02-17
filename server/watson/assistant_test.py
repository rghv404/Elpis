from __future__ import print_function, absolute_import
import requests as r

from server.watson.assistant import Assistant

msg = {"hi": "Hello",
       "severe-1": "I feel like killing myself",
       "location-1": "I am in Buffalo",
       "q_location": "Where am I?",
       "q_name": "What is my name?",
       "get_name": "Hello my name is John"}

ApiKeys = {"owm": "6cce1ac5218007fcf2eb6a1a7786be79"}

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


if __name__ == "__main__":
    iam_apikey = "zZgd_U8JM-zH7fsNulDgEXlh-wcBzQs1n7zbmX8Zk8CN"
    assistant_id = "38226af1-7add-488c-9774-e523dd61cbb8"

    assistant = Assistant(iam_apikey, assistant_id)

    test_flow = [
        "hey",
        "hey",
        "my name is john",
        "I am from buffalo",
        "I am feeling lonely",
        "ok",
        "often",
        "rarely"
    ]

    for test_message in test_flow:
        # test_message = msg["hi"]
        print("Sending to Watson: ", test_message)
        message = assistant.ask_assistant(test_message)
    print("Severity score: {}".format(assistant.case.severity_score))

    assistant.bye()
