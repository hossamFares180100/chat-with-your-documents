from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    WhisperProcessor,
    WhisperForConditionalGeneration,
)
import soundfile as sf
from gtts import gTTS
import os

# Symptom Analysis (Bio_ClinicalBERT)
symptom_model_name = "emilyalsentzer/Bio_ClinicalBERT"
symptom_tokenizer = AutoTokenizer.from_pretrained(symptom_model_name)
symptom_model = AutoModelForSequenceClassification.from_pretrained(symptom_model_name)

def analyze_symptoms(symptom_description):
    inputs = symptom_tokenizer(symptom_description, return_tensors="pt", truncation=True, padding=True)
    outputs = symptom_model(**inputs)
    probabilities = outputs.logits.softmax(dim=1)
    diagnosis_idx = probabilities.argmax().item()
    diagnosis = ["Cold", "Flu", "COVID-19", "Migraine", "Allergy"]  # Example classes
    return diagnosis[diagnosis_idx], probabilities[0][diagnosis_idx].item()

# Question Answering (deepset/roberta-base-squad2)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def answer_health_question(question, context):
    response = qa_pipeline(question=question, context=context)
    return response["answer"]

# Speech-to-Text (Whisper)
audio_model_name = "openai/whisper-small"
whisper_processor = WhisperProcessor.from_pretrained(audio_model_name)
whisper_model = WhisperForConditionalGeneration.from_pretrained(audio_model_name)

def transcribe_audio(audio_path):
    audio_input, sample_rate = sf.read(audio_path)
    inputs = whisper_processor(audio_input, sampling_rate=sample_rate, return_tensors="pt")
    predicted_ids = whisper_model.generate(inputs["input_features"])
    return whisper_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

# Text-to-Speech (gTTS)
def speak_response(response):
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")  # For Linux/macOS, replace "start" with "xdg-open".

# Main Function
def medical_assistant_interaction(input_type="text", user_input=None, audio_path=None):
    if input_type == "audio":
        user_input = transcribe_audio(audio_path)
        print(f"Transcribed Audio: {user_input}")
    
    print("User Input:", user_input)
    speak_response("Analyzing your input...")

    if any(keyword in user_input.lower() for keyword in ["symptom", "feeling", "diagnosis", "illness"]):
        # Symptom Analysis Logic
        diagnosis, confidence = analyze_symptoms(user_input)
        response = f"Based on the symptoms, it could be {diagnosis}. Confidence: {confidence:.2f}."
    else:
        # Default Medical Context for Question Answering
        medical_context = """
        Flu is a contagious respiratory illness caused by influenza viruses. Symptoms include fever, cough, and fatigue.
        Common treatments are rest, hydration, and antiviral medications.
        """
        response = answer_health_question(user_input, medical_context)
    
    print("Assistant Response:", response)
    speak_response(response)
    return response

# Example Scenarios
if _name_ == "_main_":
    print("AI-Powered Medical Assistant")
    print("Choose Input Type:")
    print("1: Text Input")
    print("2: Audio Input")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        print("Example 1: Text Input for Symptoms or Questions")
        user_input = input("Describe your symptoms or ask a medical question: ")
        medical_assistant_interaction(input_type="text", user_input=user_input)
    
    elif choice == "2":
        print("Example 2: Audio Input")
        audio_path = input("Provide the path to your audio file (e.g., user_audio_sample.wav): ").strip()
        medical_assistant_interaction(input_type="audio", audio_path=audio_path)
    
    else:
        print("Invalid choice. Please restart the program.")