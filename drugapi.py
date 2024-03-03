import requests
import json
import os
import urllib.parse
    
def getDrugInteractions(medicine_names):
    interactions = []
    medicine_names_encoded = ""

    for medicine_name in medicine_names[:-1]:
        medicine_names_encoded += urllib.parse.quote(medicine_name + ",")
    medicine_names_encoded += urllib.parse.quote(medicine_names[-1])

    response = requests.get(os.environ["DRUGBANK_API_URL"].format(medicine_names_encoded))
    data = json.loads(response.text)

    if "interactions" not in data.keys():
        return None
    
    results = data["interactions"]
    for result in results:
        if ("severity" in result.keys()) and ("description" in result.keys()):
            interactions.append(result)

    return interactions

def getAdverseReactions(medicine_name):
    reactions = set()

    response = requests.get("https://api.fda.gov/drug/label.json?search=openfda.brand_name:{0}&limit=10".format(medicine_name))
    data = json.loads(response.text)

    if "results" not in data.keys():
        return None
    
    results = data["results"]
    for result in results:
        if "adverse_reactions" in result.keys():
            adverse_reactions = result["adverse_reactions"]
            for adverse_reaction in adverse_reactions:
                reactions.add(adverse_reaction)

    return ''.join(list(reactions))
