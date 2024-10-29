from dotenv import loadenv
loadenv()
import os
import requests

API_TOKEN = os.getenv("HF_TOKEN")
os.environ['HF_TOKEN']= os.getenv("HF_TOKEN")

# Define headers with your API token
API_TOKEN = "your_huggingface_token_here"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Input data for summarization
data = {
    "inputs": "आपका यहाँ पर उदाहरण टेक्स्ट होगा। इसमें कुछ वाक्य हो सकते हैं जिनका आप संक्षेपण करना चाहते हैं।",
    "parameters": {
        "max_length": 100,
        "num_beams": 4,
    }
}

# Send request to Hugging Face model endpoint
response = requests.post(
    "https://api-inference.huggingface.co/models/ai4bharat/indic-bart",
    headers=headers,
    json=data,
)

summary = response.json()[0]['summary_text']
print("Summary:", summary)
