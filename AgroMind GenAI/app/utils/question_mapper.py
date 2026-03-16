import re
import difflib
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================================
# NORMALIZE FARMER LANGUAGE
# =========================================

def normalize_farmer_language(text):

    replacements = {
        "got": "has",
        "leaf": "leaves",
        "fruit": "fruits",
        "spray": "apply",
        "medicine": "fungicide",
        "chemical": "fungicide",
        "disease cure": "treatment",
        "plant sick": "plant disease"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


# =========================================
# SYNONYM NORMALIZATION
# =========================================

def normalize_synonyms(text):

    synonyms = {
        "use": "apply",
        "using": "apply",
        "drug": "medicine",
        "chemical": "medicine"
    }

    for k, v in synonyms.items():
        text = text.replace(k, v)

    return text


# =========================================
# SINGLE WORD MAP
# =========================================

single_word_map = {

    "medicine": "Recommended Medicine",
    "fungicide": "Recommended Medicine",
    "pesticide": "Recommended Medicine",
    "chemical": "Recommended Medicine",

    "cost": "Cost per Acre (Approximate)",
    "price": "Cost per Acre (Approximate)",
    "expense": "Cost per Acre (Approximate)",

    "symptom": "Symptoms",
    "symptoms": "Symptoms",
    "sign": "Symptoms",
    "signs": "Symptoms",

    "cause": "Cause",
    "reason": "Cause",

    "spread": "Disease Spread",

    "weather": "Favorable Conditions",
    "climate": "Favorable Conditions",

    "treatment": "Steps to Make Plant Healthy",
    "control": "Steps to Make Plant Healthy",

    "prevention": "Prevention",

    "yield": "Effect on Yield",

    "advice": "Farmer Advice",

    "practice": "Best Farming Practices",

    "damage": "Affected Plant Parts",
    "damaged": "Affected Plant Parts",
    "parts": "Affected Plant Parts"
}


# =========================================
# SHORTCUT PHRASES
# =========================================

shortcut_map = {

    "best practice": "Best Farming Practices",
    "best practices": "Best Farming Practices",

    "what should farmers do": "Steps to Make Plant Healthy",
    "what to do": "Steps to Make Plant Healthy",

    "make plant healthy": "Steps to Make Plant Healthy",

    "spray method": "How to Apply",
    "spraying method": "How to Apply",

    "tell me about this disease": "Description",
    "what is this disease": "Description",
    "explain this disease": "Description"
}


# =========================================
# SPELLING WORD LIST
# =========================================

valid_words = list(single_word_map.keys()) + [
    "apply","use","spray","fungicide","pesticide",
    "treat","treatment","control","manage","cure",
    "prevent","prevention","symptom","symptoms",
    "cause","spread","weather","climate","yield",
    "cost","price","expense","advice","practice"
]


# =========================================
# SPELLING CORRECTION
# =========================================

def correct_spelling(text):

    words = text.split()
    corrected = []

    for w in words:

        matches = difflib.get_close_matches(w, valid_words, n=1, cutoff=0.75)

        if matches:
            corrected.append(matches[0])
        else:
            corrected.append(w)

    return " ".join(corrected)


# =========================================
# INTENTS
# =========================================

intents = {

"Description":{
"keywords":[
"about","description","information","explain","detail",
"disease","tell","meaning","define","overview"
],
"examples":[
"tell me about this disease",
"what is this disease",
"explain this disease",
"give details about disease",
"information about this plant disease",
"what is this plant problem",
"tell me about the infection",
"overview of this disease"
]
},

"Symptoms":{
"keywords":[
"symptom","symptoms","sign","signs","spot","spots",
"patch","lesion","mark","appearance","identify","visible"
],
"examples":[
"what are the symptoms",
"how to identify the disease",
"what signs appear on leaves",
"what does the disease look like",
"how can i recognize the disease",
"what marks appear on plant",
"how to detect infection",
"what symptoms appear on crop"
]
},

"Affected Plant Parts":{
"keywords":[
"affected","damage","damaged","parts","leaf","leaves",
"fruit","fruits","stem","root","branch","flower"
],
"examples":[
"which parts of plant are affected",
"which parts get damaged",
"what plant parts are infected",
"does it affect leaves or fruits",
"which plant area gets disease",
"what part of plant is attacked"
]
},

"Cause":{
"keywords":[
"cause","reason","why","fungus","bacteria","virus",
"infection","pathogen","organism"
],
"examples":[
"what causes this disease",
"why does infection occur",
"organism responsible for disease",
"is it fungal or bacterial",
"why plants get this infection"
]
},

"Favorable Conditions":{
"keywords":[
"weather","climate","humidity","temperature","rain",
"moisture","season","occur","increase","wet"
],
"examples":[
"weather conditions for disease",
"when does disease occur",
"when does infection increase",
"what weather causes disease",
"which climate favors disease"
]
},

"Disease Spread":{
"keywords":[
"spread","transfer","transmission","carry","move"
],
"examples":[
"how disease spreads",
"how infection transfers",
"can wind carry disease",
"does rain spread disease",
"how infection moves"
]
},

"Steps to Make Plant Healthy":{
"keywords":[
"treat","treatment","control","manage","cure","solution",
"fix","recover"
],
"examples":[
"how to treat disease",
"how to manage infection",
"how to cure plant disease",
"how to control the disease",
"what should i do to cure plant"
]
},

"Recommended Medicine":{
"keywords":[
"medicine","fungicide","pesticide","chemical","spray",
"product"
],
"examples":[
"which fungicide should be used",
"recommended pesticide",
"best chemical for disease",
"which medicine to use",
"what should i spray"
]
},

"How to Apply":{
"keywords":[
"apply","use","spray","method","mix","dose"
],
"examples":[
"how to apply fungicide",
"how to use pesticide",
"spraying method",
"how to mix fungicide",
"how to use medicine"
]
},

"Recovery Time":{
"keywords":[
"recover","recovery","time","days","weeks","duration"
],
"examples":[
"how long to recover",
"recovery time",
"when plant becomes healthy",
"how many days to recover"
]
},

"Prevention":{
"keywords":[
"prevent","avoid","protect","stop"
],
"examples":[
"how to prevent disease",
"ways to avoid infection",
"how to protect plants",
"how to stop disease"
]
},

"Effect on Yield":{
"keywords":[
"yield","production","harvest","loss","reduce"
],
"examples":[
"does disease reduce yield",
"impact on crop production",
"harvest loss",
"how much yield loss occurs"
]
},

"Cost per Acre (Approximate)":{
"keywords":[
"cost","expense","price","money","budget"
],
"examples":[
"treatment cost per acre",
"spray cost",
"how much money needed",
"cost of treatment"
]
},

"Farmer Advice":{
"keywords":[
"advice","tip","suggestion","guidance"
],
"examples":[
"advice for farmers",
"tips for growers",
"suggestions to manage disease",
"what farmers should do"
]
},

"Best Farming Practices":{
"keywords":[
"practice","management","orchard","cultivation"
],
"examples":[
"best farming practices",
"orchard management practices",
"good cultivation practices",
"best agriculture practices"
]
}

}


# =========================================
# EMBEDDINGS
# =========================================

intent_embeddings = {
section:model.encode(data["examples"],convert_to_tensor=True)
for section,data in intents.items()
}


# =========================================
# MAIN FUNCTION
# =========================================

def map_question_to_section(question):

    q = question.lower()
    q = re.sub(r"[^\w\s]","",q).strip()

    q = correct_spelling(q)
    q = normalize_farmer_language(q)
    q = normalize_synonyms(q)

    words = q.split()

    for w in words:
        if w in single_word_map:
            return single_word_map[w]

    for phrase,section in shortcut_map.items():
        if phrase in q:
            return section

    question_embedding = model.encode(q,convert_to_tensor=True)

    best_section = "Unknown"
    best_score = 0

    for section,data in intents.items():

        score = 0

        for k in data["keywords"]:
            if k in q:
                score += 3

        similarity = util.cos_sim(
            question_embedding,
            intent_embeddings[section]
        ).max().item()

        score += similarity * 5

        if score > best_score:
            best_score = score
            best_section = section

    if best_score < 1.8:
        return "Unknown"

    return best_section





# import re
# import difflib
# from sentence_transformers import SentenceTransformer, util


# # =========================================
# # LOAD MULTILINGUAL MODEL
# # =========================================

# model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# # =========================================
# # SPELLING DICTIONARY
# # =========================================

# valid_words = [
# "symptoms","symptom","cause","spread","weather","climate","treatment",
# "medicine","fungicide","pesticide","spray","apply","dose","mix",
# "prevention","prevent","yield","loss","cost","price","advice",
# "practice","occur","happen","start","begin","increase","appear",
# "recover","recovery","time","parts","leaf","leaves","fruit","stem"
# ]


# # =========================================
# # SPELLING CORRECTION
# # =========================================

# def correct_spelling(text):

#     words = text.split()
#     corrected_words = []

#     for w in words:

#         matches = difflib.get_close_matches(w, valid_words, n=1, cutoff=0.75)

#         if matches:
#             corrected_words.append(matches[0])
#         else:
#             corrected_words.append(w)

#     return " ".join(corrected_words)


# # =========================================
# # INTENTS WITH MANY EXAMPLES
# # =========================================

# intents = {

# "Description":[
# "tell me about this disease",
# "what is this disease",
# "explain this disease",
# "information about disease",
# "what plant problem is this",
# "describe this plant disease",
# "details about this infection",
# "what does this disease mean"
# ],


# "Symptoms":[
# "what are the symptoms",
# "symptoms of this disease",
# "how to identify disease",
# "what signs appear on leaves",
# "how plant looks when infected",
# "what damage appears on plant",
# "how to detect infection",
# "what spots appear on leaves",
# "why leaves have spots"
# ],


# "Affected Plant Parts":[
# "which parts of plant affected",
# "which part of plant damaged",
# "does it affect leaves",
# "which plant part gets infection",
# "what parts are infected",
# "are fruits affected",
# "does disease damage stem"
# ],


# "Cause":[
# "what causes this disease",
# "why disease occurs",
# "why infection happens",
# "what organism causes disease",
# "is it fungal disease",
# "reason for plant disease",
# "how disease starts"
# ],


# "Favorable Conditions":[
# "when does disease occur",
# "when infection starts",
# "when problem happens",
# "which weather causes disease",
# "what climate favors infection",
# "when disease appears",
# "when infection increases",
# "what season disease spreads"
# ],


# "Disease Spread":[
# "how disease spreads",
# "how infection spreads",
# "how disease transfers",
# "can wind spread disease",
# "does rain spread infection",
# "how disease moves between plants"
# ],


# "Steps to Make Plant Healthy":[
# "how to treat disease",
# "how to cure plant disease",
# "how to manage infection",
# "how to control disease",
# "what should farmers do",
# "how to fix plant problem",
# "how to remove infection"
# ],


# "Recommended Medicine":[
# "which medicine should be used",
# "recommended fungicide",
# "best pesticide for disease",
# "what chemical to spray",
# "which fungicide works best",
# "medicine for plant disease"
# ],


# "How to Apply":[
# "how to apply fungicide",
# "how to spray pesticide",
# "spray method",
# "how to mix fungicide",
# "what dose to apply",
# "how to prepare spray solution",
# "how to use medicine",
# "how to use  medicine"
# ],


# "Recovery Time":[
# "how long to recover",
# "recovery time of plant",
# "how many days plant recovers",
# "when plant becomes healthy",
# "how fast plant heals"
# ],


# "Prevention":[
# "how to prevent disease",
# "ways to avoid infection",
# "how to protect plants",
# "how to stop disease",
# "precautions for disease"
# ],


# "Effect on Yield":[
# "does disease reduce yield",
# "impact on crop production",
# "how much yield loss",
# "does disease affect harvest",
# "crop production loss"
# ],


# "Cost per Acre (Approximate)":[
# "treatment cost per acre",
# "spray cost",
# "how much money needed",
# "cost of disease control",
# "expense for treatment"
# ],


# "Farmer Advice":[
# "advice for farmers",
# "tips for growers",
# "suggestions for farmers",
# "expert advice for crop disease"
# ],


# "Best Farming Practices":[
# "best farming practices",
# "good cultivation practices",
# "how to maintain healthy crop",
# "best agriculture practices",
# "crop management practices"
# ]

# }


# # =========================================
# # CREATE INTENT EMBEDDINGS
# # =========================================

# intent_embeddings = {
# intent: model.encode(examples, convert_to_tensor=True)
# for intent, examples in intents.items()
# }


# # =========================================
# # MAIN INTENT DETECTION
# # =========================================

# def map_question_to_section(question):

#     q = question.lower()
#     q = re.sub(r"[^\w\s]", "", q).strip()

#     # spelling correction
#     q = correct_spelling(q)

#     question_embedding = model.encode(q, convert_to_tensor=True)

#     best_intent = "Unknown"
#     best_score = 0

#     for intent, embeddings in intent_embeddings.items():

#         similarity = util.cos_sim(question_embedding, embeddings).max().item()

#         if similarity > best_score:
#             best_score = similarity
#             best_intent = intent

#     if best_score < 0.35:
#         return "Unknown"

#     return best_intent