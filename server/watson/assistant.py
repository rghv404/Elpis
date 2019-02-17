import csv
import json
import requests as r

from watson_developer_cloud import AssistantV2

from server.watson.case import Case

ApiKeys = {"owm": "6cce1ac5218007fcf2eb6a1a7786be79"}

Questionnaire_Score_Map = {
    "Not_At_All": 0,
    "Several_Days": 1,
    "More_Than_Half_The_Days": 2,
    "Nearly_Everyday": 3
}

List_Cities = ["Aberdeen",
               "Abilene",
               "Akron",
               "Albany",
               "Albuquerque",
               "Alexandria",
               "Allentown",
               "Amarillo",
               "Anaheim",
               "Anchorage",
               "Ann Arbor",
               "Antioch",
               "Apple Valley",
               "Appleton",
               "Arlington",
               "Arvada",
               "Asheville",
               "Athens",
               "Atlanta",
               "Atlantic City",
               "Augusta",
               "Aurora",
               "Austin",
               "Bakersfield",
               "Baltimore",
               "Barnstable",
               "Baton Rouge",
               "Beaumont",
               "Bel Air",
               "Bellevue",
               "Berkeley",
               "Bethlehem",
               "Billings",
               "Birmingham",
               "Bloomington",
               "Boise",
               "Boise City",
               "Bonita Springs",
               "Boston",
               "Boulder",
               "Bradenton",
               "Bremerton",
               "Bridgeport",
               "Brighton",
               "Brownsville",
               "Bryan",
               "Buffalo",
               "Burbank",
               "Burlington",
               "Cambridge",
               "Canton",
               "Cape Coral",
               "Carrollton",
               "Cary",
               "Cathedral City",
               "Cedar Rapids",
               "Champaign",
               "Chandler",
               "Charleston",
               "Charlotte",
               "Chattanooga",
               "Chesapeake",
               "Chicago",
               "Chula Vista",
               "Cincinnati",
               "Clarke County",
               "Clarksville",
               "Clearwater",
               "Cleveland",
               "College Station",
               "Colorado Springs",
               "Columbia",
               "Columbus",
               "Concord",
               "Coral Springs",
               "Corona",
               "Corpus Christi",
               "Costa Mesa",
               "Dallas",
               "Daly City",
               "Danbury",
               "Davenport",
               "Davidson County",
               "Dayton",
               "Daytona Beach",
               "Deltona",
               "Denton",
               "Denver",
               "Des Moines",
               "Detroit",
               "Downey",
               "Duluth",
               "Durham",
               "El Monte",
               "El Paso",
               "Elizabeth",
               "Elk Grove",
               "Elkhart",
               "Erie",
               "Escondido",
               "Eugene",
               "Evansville",
               "Fairfield",
               "Fargo",
               "Fayetteville",
               "Fitchburg",
               "Flint",
               "Fontana",
               "Fort Collins",
               "Fort Lauderdale",
               "Fort Smith",
               "Fort Walton Beach",
               "Fort Wayne",
               "Fort Worth",
               "Frederick",
               "Fremont",
               "Fresno",
               "Fullerton",
               "Gainesville",
               "Garden Grove",
               "Garland",
               "Gastonia",
               "Gilbert",
               "Glendale",
               "Grand Prairie",
               "Grand Rapids",
               "Grayslake",
               "Green Bay",
               "GreenBay",
               "Greensboro",
               "Greenville",
               "Gulfport-Biloxi",
               "Hagerstown",
               "Hampton",
               "Harlingen",
               "Harrisburg",
               "Hartford",
               "Havre de Grace",
               "Hayward",
               "Hemet",
               "Henderson",
               "Hesperia",
               "Hialeah",
               "Hickory",
               "High Point",
               "Hollywood",
               "Honolulu",
               "Houma",
               "Houston",
               "Howell",
               "Huntington",
               "Huntington Beach",
               "Huntsville",
               "Independence",
               "Indianapolis",
               "Inglewood",
               "Irvine",
               "Irving",
               "Jackson",
               "Jacksonville",
               "Jefferson",
               "Jersey City",
               "Johnson City",
               "Joliet",
               "Kailua",
               "Kalamazoo",
               "Kaneohe",
               "Kansas City",
               "Kennewick",
               "Kenosha",
               "Killeen",
               "Kissimmee",
               "Knoxville",
               "Lacey",
               "Lafayette",
               "Lake Charles",
               "Lakeland",
               "Lakewood",
               "Lancaster",
               "Lansing",
               "Laredo",
               "Las Cruces",
               "Las Vegas",
               "Layton",
               "Leominster",
               "Lewisville",
               "Lexington",
               "Lincoln",
               "Little Rock",
               "Long Beach",
               "Lorain",
               "Los Angeles",
               "Louisville",
               "Lowell",
               "Lubbock",
               "Macon",
               "Madison",
               "Manchester",
               "Marina",
               "Marysville",
               "McAllen",
               "McHenry",
               "Medford",
               "Melbourne",
               "Memphis",
               "Merced",
               "Mesa",
               "Mesquite",
               "Miami",
               "Milwaukee",
               "Minneapolis",
               "Miramar",
               "Mission Viejo",
               "Mobile",
               "Modesto",
               "Monroe",
               "Monterey",
               "Montgomery",
               "Moreno Valley",
               "Murfreesboro",
               "Murrieta",
               "Muskegon",
               "Myrtle Beach",
               "Naperville",
               "Naples",
               "Nashua",
               "Nashville",
               "New Bedford",
               "New Haven",
               "New London",
               "New Orleans",
               "New York",
               "New York City",
               "Newark",
               "Newburgh",
               "Newport News",
               "Norfolk",
               "Normal",
               "Norman",
               "North Charleston",
               "North Las Vegas",
               "North Port",
               "Norwalk",
               "Norwich",
               "Oakland",
               "Ocala",
               "Oceanside",
               "Odessa",
               "Ogden",
               "Oklahoma City",
               "Olathe",
               "Olympia",
               "Omaha",
               "Ontario",
               "Orange",
               "Orem",
               "Orlando",
               "Overland Park",
               "Oxnard",
               "Palm Bay",
               "Palm Springs",
               "Palmdale",
               "Panama City",
               "Pasadena",
               "Paterson",
               "Pembroke Pines",
               "Pensacola",
               "Peoria",
               "Philadelphia",
               "Phoenix",
               "Pittsburgh",
               "Plano",
               "Pomona",
               "Pompano Beach",
               "Port Arthur",
               "Port Orange",
               "Port Saint Lucie",
               "Port St. Lucie",
               "Portland",
               "Portsmouth",
               "Poughkeepsie",
               "Providence",
               "Provo",
               "Pueblo",
               "Punta Gorda",
               "Racine",
               "Raleigh",
               "Rancho Cucamonga",
               "Reading",
               "Redding",
               "Reno",
               "Richland",
               "Richmond",
               "Richmond County",
               "Riverside",
               "Roanoke",
               "Rochester",
               "Rockford",
               "Roseville",
               "Round Lake Beach",
               "Sacramento",
               "Saginaw",
               "Saint Louis",
               "Saint Paul",
               "Saint Petersburg",
               "Salem",
               "Salinas",
               "Salt Lake City",
               "San Antonio",
               "San Bernardino",
               "San Buenaventura",
               "San Diego",
               "San Francisco",
               "San Jose",
               "Santa Ana",
               "Santa Barbara",
               "Santa Clara",
               "Santa Clarita",
               "Santa Cruz",
               "Santa Maria",
               "Santa Rosa",
               "Sarasota",
               "Savannah",
               "Scottsdale",
               "Scranton",
               "Seaside",
               "Seattle",
               "Sebastian",
               "Shreveport",
               "Simi Valley",
               "Sioux City",
               "Sioux Falls",
               "South Bend",
               "South Lyon",
               "Spartanburg",
               "Spokane",
               "Springdale",
               "Springfield",
               "St. Louis",
               "St. Paul",
               "St. Petersburg",
               "Stamford",
               "Sterling Heights",
               "Stockton",
               "Sunnyvale",
               "Syracuse",
               "Tacoma",
               "Tallahassee",
               "Tampa",
               "Temecula",
               "Tempe",
               "Thornton",
               "Thousand Oaks",
               "Toledo",
               "Topeka",
               "Torrance",
               "Trenton",
               "Tucson",
               "Tulsa",
               "Tuscaloosa",
               "Tyler",
               "Utica",
               "Vallejo",
               "Vancouver",
               "Vero Beach",
               "Victorville",
               "Virginia Beach",
               "Visalia",
               "Waco",
               "Warren",
               "Washington",
               "Waterbury",
               "Waterloo",
               "West Covina",
               "West Valley City",
               "Westminster",
               "Wichita",
               "Wilmington",
               "Winston",
               "Winter Haven",
               "Worcester",
               "Yakima",
               "Yonkers",
               "York",
               "Youngstown",
               ]


def fetch_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}".format(
        location, ApiKeys["owm"]
    )
    response = r.get(url)
    data = response.json()
    if "weather" in data:
        w_str = "{}, {}".format(data["weather"][0]["main"], data["weather"][0]["description"])
        temp = round(float(data["main"]["temp"]) - 273, 2)
        return w_str, temp
    return None, None


class Assistant:
    def __init__(self, apikey, asst_id):
        self.assistant = AssistantV2(version="2019-02-16",
                                     iam_apikey=apikey)

        self.assistant_id = asst_id
        self.session = self.assistant.create_session(self.assistant_id).get_result()
        self.session_id = self.session["session_id"]
        self.pass_date = {}
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

        if msg["context"]:
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
            if not location and any([city.lower() in str(message).lower() for city in List_Cities]):
                for city in List_Cities:
                    if city.lower() in str(message).lower():
                        location = city
            if location:
                self.case.location = location
                w_str, temp = fetch_weather(self.case.location)
                if w_str and temp:
                    self.pass_date['weather'] = {'w_str': w_str, 'temp': temp}
                    print("Location is {}".format(self.case.location))
                    print("{}, Temp {}".format(w_str, temp))

        # Print the response returned by the assistant, if it exists
        text_msg = Assistant._get_text_response(msg["output"])
        if text_msg:
            print("Response from Assistant: {}".format(text_msg))

        # Calculate severity score at every interaction
        self.case.severity_score += Assistant._get_score(msg["output"])
        self.write_to_csv()
        print("Message: {}".format(msg))
        if self.is_end_of_chat():
            print("Approaching end of chat")
        return msg

    def write_to_csv(self):
        filename = "casefiles/{}.csv".format(self.case.id)
        with open(filename, "w+") as f:
            writer = csv.writer(f)
            writer.writerow(self.case.__dict__.keys())
            writer.writerow(self.case.__dict__.values())
        return

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
        if "intents" in message and \
                len(message["intents"]) >= 1 and \
                "intent" in message["intents"][0]:
            curr_response_intent = message["intents"][0]["intent"]

            # checking if intent belongs to depression severity maps
            # if yes then calculate the score else move on
            if curr_response_intent in Questionnaire_Score_Map:
                sev_score += Questionnaire_Score_Map[curr_response_intent]
        return sev_score

    def is_end_of_chat(self):
        return self.context and "skills" in self.context and \
               "main skill" in self.context["skills"] and \
               "user_defined" in self.context["skills"]["main skill"] and \
               "EndOfChat" in self.context["skills"]["main skill"]["user_defined"] and \
               self.context["skills"]["main skill"]["user_defined"]["EndOfChat"]

    def _set_entity(self, entity_name, value):
        pass
