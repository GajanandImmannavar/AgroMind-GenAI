import os
import re
from app.utils.question_mapper import map_question_to_section


# =========================================
# NORMALIZE TEXT FOR MATCHING
# =========================================

def normalize_name(text):

    text = text.lower()

    text = text.replace("(", "").replace(")", "")
    text = text.replace(" ", "_").replace("-", "_")

    text = re.sub(r"_+", "_", text)
    text = re.sub(r"[^a-z0-9_]", "", text)

    return text


# =========================================
# FIND MATCHING DOCUMENT
# =========================================

def find_disease_file(predicted_class):

    documents_path = "app/rag/documents"

    normalized_class = normalize_name(predicted_class)

    for file in os.listdir(documents_path):

        file_without_ext = file.replace(".txt", "")
        normalized_file = normalize_name(file_without_ext)

        if normalized_class in normalized_file or normalized_file in normalized_class:
            return os.path.join(documents_path, file)

    return None


# =========================================
# PARSE DOCUMENT SECTIONS
# =========================================

def parse_document(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = {}

    pattern = r"([A-Za-z0-9 ()\-]+):\n(.*?)(?=\n[A-Za-z0-9 ()\-]+?:|\Z)"

    matches = re.findall(pattern, text, re.S)

    for title, content in matches:
        sections[title.strip()] = content.strip()

    return sections


# =========================================
# FORMAT ANSWER
# =========================================

def format_answer(section, content):

    lines = content.split("\n")

    formatted = f"{section}\n\n"

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("-") or line.startswith("•"):
            formatted += f"{line}\n"

        elif line[0].isdigit():
            formatted += f"{line}\n"

        else:
            formatted += f"• {line}\n"

    return formatted


# =========================================
# FIND CLOSEST SECTION MATCH
# =========================================

def find_section(sections, predicted_section):

    predicted_section = predicted_section.lower()

    # -------------------------------------
    # SECTION ALIASES (SAFETY MATCHING)
    # -------------------------------------

    section_alias = {

        "symptoms":[
            "symptoms",
            "signs"
        ],

        "cause":[
            "cause",
            "reason",
            "disease cause"
        ],

        "favorable conditions":[
            "favorable conditions",
            "weather conditions",
            "environment conditions",
            "when does this this occure"
        ],

        "disease spread":[
            "disease spread",
            "how the disease spreads",
            "spread"
        ],

        "steps to make plant healthy":[
            "steps to make plant healthy",
            "treatment",
            "control"
        ],

        "recommended medicine":[
            "recommended fungicides",
            "recommended pesticide",
            "recommended medicine",
            "medicine"
        ],

        "how to apply":[
            "how to apply",
            "spray method",
            "application method",
            "how to apply medicine",
            "how to use medicine"
        ],

        "recovery time":[
            "recovery time",
            "time to recover"
        ],

        "prevention":[
            "prevention",
            "preventive measures"
        ],

        "effect on yield":[
            "effect on yield",
            "yield loss",
            "impact on yield"
        ],

        "cost per acre (approximate)":[
            "cost of treatment (approximate per acre)",
            "treatment cost",
            "cost per acre"
        ],

        "farmer advice":[
            "farmer advice",
            "advice for farmers"
        ],

        "best farming practices":[
            "best farming practices",
            "farming practices",
            "orchard practices"
        ]

    }

    # -------------------------------------
    # CHECK ALIASES
    # -------------------------------------

    for main_section, aliases in section_alias.items():

        if predicted_section == main_section:

            for key in sections.keys():

                key_lower = key.lower()

                for alias in aliases:

                    if alias in key_lower:
                        return key

    # -------------------------------------
    # NORMAL MATCH
    # -------------------------------------

    for key in sections.keys():

        key_lower = key.lower()

        if predicted_section == key_lower:
            return key

        if predicted_section in key_lower:
            return key

        if key_lower in predicted_section:
            return key

    return None

# =========================================
# MAIN RESPONSE FUNCTION
# =========================================

def get_rag_response(predicted_class, question=None):

    file_path = find_disease_file(predicted_class)

    if file_path is None:
        return "Disease information not available."

    sections = parse_document(file_path)

    # -------------------------------------
    # FIRST RESPONSE AFTER IMAGE UPLOAD
    # -------------------------------------

    if question is None:

        section = "Symptoms"

        matched_section = find_section(sections, section)

        if matched_section:

            response = format_answer(matched_section, sections[matched_section])

            response += "\n\nYou can now ask questions like:\n"
            response += "• What causes this disease?\n"
            response += "• What medicine should I spray?\n"
            response += "• How to apply fungicide?\n"
            response += "• How to prevent it?\n"

            return response

        return "Information not available."

    # -------------------------------------
    # USER QUESTION RESPONSE
    # -------------------------------------

    section = map_question_to_section(question)

    if section == "Unknown":
        return (
            "Sorry, I can only answer questions related to this plant disease.\n"
            "Please ask about symptoms, treatment, prevention, cost, etc."
        )

    matched_section = find_section(sections, section)

    if matched_section is None:
        return "Information not available."

    content = sections[matched_section]

    return format_answer(matched_section, content)