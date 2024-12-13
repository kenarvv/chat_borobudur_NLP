import random
import json

# Placeholder untuk pustaka Gemini, pastikan sudah terinstal dan diimport
from gemini import GeminiModel

# Load model Gemini
model_path = "path_to_gemini_model"  # Path ke model Gemini yang sudah di-fine-tune
model = GeminiModel.load(model_path)

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

bot_name = "Sam"

def get_response(msg):
    # Kirimkan pesan ke model Gemini untuk mendapatkan respons
    response = model.generate_response(
        instruction=msg,
        context="",  # Bisa ditambahkan konteks jika dibutuhkan
        temperature=0.7,  # Atur parameter untuk variasi respons
        top_p=0.9
    )
    
    # Periksa apakah respons sesuai dengan intent atau fallback
    if response:
        return response
    return "I do not understand..."

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence.lower() == "quit":
            break

        resp = get_response(sentence)
        print(resp)
