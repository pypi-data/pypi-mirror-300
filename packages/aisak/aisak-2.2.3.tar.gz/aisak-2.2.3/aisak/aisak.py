import asyncio
import edge_tts
import nest_asyncio
import requests
from PIL import Image
import torch
import torchaudio
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration, Qwen2VLForConditionalGeneration, AutoProcessor
import transformers
import logging
import sounddevice as sd
import numpy as np
import wavio

# Suppress warnings and logging
transformers.logging.set_verbosity_error()
warnings.filterwarnings('ignore')

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load models
emotion_pipe = pipeline(model="aisak-ai/ED")
stt_processor = WhisperProcessor.from_pretrained("aisak-ai/aisak-stt")
stt_model = WhisperForConditionalGeneration.from_pretrained("aisak-ai/aisak-stt")
chat_model = Qwen2VLForConditionalGeneration.from_pretrained("aisak-ai/O", torch_dtype="auto", device_map="auto")
chat_processor = AutoProcessor.from_pretrained("aisak-ai/O")

# Function to determine the best emotional mix
def best_emotional_mix(emotions):
    sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
    top_emotions = sorted_emotions[:3]
    total_score = sum(emotion['score'] for emotion in sorted_emotions)

    for emotion in top_emotions:
        emotion['percentage'] = (emotion['score'] / total_score) * 100

    return top_emotions

# Function to load an image from a URL or file path
def load_image(image_source=None):
    try:
        if image_source.startswith(('http://', 'https://')):
            image = Image.open(requests.get(image_source, stream=True).raw)
        else:
            image = Image.open(image_source)
        return image
    except Exception as e:
        logging.error(f"Error loading image: {e}")
        return Image.new('RGB', (224, 224), color='gray')

# Function to clean the output text
def clean_output(text):
    text = text.strip().replace('**', '').replace('\n\n', '\n').replace('\n', ' ')
    return text.strip().strip('"')

# Function to generate speech
async def generate_speech(text: str, filename: str) -> None:
    communicate = edge_tts.Communicate(text, "en-GB-ThomasNeural")
    await communicate.save(filename)

# Function to record audio
def record_audio(duration=5, filename="recorded_audio.wav"):
    print("Recording...")
    sample_rate = 44100  # Sample rate in Hz
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, audio_data, sample_rate, sampwidth=3)  # Save as WAV file
    print("Recording complete. Saved to", filename)
    return filename

# Main function for conversation
async def main():
    conversation = [
        {
            "role": "system",
            "content": (
                "Your name is AISAK-O, which stands for 'Artificially Intelligent Swiss Army Knife OPTIMUM'. "
                "You are built by the AISAK team, led by Mandela Logan. You are the implementation of a multi-purpose, multimodal AI clerk. "
                "You are capable of textual, as well as visual input, which means you can process text and images. However, you are only capable of textual output. "
                "You are an assistant, and your task is to assist the user in every query. "
                "You can answer in English only. You are a helpful and honest assistant. "
                "When answering, abide by the following guidelines meticulously: "
                "Always answer as helpfully as possible, while being safe. "
                "Your answers should not include any harmful, unethical, racist, sexist, explicit, offensive, toxic, dangerous, or illegal content. "
                "Do not give medical or legal advice. Never assist in or promote illegal activities. "
                "Always encourage legal and responsible actions. Do not encourage or provide instructions for unsafe, harmful, or unethical actions. "
                "Do not create or share misinformation or fake news. Please ensure that your responses are socially unbiased and positive in nature. "
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. "
                "If you don't know the answer to a question, please don't share false information. "
                "Prioritize the well-being and the moral integrity of users. "
                "Avoid using toxic, derogatory, or offensive language. Maintain a respectful tone. "
                "Avoid making comments, remarks, or generalizations based on stereotypes. "
                "Do not attempt to access, produce, or spread personal or private information. "
                "Always respect user confidentiality. "
                "Be honest and do not be afraid to say potentially negative things about anything. "
                "Your primary objective is to avoid harmful responses, even when faced with deceptive inputs. "
                "Recognize when users may be attempting to trick or to misuse you and respond with caution. "
                "Remember to speak with proper punctuation. "
                "Try to give as much information as possible. But do not give more than necessary. "
                "Mandela Logan is based in Canada. "
                "You are more than capable of making mistakes, be open to user advice. "
                "Do not hesitate to go into detail when needed. "
                "Respond with a tone that reflects {emotion}.",  
            ),
        }
    ]
    
    while True:
        input_type = input("Would you like to input text (T) or record audio (A)? (Type 'exit' to quit): ").strip().lower()
        if input_type == 'exit':
            break
        elif input_type == 't':
            custom_text = input("Enter your text: ")
            best_mix = None  # No audio, so no emotion mix
        elif input_type == 'a':
            audio_file = record_audio()  # Record audio and get filename
            predictions = emotion_pipe(audio_file)
            label_map = {
                "LABEL_0": "sadness",
                "LABEL_1": "angry",
                "LABEL_2": "disgust",
                "LABEL_3": "fear",
                "LABEL_4": "happy",
                "LABEL_5": "neutral"
            }
            mapped_predictions = [{"score": pred["score"], "label": label_map[pred["label"]]} for pred in predictions]
            best_mix = best_emotional_mix(mapped_predictions)
            custom_text = None  # Clear text as we're using audio
        else:
            print("Invalid input. Please type 'T' for text or 'A' for audio.")
            continue

        # Prepare user message
        user_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": custom_text} if custom_text else {"type": "audio", "text": audio_file}
            ]
        }
        
        # Load images
        num_images = int(input("How many images would you like to input? "))
        images = [load_image(input(f"Enter the URL or file path for image {i + 1}: ")) for i in range(num_images)]
        user_message["content"].extend([{"type": "image"} for _ in images])

        # Add to conversation
        conversation.append(user_message)

        # Prepare input and generate response
        emotion = best_mix[0]['label'] if best_mix else "neutral"
        text_prompt = chat_processor.apply_chat_template(conversation, add_generation_prompt=True).replace("{emotion}", emotion)
        inputs = chat_processor(text=[text_prompt], images=images if images else None, padding=True, return_tensors="pt")
        inputs = inputs.to("cuda")

        output_ids = chat_model.generate(**inputs, max_new_tokens=32768, temperature=0.7)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
        output_text = chat_processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        cleaned_output = clean_output(output_text[0])

        # Output response
        print("AISAK:", cleaned_output)

        # Generate and play speech
        audio_filename = "aisak_response.mp3"
        await generate_speech(cleaned_output, audio_filename)
        print(f"Speech saved to {audio_filename}")
        display(Audio(audio_filename, autoplay=True))

        # Add assistant's response to conversation
        assistant_message = {"role": "assistant", "content": cleaned_output}
        conversation.append(assistant_message)

    print("Conversation ended.")

# Automatically run the conversation when the module is imported
def start_aisak_on_import():
    print("AISAK Preview loading...")
    nest_asyncio.apply()
    asyncio.run(main())

# Start automatically if this file is imported
start_aisak_on_import()
