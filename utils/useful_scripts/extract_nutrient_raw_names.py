import json
import pprint


def extract_nutrient_raw_names():
    stop_sections =[
        "We suggest this product provides",
        "Reference Intake",
        "This pack contains approx",
        "contains",
        "This jar contains",
        "The mineral content",
        "Servings per",
        "Serves",
        "RI ",
        "Portions should be adjusted",
        "Portions per",
        "Number of serving",
        "Each pack contains",
        "Contains approximately",
        "Contains",
        "A serving of",
        "Salt content",
        "as prepared to Vegan",
        "NRV",
        "Method of analysis ",
        "analysis",
        "We suggest"


    ]
    data = []
    with open(
            "./data/optimization_data/name raw.json",
            encoding='utf-8'
            ) as json_file:
        file_data = json.load(json_file)
        for item in file_data:
            for name in item["nutrients"]:
                nope = False

                for stop in stop_sections:
                    if stop in name["name_raw"]:
                        nope = True

                if not nope:
                    data.append(str(name["name_raw"]).strip())

    print(len(data))

    sett = set(data)
    pprint.pprint(sett)

    pprint.pprint(len(sett))

