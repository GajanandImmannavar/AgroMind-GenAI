import json
import os


def load_knowledge():
    file_path = os.path.join("app", "utils", "knowledge.json")

    with open(file_path, "r", encoding="utf-8") as f:
        knowledge = json.load(f)

    return knowledge


def get_disease_info(predicted_class):
    knowledge = load_knowledge()

    return knowledge.get(
        predicted_class,
        {
            "description": "No information available.",
            "cause": "Unknown",
            "symptoms": "Unknown",
            "treatment": "Consult agricultural expert.",
            "prevention": "Follow general plant care practices."
        }
    )