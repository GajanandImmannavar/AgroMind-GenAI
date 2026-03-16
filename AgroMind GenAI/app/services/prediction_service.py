# # import torch
# # import requests
# # from PIL import Image
# # from io import BytesIO
# # import os

# # from app.models.multimodal_model import MultimodalCropModel
# # from app.data.preprocessing import get_val_transform
# # from app.data.dataset_loader import create_dataloaders
# # from app.config import WHATSAPP_ACCESS_TOKEN


# # class PredictionService:

# #     def __init__(self):
# #         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# #         dataset_path = r"app/dataset/train"

# #         _, _, self.classes = create_dataloaders(
# #             dataset_path=dataset_path,
# #             batch_size=1,
# #             image_size=224,
# #             num_workers=0
# #         )

# #         self.model = MultimodalCropModel(len(self.classes)).to(self.device)
# #         self.model.load_state_dict(
# #             torch.load("app/models/best_agri_model.pth", map_location=self.device)
# #         )
# #         self.model.eval()

# #         self.transform = get_val_transform(224)

# #     # =========================
# #     # 🔹 Download Image From WhatsApp
# #     # =========================
# #     def download_whatsapp_image(self, media_id):

# #         # Step 1: Get media URL
# #         url = f"https://graph.facebook.com/v19.0/{media_id}"

# #         headers = {
# #             "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
# #         }

# #         response = requests.get(url, headers=headers)
# #         media_url = response.json()["url"]

# #         # Step 2: Download actual image
# #         image_response = requests.get(media_url, headers=headers)

# #         return Image.open(BytesIO(image_response.content)).convert("RGB")

# #     # =========================
# #     # 🔹 Predict Disease
# #     # =========================
# #     def predict(self, image):

# #         image_tensor = self.transform(image).unsqueeze(0).to(self.device)

# #         weather = torch.tensor([[30.0, 70.0, 5.0]], dtype=torch.float32).to(self.device)

# #         with torch.no_grad():
# #             outputs = self.model(image_tensor, weather)
# #             probs = torch.nn.functional.softmax(outputs, dim=1)
# #             confidence, predicted = torch.max(probs, dim=1)

# #         predicted_class = self.classes[predicted.item()]
# #         confidence = round(confidence.item(), 4)

# #         return predicted_class, confidence


# # updated

# # import torch
# # import requests
# # from PIL import Image
# # from io import BytesIO

# # from app.models.multimodal_model import MultimodalCropModel
# # from app.data.preprocessing import get_val_transform
# # from app.data.dataset_loader import create_dataloaders
# # from app.config import WHATSAPP_ACCESS_TOKEN

# # from app.utils.database import get_latest_prediction


# # class PredictionService:

# #     def __init__(self):

# #         self.device = torch.device(
# #             "cuda" if torch.cuda.is_available() else "cpu"
# #         )

# #         dataset_path = r"app/dataset/train"

# #         _, _, self.classes = create_dataloaders(
# #             dataset_path=dataset_path,
# #             batch_size=1,
# #             image_size=224,
# #             num_workers=0
# #         )

# #         print("Detected Classes:", self.classes)
# #         print("Total Classes:", len(self.classes))

# #         self.model = MultimodalCropModel(len(self.classes)).to(self.device)

# #         self.model.load_state_dict(
# #             torch.load(
# #                 "app/models/best_agri_model.pth",
# #                 map_location=self.device
# #             )
# #         )

# #         self.model.eval()

# #         self.transform = get_val_transform(224)

# #     # ====================================
# #     # 🔹 Download Image From WhatsApp
# #     # ====================================
# #     def download_whatsapp_image(self, media_id):

# #         url = f"https://graph.facebook.com/v19.0/{media_id}"

# #         headers = {
# #             "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
# #         }

# #         response = requests.get(url, headers=headers)

# #         media_url = response.json()["url"]

# #         image_response = requests.get(media_url, headers=headers)

# #         image = Image.open(
# #             BytesIO(image_response.content)
# #         ).convert("RGB")

# #         return image

# #     # ====================================
# #     # 🔹 Predict Disease
# #     # ====================================
# #     def predict(self, image):

# #         image_tensor = self.transform(image).unsqueeze(0).to(self.device)

# #         # Dummy weather input
# #         weather = torch.tensor(
# #             [[30.0, 70.0, 5.0]],
# #             dtype=torch.float32
# #         ).to(self.device)

# #         with torch.no_grad():

# #             outputs = self.model(image_tensor, weather)

# #             probs = torch.nn.functional.softmax(outputs, dim=1)

# #             confidence, predicted = torch.max(probs, dim=1)

# #         predicted_class = self.classes[predicted.item()]

# #         confidence = round(confidence.item(), 4)

# #         return predicted_class, confidence

# #     # ====================================
# #     # 🔹 Get Latest Prediction (for chat)
# #     # ====================================
# #     def get_latest_prediction(self, phone_number):

# #         return get_latest_prediction(phone_number)

# # confidence 

# import torch
# import requests
# from PIL import Image
# from io import BytesIO
# import open_clip

# from app.models.multimodal_model import MultimodalCropModel
# from app.data.preprocessing import get_val_transform
# from app.data.dataset_loader import create_dataloaders
# from app.config import WHATSAPP_ACCESS_TOKEN
# from app.utils.database import get_latest_prediction


# class PredictionService:

#     def __init__(self):

#         self.device = torch.device(
#             "cuda" if torch.cuda.is_available() else "cpu"
#         )

#         # =====================================
#         # CLIP Leaf Detector
#         # =====================================
#         print("Loading CLIP leaf detector...")

#         self.clip_model, _, self.clip_preprocess = open_clip.create_model_and_transforms(
#             "ViT-B-32",
#             pretrained="openai"
#         )

#         self.clip_model = self.clip_model.to(self.device)

#         self.tokenizer = open_clip.get_tokenizer("ViT-B-32")

#         # Leaf prompts
#         self.leaf_prompts = [
#             "a photo of a plant leaf",
#             "a green leaf with veins",
#             "a crop leaf",
#             "a diseased plant leaf",
#             "a close-up of a leaf on a plant"
#         ]

#         # Non-leaf prompts
#         self.non_leaf_prompts = [
#             "a mountain landscape",
#             "a river and sky",
#             "a lake with water",
#             "a waterfall",
#             "a hill with trees",
#             "a forest landscape",
#             "a road in nature",
#             "a city street",
#             "a person selfie",
#             "a human face",
#             "a building",
#             "a car",
#             "fabric texture",
#             "a patterned cloth",
#             "a carpet",
#             "a blanket",
#             "a random indoor object",
#             "a table surface"
#         ]

#         # =====================================
#         # Load Disease Model
#         # =====================================
#         dataset_path = r"app/dataset/train"

#         _, _, self.classes = create_dataloaders(
#             dataset_path=dataset_path,
#             batch_size=1,
#             image_size=224,
#             num_workers=0
#         )

#         print("Detected Classes:", self.classes)
#         print("Total Classes:", len(self.classes))

#         self.model = MultimodalCropModel(len(self.classes)).to(self.device)

#         self.model.load_state_dict(
#             torch.load(
#                 "app/models/best_agri_model.pth",
#                 map_location=self.device
#             )
#         )

#         self.model.eval()

#         self.transform = get_val_transform(224)

#     # =====================================================
#     # Download Image From WhatsApp
#     # =====================================================
#     def download_whatsapp_image(self, media_id):

#         url = f"https://graph.facebook.com/v19.0/{media_id}"

#         headers = {
#             "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
#         }

#         response = requests.get(url, headers=headers)

#         media_url = response.json()["url"]

#         image_response = requests.get(media_url, headers=headers)

#         image = Image.open(BytesIO(image_response.content)).convert("RGB")

#         return image

#     # =====================================================
#     # CLIP Leaf Detection
#     # =====================================================
#     def is_leaf_image(self, image):

#         image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)

#         prompts = self.leaf_prompts + self.non_leaf_prompts

#         text_tokens = self.tokenizer(prompts).to(self.device)

#         with torch.no_grad():

#             image_features = self.clip_model.encode_image(image_input)
#             text_features = self.clip_model.encode_text(text_tokens)

#             image_features /= image_features.norm(dim=-1, keepdim=True)
#             text_features /= text_features.norm(dim=-1, keepdim=True)

#             similarity = (image_features @ text_features.T).softmax(dim=-1)

#         probs = similarity[0].cpu().numpy()

#         best_idx = probs.argmax()
#         best_prompt = prompts[best_idx]

#         leaf_scores = probs[:len(self.leaf_prompts)]
#         non_leaf_scores = probs[len(self.leaf_prompts):]

#         best_leaf = leaf_scores.max()
#         best_non_leaf = non_leaf_scores.max()

#         print("CLIP Prediction:", best_prompt)
#         print("Leaf score:", best_leaf)
#         print("Non-leaf score:", best_non_leaf)

#         # 🚨 If best prediction belongs to NON-LEAF → reject
#         if best_idx >= len(self.leaf_prompts):

#             print("Rejected: Non-leaf image detected")

#             return False

#         return True

#     # =====================================================
#     # Disease Prediction
#     # =====================================================
#     def predict(self, image):

#         # Step 1: Check if image is leaf
#         if not self.is_leaf_image(image):

#             print("Rejected: Not a plant leaf")

#             return None, 0.0

#         # Step 2: Run disease model
#         image_tensor = self.transform(image).unsqueeze(0).to(self.device)

#         weather = torch.tensor(
#             [[30.0, 70.0, 5.0]],
#             dtype=torch.float32
#         ).to(self.device)

#         with torch.no_grad():

#             outputs = self.model(image_tensor, weather)

#             probs = torch.nn.functional.softmax(outputs, dim=1)

#             confidence, predicted = torch.max(probs, dim=1)

#         predicted_class = self.classes[predicted.item()]
#         confidence = round(confidence.item(), 4)

#         print("Predicted Class:", predicted_class)
#         print("Confidence:", confidence)

#         # Safety filter
#         if confidence < 0.60:

#             print("Low confidence — likely incorrect image")

#             return None, confidence

#         return predicted_class, confidence

#     # =====================================================
#     # Get Latest Prediction
#     # =====================================================
#     def get_latest_prediction(self, phone_number):

#         return get_latest_prediction(phone_number)

# updated for user chat store and prediction


# import torch
# import requests
# from PIL import Image
# from io import BytesIO
# import open_clip

# from app.models.multimodal_model import MultimodalCropModel
# from app.data.preprocessing import get_val_transform
# from app.data.dataset_loader import create_dataloaders
# from app.config import WHATSAPP_ACCESS_TOKEN

# from app.utils.database import get_latest_prediction

# # NEW: MySQL logging
# from app.utils.mysql_functions import save_prediction


# class PredictionService:

#     def __init__(self):

#         self.device = torch.device(
#             "cuda" if torch.cuda.is_available() else "cpu"
#         )

#         # =====================================
#         # CLIP Leaf Detector
#         # =====================================
#         print("Loading CLIP leaf detector...")

#         self.clip_model, _, self.clip_preprocess = open_clip.create_model_and_transforms(
#             "ViT-B-32",
#             pretrained="openai"
#         )

#         self.clip_model = self.clip_model.to(self.device)

#         self.tokenizer = open_clip.get_tokenizer("ViT-B-32")

#         # Leaf prompts
#         self.leaf_prompts = [
#             "a photo of a plant leaf",
#             "a green leaf with veins",
#             "a crop leaf",
#             "a diseased plant leaf",
#             "a close-up of a leaf on a plant"
#         ]

#         # Non-leaf prompts
#         self.non_leaf_prompts = [
#             "a mountain landscape",
#             "a river and sky",
#             "a lake with water",
#             "a waterfall",
#             "a hill with trees",
#             "a forest landscape",
#             "a road in nature",
#             "a city street",
#             "a person selfie",
#             "a human face",
#             "a building",
#             "a car",
#             "fabric texture",
#             "a patterned cloth",
#             "a carpet",
#             "a blanket",
#             "a random indoor object",
#             "a table surface"
#         ]

#         # =====================================
#         # Load Disease Model
#         # =====================================
#         dataset_path = r"app/dataset/train"

#         _, _, self.classes = create_dataloaders(
#             dataset_path=dataset_path,
#             batch_size=1,
#             image_size=224,
#             num_workers=0
#         )

#         print("Detected Classes:", self.classes)
#         print("Total Classes:", len(self.classes))

#         self.model = MultimodalCropModel(len(self.classes)).to(self.device)

#         self.model.load_state_dict(
#             torch.load(
#                 "app/models/best_agri_model.pth",
#                 map_location=self.device
#             )
#         )

#         self.model.eval()

#         self.transform = get_val_transform(224)

#     # =====================================================
#     # Download Image From WhatsApp
#     # =====================================================
#     def download_whatsapp_image(self, media_id):

#         url = f"https://graph.facebook.com/v19.0/{media_id}"

#         headers = {
#             "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
#         }

#         response = requests.get(url, headers=headers)

#         media_url = response.json()["url"]

#         image_response = requests.get(media_url, headers=headers)

#         image = Image.open(BytesIO(image_response.content)).convert("RGB")

#         return image

#     # =====================================================
#     # CLIP Leaf Detection
#     # =====================================================
#     def is_leaf_image(self, image):

#         image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)

#         prompts = self.leaf_prompts + self.non_leaf_prompts

#         text_tokens = self.tokenizer(prompts).to(self.device)

#         with torch.no_grad():

#             image_features = self.clip_model.encode_image(image_input)
#             text_features = self.clip_model.encode_text(text_tokens)

#             image_features /= image_features.norm(dim=-1, keepdim=True)
#             text_features /= text_features.norm(dim=-1, keepdim=True)

#             similarity = (image_features @ text_features.T).softmax(dim=-1)

#         probs = similarity[0].cpu().numpy()

#         best_idx = probs.argmax()
#         best_prompt = prompts[best_idx]

#         leaf_scores = probs[:len(self.leaf_prompts)]
#         non_leaf_scores = probs[len(self.leaf_prompts):]

#         best_leaf = leaf_scores.max()
#         best_non_leaf = non_leaf_scores.max()

#         print("CLIP Prediction:", best_prompt)
#         print("Leaf score:", best_leaf)
#         print("Non-leaf score:", best_non_leaf)

#         if best_idx >= len(self.leaf_prompts):

#             print("Rejected: Non-leaf image detected")

#             return False

#         return True

#     # =====================================================
#     # Disease Prediction
#     # =====================================================
#     def predict(self, image, phone_number=None, image_name="whatsapp_image.jpg"):

#         # Step 1: Check if image is leaf
#         if not self.is_leaf_image(image):

#             print("Rejected: Not a plant leaf")

#             return None, 0.0

#         # Step 2: Run disease model
#         image_tensor = self.transform(image).unsqueeze(0).to(self.device)

#         weather = torch.tensor(
#             [[30.0, 70.0, 5.0]],
#             dtype=torch.float32
#         ).to(self.device)

#         with torch.no_grad():

#             outputs = self.model(image_tensor, weather)

#             probs = torch.nn.functional.softmax(outputs, dim=1)

#             confidence, predicted = torch.max(probs, dim=1)

#         predicted_class = self.classes[predicted.item()]
#         confidence = round(confidence.item(), 4)

#         print("Predicted Class:", predicted_class)
#         print("Confidence:", confidence)

#         # Safety filter
#         if confidence < 0.60:

#             print("Low confidence — likely incorrect image")

#             return None, confidence

#         # =====================================================
#         # Save prediction to MySQL
#         # =====================================================
#         if phone_number is not None:

#             try:
#                 save_prediction(
#                     phone_number,
#                     image_name,
#                     predicted_class,
#                     confidence
#                 )
#                 print("Prediction saved to MySQL")

#             except Exception as e:
#                 print("MySQL save error:", e)

#         return predicted_class, confidence

#     # =====================================================
#     # Get Latest Prediction
#     # =====================================================
#     def get_latest_prediction(self, phone_number):

#         return get_latest_prediction(phone_number)


import torch
import requests
from PIL import Image
from io import BytesIO
import open_clip

from app.models.multimodal_model import MultimodalCropModel
from app.data.preprocessing import get_val_transform
from app.data.dataset_loader import create_dataloaders
from app.config import WHATSAPP_ACCESS_TOKEN

from app.utils.database import get_latest_prediction, save_prediction


class PredictionService:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # =====================================
        # CLIP Leaf Detector
        # =====================================
        print("Loading CLIP leaf detector...")

        self.clip_model, _, self.clip_preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained="openai"
        )

        self.clip_model = self.clip_model.to(self.device)

        self.tokenizer = open_clip.get_tokenizer("ViT-B-32")

        # Leaf prompts
        self.leaf_prompts = [
            "a photo of a plant leaf",
            "a green leaf with veins",
            "a crop leaf",
            "a diseased plant leaf",
            "a close-up of a leaf on a plant"
        ]

        # Non-leaf prompts
        self.non_leaf_prompts = [
            "a mountain landscape",
            "a river and sky",
            "a lake with water",
            "a waterfall",
            "a hill with trees",
            "a forest landscape",
            "a road in nature",
            "a city street",
            "a person selfie",
            "a human face",
            "a building",
            "a car",
            "fabric texture",
            "a patterned cloth",
            "a carpet",
            "a blanket",
            "a random indoor object",
            "a table surface"
        ]

        # =====================================
        # Load Disease Model
        # =====================================
        dataset_path = r"app/dataset/train"

        _, _, self.classes = create_dataloaders(
            dataset_path=dataset_path,
            batch_size=1,
            image_size=224,
            num_workers=0
        )

        print("Detected Classes:", self.classes)
        print("Total Classes:", len(self.classes))

        self.model = MultimodalCropModel(len(self.classes)).to(self.device)

        self.model.load_state_dict(
            torch.load(
                "app/models/best_agri_model.pth",
                map_location=self.device
            )
        )

        self.model.eval()

        self.transform = get_val_transform(224)

    # =====================================================
    # Download Image From WhatsApp
    # =====================================================
    def download_whatsapp_image(self, media_id):

        url = f"https://graph.facebook.com/v19.0/{media_id}"

        headers = {
            "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
        }

        response = requests.get(url, headers=headers)

        media_url = response.json()["url"]

        image_response = requests.get(media_url, headers=headers)

        image = Image.open(BytesIO(image_response.content)).convert("RGB")

        return image

    # =====================================================
    # CLIP Leaf Detection
    # =====================================================
    def is_leaf_image(self, image):

        image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)

        prompts = self.leaf_prompts + self.non_leaf_prompts

        text_tokens = self.tokenizer(prompts).to(self.device)

        with torch.no_grad():

            image_features = self.clip_model.encode_image(image_input)
            text_features = self.clip_model.encode_text(text_tokens)

            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)

            similarity = (image_features @ text_features.T).softmax(dim=-1)

        probs = similarity[0].cpu().numpy()

        best_idx = probs.argmax()
        best_prompt = prompts[best_idx]

        leaf_scores = probs[:len(self.leaf_prompts)]
        non_leaf_scores = probs[len(self.leaf_prompts):]

        best_leaf = leaf_scores.max()
        best_non_leaf = non_leaf_scores.max()

        print("CLIP Prediction:", best_prompt)
        print("Leaf score:", best_leaf)
        print("Non-leaf score:", best_non_leaf)

        # Reject if non-leaf
        if best_idx >= len(self.leaf_prompts):

            print("Rejected: Non-leaf image detected")

            return False

        return True

    # =====================================================
    # Disease Prediction
    # =====================================================
    def predict(self, image, phone_number=None, image_name="whatsapp_image.jpg"):

        # Step 1: Check if image is leaf
        if not self.is_leaf_image(image):

            print("Rejected: Not a plant leaf")

            return None, 0.0

        # Step 2: Run disease model
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)

        weather = torch.tensor(
            [[30.0, 70.0, 5.0]],
            dtype=torch.float32
        ).to(self.device)

        with torch.no_grad():

            outputs = self.model(image_tensor, weather)

            probs = torch.nn.functional.softmax(outputs, dim=1)

            confidence, predicted = torch.max(probs, dim=1)

        predicted_class = self.classes[predicted.item()]
        confidence = round(confidence.item(), 4)

        print("Predicted Class:", predicted_class)
        print("Confidence:", confidence)

        # Safety filter
        if confidence < 0.60:

            print("Low confidence — likely incorrect image")

            return None, confidence

        # =====================================================
        # Save prediction to SQLite database
        # =====================================================
        if phone_number is not None:

            try:

                save_prediction(
                    phone_number,
                    image_name,
                    predicted_class,
                    confidence
                )

                print("Prediction saved to database")

            except Exception as e:

                print("Database save error:", e)

        return predicted_class, confidence

    # =====================================================
    # Get Latest Prediction
    # =====================================================
    def get_latest_prediction(self, phone_number):

        return get_latest_prediction(phone_number)