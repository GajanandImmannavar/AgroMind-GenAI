
# from fastapi import APIRouter, Request, HTTPException
# import requests

# from app.services.chat_service import ChatService
# from app.services.prediction_service import PredictionService
# from app.utils.database import get_latest_prediction
# from app.config import (
#     WHATSAPP_ACCESS_TOKEN,
#     WHATSAPP_PHONE_NUMBER_ID,
# )

# router = APIRouter()

# # ==========================================
# # Initialize Services
# # ==========================================
# prediction_service = PredictionService()

# # Pass model classes dynamically
# chat_service = ChatService(model_classes=prediction_service.classes)

# # Prevent duplicate webhook messages
# processed_messages = set()


# # =====================================================
# # 🔹 Webhook Verification (Meta Requirement)
# # =====================================================
# @router.get("/webhook")
# async def verify_webhook(request: Request):

#     params = request.query_params

#     if params.get("hub.verify_token") == "agromind_secure_token_123":
#         return int(params.get("hub.challenge"))

#     raise HTTPException(status_code=403, detail="Verification failed")


# # =====================================================
# # 🔹 Receive WhatsApp Messages
# # =====================================================
# @router.post("/webhook")
# async def receive_message(request: Request):

#     data = await request.json()

#     print("Incoming Webhook Data:", data)

#     try:
#         entry = data["entry"][0]
#         changes = entry["changes"][0]
#         value = changes["value"]
#         messages = value.get("messages")

#         if not messages:
#             return {"status": "no message"}

#         message = messages[0]
#         message_id = message["id"]

#         # ==========================================
#         # Prevent duplicate processing
#         # ==========================================
#         if message_id in processed_messages:
#             print("Duplicate message ignored:", message_id)
#             return {"status": "duplicate"}

#         processed_messages.add(message_id)

#         phone_number = message["from"]
#         message_type = message["type"]

#         print("Message Type:", message_type)
#         print("From:", phone_number)

#         # =====================================================
#         # 📷 IMAGE MESSAGE
#         # =====================================================
#         if message_type == "image":

#             media_id = message["image"]["id"]

#             print("Media ID:", media_id)

#             image = prediction_service.download_whatsapp_image(media_id)

#             predicted_class, confidence = prediction_service.predict(image)

#             # 🚨 Invalid Image (not a leaf)
#             if predicted_class is None:

#                 reply = (
#                     "⚠️ The uploaded image does not appear to be a plant leaf.\n\n"
#                     "Please upload a clear close-up photo of a plant leaf "
#                     "for disease diagnosis."
#                 )

#                 send_whatsapp_message(phone_number, reply)

#                 return {"status": "invalid image"}

#             # Run RAG explanation
#             rag_response = chat_service.handle_first_prediction(
#                 phone_number,
#                 predicted_class,
#                 confidence
#             )

#             reply = (
#                 f"🌿 Disease Detected: {predicted_class}\n"
#                 f"Confidence: {confidence}\n\n"
#                 f"{rag_response}\n\n"
#                 "You can now ask more questions about this disease."
#             )

#             send_whatsapp_message(phone_number, reply)

#             return {"status": "image processed"}

#         # =====================================================
#         # 💬 TEXT MESSAGE
#         # =====================================================
#         elif message_type == "text":

#             user_text = message["text"]["body"]

#             print("User Text:", user_text)

#             latest_prediction = get_latest_prediction(phone_number)

#             # If user never uploaded image
#             if not latest_prediction:

#                 if user_text.lower() in ["hi", "hello", "hey", "start"]:
#                     reply = (
#                         "👋 Hello!\n\n"
#                         "Please upload a plant leaf image "
#                         "for disease diagnosis."
#                     )
#                 else:
#                     reply = (
#                         "Please upload a plant leaf image "
#                         "first for disease diagnosis."
#                     )

#                 send_whatsapp_message(phone_number, reply)

#                 return {"status": "waiting for image"}

#             # Run AI chat
#             ai_reply = chat_service.handle_chat(
#                 phone_number,
#                 user_text
#             )

#             send_whatsapp_message(phone_number, ai_reply)

#             return {"status": "text processed"}

#         # =====================================================
#         # ❌ Unsupported Message Type
#         # =====================================================
#         else:

#             send_whatsapp_message(
#                 phone_number,
#                 "Please send a plant leaf image or text message."
#             )

#             return {"status": "unsupported message"}

#     except Exception as e:

#         print("ERROR:", str(e))

#         return {"error": str(e)}


# # =====================================================
# # 🔹 Send Message Back to WhatsApp
# # =====================================================
# def send_whatsapp_message(to, message):

#     print("Sending message to:", to)

#     url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

#     headers = {
#         "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": to,
#         "type": "text",
#         "text": {"body": message[:4096]}
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     print("WhatsApp API Status:", response.status_code)
#     print("WhatsApp API Response:", response.text)

#     return response.json()





from fastapi import APIRouter, Request, HTTPException
import requests

from app.services.chat_service import ChatService
from app.services.prediction_service import PredictionService
from app.utils.database import get_latest_prediction
from app.config import (
    WHATSAPP_ACCESS_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
)

router = APIRouter()

# ==========================================
# Initialize Services
# ==========================================
prediction_service = PredictionService()

# Pass model classes dynamically
chat_service = ChatService(model_classes=prediction_service.classes)

# Prevent duplicate webhook messages
processed_messages = set()


# =====================================================
# 🔹 Webhook Verification (Meta Requirement)
# =====================================================
@router.get("/webhook")
async def verify_webhook(request: Request):

    params = request.query_params

    if params.get("hub.verify_token") == "agromind_secure_token_123":
        return int(params.get("hub.challenge"))

    raise HTTPException(status_code=403, detail="Verification failed")


# =====================================================
# 🔹 Receive WhatsApp Messages
# =====================================================
@router.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    print("Incoming Webhook Data:", data)

    try:

        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages")

        if not messages:
            return {"status": "no message"}

        message = messages[0]
        message_id = message["id"]

        # ==========================================
        # Prevent duplicate processing
        # ==========================================
        if message_id in processed_messages:
            print("Duplicate message ignored:", message_id)
            return {"status": "duplicate"}

        processed_messages.add(message_id)

        phone_number = message["from"]
        message_type = message["type"]

        print("Message Type:", message_type)
        print("From:", phone_number)

        # =====================================================
        # 📷 IMAGE MESSAGE
        # =====================================================
        if message_type == "image":

            media_id = message["image"]["id"]

            print("Media ID:", media_id)

            image = prediction_service.download_whatsapp_image(media_id)

            # ✅ Pass phone_number so prediction gets stored
            predicted_class, confidence = prediction_service.predict(
                image,
                phone_number
            )

            # 🚨 Invalid Image (not a leaf)
            if predicted_class is None:

                reply = (
                    "⚠️ The uploaded image does not appear to be a plant leaf.\n\n"
                    "Please upload a clear close-up photo of a plant leaf "
                    "for disease diagnosis."
                )

                send_whatsapp_message(phone_number, reply)

                return {"status": "invalid image"}

            # Run RAG explanation
            rag_response = chat_service.handle_first_prediction(
                phone_number,
                predicted_class,
                confidence
            )

            reply = (
                f"🌿 Disease Detected: {predicted_class}\n"
                f"Confidence: {confidence}\n\n"
                f"{rag_response}\n\n"
                "You can now ask more questions about this disease."
            )

            send_whatsapp_message(phone_number, reply)

            return {"status": "image processed"}

        # =====================================================
        # 💬 TEXT MESSAGE
        # =====================================================
        elif message_type == "text":

            user_text = message["text"]["body"]

            print("User Text:", user_text)

            latest_prediction = get_latest_prediction(phone_number)

            # If user never uploaded image
            if not latest_prediction:

                if user_text.lower() in ["hi", "hello", "hey", "start"]:

                    reply = (
                        "👋 Hello!\n\n"
                        "Please upload a plant leaf image "
                        "for disease diagnosis."
                    )

                else:

                    reply = (
                        "Please upload a plant leaf image "
                        "first for disease diagnosis."
                    )

                send_whatsapp_message(phone_number, reply)

                return {"status": "waiting for image"}

            # Run AI chat
            ai_reply = chat_service.handle_chat(
                phone_number,
                user_text
            )

            send_whatsapp_message(phone_number, ai_reply)

            return {"status": "text processed"}

        # =====================================================
        # ❌ Unsupported Message Type
        # =====================================================
        else:

            send_whatsapp_message(
                phone_number,
                "Please send a plant leaf image or text message."
            )

            return {"status": "unsupported message"}

    except Exception as e:

        print("ERROR:", str(e))

        return {"error": str(e)}


# =====================================================
# 🔹 Send Message Back to WhatsApp
# =====================================================
def send_whatsapp_message(to, message):

    print("Sending message to:", to)

    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message[:4096]}
    }

    response = requests.post(url, headers=headers, json=payload)

    print("WhatsApp API Status:", response.status_code)
    print("WhatsApp API Response:", response.text)

    return response.json()