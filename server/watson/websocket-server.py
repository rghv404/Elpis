from __future__ import print_function, absolute_import
import asyncio
import websockets

from assistant import Assistant

ApiKeys = {"owm": "6cce1ac5218007fcf2eb6a1a7786be79"}

Questionnaire_Score_Map = {
    "Not_At_All": 0,
    "Several_Days": 1,
    "More_Than_Half_The_Days": 2,
    "Nearly_Everyday": 3
}

shown_weather = False


async def communicate(websock, path):
    global shown_weather
    iam_apikey = "zZgd_U8JM-zH7fsNulDgEXlh-wcBzQs1n7zbmX8Zk8CN"
    assistant_id = "38226af1-7add-488c-9774-e523dd61cbb8"
    assistant = Assistant(iam_apikey, assistant_id)
    test_message = await websock.recv()
    while test_message is not None:
        message = assistant.ask_assistant(test_message)
        msg = Assistant._get_text_response(message["output"])
        if "weather" in assistant.pass_date and not shown_weather:
            w_str, temp = assistant.pass_date["weather"]["w_str"], assistant.pass_date["weather"]["temp"]
            if str(w_str).lower().__contains__("snow"):
                msg = "The weather in {0} appears to be quite cold, with temperatures of {2} Celsius. {3}".format(
                    assistant.case.location, w_str, temp, msg
                )
            elif str(w_str).lower().__contains__("rain"):
                msg = "The weather in {0} appears to be quite rainy, with temperatures of {2} Celsius. {3}".format(
                    assistant.case.location, w_str, temp, msg
                )
            else:
                msg = "The weather in {0} is {1}, with temperatures of {2} Celsius. {3}".format(
                    assistant.case.location, w_str, temp, msg
                )
            shown_weather = True
        print("Context at this point: {}".format(assistant.context))
        await websock.send(msg)
        test_message = await websock.recv()
    assistant.bye()
    return True


if __name__ == "__main__":
    start_server = websockets.serve(communicate, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
