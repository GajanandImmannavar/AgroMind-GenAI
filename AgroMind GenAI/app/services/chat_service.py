
# from app.utils.database import (
#     save_user,
#     save_prediction,
#     save_chat,
#     save_feedback,
#     get_chat_history,
#     get_latest_prediction
# )

# from app.rag.rag_pipeline import get_rag_response
# from app.utils.question_mapper import map_question_to_section


# class ChatService:

#     def __init__(self, model_classes=None):

#         # Extract crops dynamically from ML classes
#         self.crops = set()

#         if model_classes:
#             for cls in model_classes:
#                 crop = cls.split("___")[0].lower()
#                 self.crops.add(crop)

#     # -------------------------------------------------
#     # Detect crop name inside user text
#     # -------------------------------------------------
#     def detect_crop(self, text):

#         text = text.lower()

#         for crop in self.crops:
#             if crop in text:
#                 return crop

#         return None

#     # -------------------------------------------------
#     # When image is uploaded
#     # -------------------------------------------------
#     def handle_first_prediction(self, phone_number, predicted_class, confidence=1.0):

#         # Save user if not exists
#         save_user(phone_number)

#         # Save prediction
#         save_prediction(
#             phone_number,
#             "whatsapp_image",
#             predicted_class,
#             confidence
#         )

#         # Get disease description
#         rag_response = get_rag_response(predicted_class)

#         return rag_response

#     # -------------------------------------------------
#     # Chat handler
#     # -------------------------------------------------
#     def handle_chat(self, phone_number, user_message):

#         user_message = user_message.strip().lower()

#         # --------------------------------
#         # FEEDBACK DETECTION
#         # --------------------------------
#         if user_message in ["1", "yes"]:
#             save_feedback(phone_number, "good")
#             return "✅ Thanks for your feedback!"

#         if user_message in ["2", "no"]:
#             save_feedback(phone_number, "bad")
#             return "Thanks! We will improve the answer."

#         # --------------------------------
#         # Get latest disease prediction
#         # --------------------------------
#         predicted_class = get_latest_prediction(phone_number)

#         if not predicted_class:
#             return "Please upload a plant leaf image first for disease diagnosis."

#         # --------------------------------
#         # Detect question intent
#         # --------------------------------
#         predicted_section = map_question_to_section(user_message)

#         # --------------------------------
#         # Get answer from knowledge system
#         # --------------------------------
#         answer = get_rag_response(predicted_class, user_message)

#         # --------------------------------
#         # Save chat history
#         # --------------------------------
#         save_chat(
#             phone_number,
#             predicted_class,
#             predicted_section,
#             user_message,
#             answer
#         )

#         # --------------------------------
#         # Ask feedback every 5 questions
#         # --------------------------------
#         history = get_chat_history(phone_number)

#         if len(history) % 5 == 0:
#             answer += "\n\nWas this answer helpful?\n1️⃣ Yes\n2️⃣ No"

#         return answer


from app.utils.database import (
    save_user,
    save_prediction,
    save_chat,
    save_feedback,
    get_chat_count,
    get_latest_prediction
)

from app.rag.rag_pipeline import get_rag_response
from app.utils.question_mapper import map_question_to_section


class ChatService:

    def __init__(self, model_classes=None):

        self.crops = set()

        # Track feedback state
        self.awaiting_feedback = {}

        if model_classes:
            for cls in model_classes:
                crop = cls.split("___")[0].lower()
                self.crops.add(crop)

    # -------------------------------------------------
    # Detect crop name inside user text
    # -------------------------------------------------
    def detect_crop(self, text):

        text = text.lower()

        for crop in self.crops:
            if crop in text:
                return crop

        return None

    # -------------------------------------------------
    # When image is uploaded
    # -------------------------------------------------
    def handle_first_prediction(self, phone_number, predicted_class, confidence=1.0):

        save_user(phone_number)

        save_prediction(
            phone_number,
            "whatsapp_image",
            predicted_class,
            confidence
        )

        rag_response = get_rag_response(predicted_class)

        return rag_response

    # -------------------------------------------------
    # Chat handler
    # -------------------------------------------------
    def handle_chat(self, phone_number, user_message):

        msg = user_message.strip().lower()

        # --------------------------------
        # FEEDBACK DETECTION
        # --------------------------------
        if self.awaiting_feedback.get(phone_number):

            if msg.startswith("1") or msg.startswith("yes"):

                comment = msg[1:].strip() if msg.startswith("1") else msg.replace("yes","").strip()

                save_feedback(phone_number, "good", comment)

                self.awaiting_feedback[phone_number] = False

                return "✅ Thanks for your feedback!"

            if msg.startswith("2") or msg.startswith("no"):

                comment = msg[1:].strip() if msg.startswith("2") else msg.replace("no","").strip()

                save_feedback(phone_number, "bad", comment)

                self.awaiting_feedback[phone_number] = False

                return "Thanks! We will improve the answer."

        # --------------------------------
        # Get latest disease prediction
        # --------------------------------
        predicted_class = get_latest_prediction(phone_number)

        if not predicted_class:
            return "Please upload a plant leaf image first for disease diagnosis."

        # --------------------------------
        # Detect intent
        # --------------------------------
        predicted_section = map_question_to_section(msg)

        # --------------------------------
        # Get RAG answer
        # --------------------------------
        answer = get_rag_response(predicted_class, msg)

        # --------------------------------
        # Save chat
        # --------------------------------
        save_chat(
            phone_number,
            predicted_class,
            predicted_section,
            msg,
            answer
        )

        # --------------------------------
        # Ask feedback every 5 questions
        # --------------------------------
        chat_count = get_chat_count(phone_number)

        if chat_count % 5 == 0:

            self.awaiting_feedback[phone_number] = True

            answer += "\n\nWas this answer helpful?\n1️⃣ Yes\n2️⃣ No"

        return answer