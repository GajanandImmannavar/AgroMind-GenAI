# import torch
# import torch.nn.functional as F
# from PIL import Image

# from app.models.multimodal_model import MultimodalCropModel
# from app.data.preprocessing import get_val_transform
# from app.data.dataset_loader import create_dataloaders
# from app.rag.rag_pipeline import get_rag_response
# from app.rag.chat_engine import AgroChatEngine


# # ==============================
# # 🔹 Load Trained Model
# # ==============================
# def load_model(model_path, num_classes, device):
#     model = MultimodalCropModel(num_classes).to(device)
#     model.load_state_dict(torch.load(model_path, map_location=device))
#     model.eval()
#     return model


# # ==============================
# # 🔹 Predict Image + RAG
# # ==============================
# def predict_image(
#     image_path,
#     model,
#     classes,
#     device,
#     image_size=224,
#     confidence_threshold=0.6
# ):

#     image = Image.open(image_path).convert("RGB")
#     transform = get_val_transform(image_size)
#     image = transform(image).unsqueeze(0).to(device)

#     # Dummy weather input (replace later with real API data)
#     weather = torch.tensor([[30.0, 70.0, 5.0]], dtype=torch.float32).to(device)

#     with torch.no_grad():
#         outputs = model(image, weather)
#         probs = F.softmax(outputs, dim=1)
#         confidence, predicted = torch.max(probs, dim=1)

#     confidence = confidence.item()
#     predicted_class = classes[predicted.item()]

#     if confidence < confidence_threshold:
#         return {
#             "status": "rejected",
#             "message": "Low confidence. Possibly not a valid plant leaf image.",
#             "confidence": round(confidence, 4)
#         }

#     # 🔥 First RAG explanation
#     try:
#         rag_answer = get_rag_response(predicted_class)
#     except Exception as e:
#         rag_answer = f"RAG system error: {str(e)}"

#     return {
#         "status": "success",
#         "predicted_class": predicted_class,
#         "confidence": round(confidence, 4),
#         "rag_response": rag_answer
#     }


# # ==============================
# # 🔹 Start Conversational Chat
# # ==============================
# def start_chat(predicted_class):
#     print("\n🌿 AgroMind AI Chat Started (type 'exit' to stop)\n")

#     chat_engine = AgroChatEngine(predicted_class)

#     while True:
#         user_input = input("Farmer: ")

#         if user_input.lower() == "exit":
#             print("AgroMind AI: Stay safe! 🌱")
#             break

#         reply = chat_engine.ask(user_input)
#         print("AgroMind AI:", reply)


# # ==============================
# # 🔹 Run Standalone
# # ==============================
# if __name__ == "__main__":

#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print("Using device:", device)

#     dataset_path = r"C:\Users\ADMIN\Desktop\AgroMind GenAI\app\dataset\train"

#     _, _, classes = create_dataloaders(
#         dataset_path=dataset_path,
#         batch_size=1,
#         image_size=224,
#         num_workers=0
#     )

#     model = load_model(
#         model_path="app/models/best_agri_model.pth",
#         num_classes=len(classes),
#         device=device
#     )

#     image_path = r"app/dataset/test.JPG"

#     result = predict_image(
#         image_path=image_path,
#         model=model,
#         classes=classes,
#         device=device
#     )

#     print("\n==============================")
#     print("🔍 Final Prediction Result")
#     print("==============================")
#     print(result)

#     # 🔥 If success → start conversational AI
#     if result["status"] == "success":
#         start_chat(result["predicted_class"])


import torch
import torch.nn.functional as F
from PIL import Image

from app.models.multimodal_model import MultimodalCropModel
from app.data.preprocessing import get_val_transform
from app.data.dataset_loader import create_dataloaders
from app.rag.rag_pipeline import get_rag_response
from app.rag.chat_engine import AgroChatEngine


# ==============================
# 🔹 Load Trained Model
# ==============================
def load_model(model_path, num_classes, device):
    model = MultimodalCropModel(num_classes).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model


# ==============================
# 🔹 Predict Image + RAG
# ==============================
def predict_image(
    image_path,
    model,
    classes,
    device,
    image_size=224,
    confidence_threshold=0.6
):

    image = Image.open(image_path).convert("RGB")
    transform = get_val_transform(image_size)
    image = transform(image).unsqueeze(0).to(device)

    # Dummy weather input (replace later with real API data)
    weather = torch.tensor([[30.0, 70.0, 5.0]], dtype=torch.float32).to(device)

    with torch.no_grad():
        outputs = model(image, weather)
        probs = F.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, dim=1)

    confidence = confidence.item()
    predicted_class = classes[predicted.item()]

    if confidence < confidence_threshold:
        return {
            "status": "rejected",
            "message": "Low confidence. Possibly not a valid plant leaf image.",
            "confidence": round(confidence, 4)
        }

    # 🔥 First RAG explanation
    try:
        # UPDATED: get_rag_response now requires a question argument
        rag_answer = get_rag_response(
            predicted_class,
            "give details about this disease"   # UPDATED
        )
    except Exception as e:
        rag_answer = f"RAG system error: {str(e)}"

    return {
        "status": "success",
        "predicted_class": predicted_class,
        "confidence": round(confidence, 4),
        "rag_response": rag_answer
    }


# ==============================
# 🔹 Start Conversational Chat
# ==============================
def start_chat(predicted_class):

    print("\n🌿 AgroMind AI Chat Started (type 'exit' to stop)\n")

    chat_engine = AgroChatEngine(predicted_class)

    while True:

        user_input = input("Farmer: ")

        if user_input.lower() == "exit":
            print("AgroMind AI: Stay safe! 🌱")
            break

        reply = chat_engine.ask(user_input)

        print("AgroMind AI:", reply)


# ==============================
# 🔹 Run Standalone
# ==============================
if __name__ == "__main__":

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    dataset_path = r"C:\Users\ADMIN\Desktop\AgroMind GenAI\app\dataset\train"

    _, _, classes = create_dataloaders(
        dataset_path=dataset_path,
        batch_size=1,
        image_size=224,
        num_workers=0
    )

    model = load_model(
        model_path="app/models/best_agri_model.pth",
        num_classes=len(classes),
        device=device
    )

    image_path = r"app/dataset/test.JPG"

    result = predict_image(
        image_path=image_path,
        model=model,
        classes=classes,
        device=device
    )

    print("\n==============================")
    print("🔍 Final Prediction Result")
    print("==============================")
    print(result)

    # 🔥 If success → start conversational AI
    if result["status"] == "success":
        start_chat(result["predicted_class"])