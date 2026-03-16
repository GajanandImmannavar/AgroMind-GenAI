# AgroMind-GenA
End-to-end multimodal AI system for plant disease detection from leaf images using deep learning, CLIP validation, and RAG-based advisory delivered via WhatsApp.

# 🌿 AgroMind GenAI — Multimodal Plant Disease Detection & Advisory System

AgroMind GenAI is an end-to-end AI system that enables farmers to diagnose plant diseases by sending leaf images via WhatsApp. The platform combines deep learning–based computer vision, multimodal learning, and a Retrieval-Augmented Generation (RAG) module to provide accurate diagnosis and actionable farming guidance through a conversational interface.

---

## 📌 Project Overview

Plant diseases can significantly reduce crop yield if not detected early. AgroMind GenAI provides an automated solution that analyzes plant leaf images and delivers treatment recommendations without requiring physical access to agricultural experts.

---

## ✨ Key Features

• Automatic plant disease detection from leaf images  
• CLIP-based validation to reject non-leaf images  
• Multimodal prediction using image + environmental inputs  
• AI advisory chatbot powered by RAG  
• Real-time interaction via WhatsApp  
• Context-aware responses based on detected disease  
• Prediction history and chat storage  
• Feedback collection for system improvement  

---

## 🧠 Model Architecture

Disease Classification Model: **Multimodal CNN (EfficientNet-B2 backbone)**  
Framework: **PyTorch with Transfer Learning**

Leaf Validation Model: **CLIP (Vision-Language Model)**  

Advisory System: **Retrieval-Augmented Generation (RAG)**  

---

## 📡 Complete System Pipeline

### 🔹 Image Diagnosis Pipeline

1. Farmer sends a leaf image via WhatsApp  
2. WhatsApp Business API forwards the message to FastAPI webhook  
3. Server downloads the image from Meta servers  
4. CLIP model checks whether the image contains a plant leaf  

   • If NOT a leaf → Request a valid leaf image  
   • If leaf → Continue  

5. Image is preprocessed and passed to the Multimodal CNN model  
6. Model predicts disease class and confidence score  

   • Low confidence → Ask for clearer image  
   • Valid prediction → Continue  

7. Prediction result is stored in SQLite database  
8. RAG system retrieves disease knowledge  
9. System generates explanation (symptoms, treatment, prevention)  
10. Response is sent back to the farmer via WhatsApp  

---

### 🔹 Conversational AI Pipeline (After Diagnosis)

1. Farmer sends a text query  
2. Webhook receives the message  
3. System retrieves the user's latest disease prediction  
4. Question Mapper detects intent (symptoms, cause, treatment, etc.)  
5. Sentence Transformer generates embeddings  
6. Vector search retrieves relevant knowledge from ChromaDB  
7. RAG pipeline generates grounded response  
8. Answer is sent via WhatsApp  
9. Chat history and feedback are stored  

---

### 🔹 Training Pipeline

Dataset → Data Augmentation → DataLoader  
→ Multimodal CNN Training → Loss Optimization  
→ Model Evaluation → Best Model Saved  

---

## ⚙️ Training Configuration

Image Size: **192 / 224**  
Batch Size: **8**  
Optimizer: **Adam**  
Loss Function: **CrossEntropyLoss**

Data augmentation:

• Random crop  
• Rotation  
• Horizontal & vertical flip  
• Color jitter  
• Perspective distortion  
• Gaussian blur  
• Normalization  

Evaluation metrics:

• Accuracy  
• F1 Score  
• Confusion Matrix  
• Classification Report  

---

## 🤖 NLP & Generative AI Components

Embedding Model: **Sentence Transformers (MiniLM — Hugging Face ecosystem)**  
Vector Database: **ChromaDB**  
Framework: **LangChain**

Provides grounded responses about:

• Symptoms  
• Causes  
• Treatment  
• Prevention  
• Recovery time  
• Cost  

---

## 🗂️ Repository Structure

```
AgroMind GenAI
│
├── README.md
├── requirements.txt
├── train.py
├── agromind.db
├── .env
│
├── app
│   ├── main.py
│   ├── config.py
│   ├── api
│   ├── data
│   ├── dataset
│   ├── ml
│   ├── models
│   ├── rag
│   ├── services
│   └── utils
│
├── venv
├── .vscode
└── __pycache__
```

---

## 🚀 How to Run the Project

Install dependencies:

```
pip install -r requirements.txt
```

Train the model:

```
python train.py
```

Run the API server:

```
uvicorn app.main:app --reload
```

Configure environment variables in `.env`:

```
WHATSAPP_ACCESS_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_id
WEBHOOK_VERIFY_TOKEN=your_verify_token
```

---

## 🛠️ Tech Stack

Python • PyTorch • Computer Vision • Deep Learning  
EfficientNet • CLIP • Multimodal AI  
FastAPI • NLP • RAG • LangChain  
Sentence Transformers • ChromaDB • SQLite  
Git • GitHub • WhatsApp Business API  

---

## 🔮 Future Improvements

• Integration with real-time weather APIs  
• Multilingual support for farmers  
• Cloud deployment for scalability  
• Mobile application interface  
• Support for additional crops and diseases  
• Continuous model retraining using collected feedback  

---

## ⚠️ Important Notes

• `.env`, `venv`, and cache files are not included for security reasons  
• Large model files may be excluded due to repository size limits  
• Requires valid WhatsApp Business API credentials to run fully  

---

## 📜 License

Released under the MIT License.

---

## 👤 Author

Gajanand L Immannavar  
AI/ML Enthusiast | Computer Vision | Generative AI
