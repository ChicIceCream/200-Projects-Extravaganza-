import os
import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
from dotenv import load_dotenv
import requests

def setup_model():
    """Initialize the tokenizer and model."""
    # Using the correct model name and tokenizer configuration
    model_name = "ai4bharat/indic-bert"
    
    # Initialize tokenizer with use_fast=False to avoid tiktoken issues
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=False,  # Use the slower but more compatible tokenizer
        do_lower_case=True
    )
    
    # Initialize the base model
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

def process_text(text, tokenizer, model, max_length=128):
    """Process text through the Indic-BERT model."""
    # Prepare the input
    encoded_input = tokenizer(
        text,
        padding='max_length',
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    )
    
    # Get model outputs
    with torch.no_grad():
        outputs = model(**encoded_input)
        
    # Get the pooled output (CLS token output)
    pooled_output = outputs.last_hidden_state[:, 0, :]
    return pooled_output

def main():
    # Load environment variables
    load_dotenv()
    API_TOKEN = os.getenv("HF_TOKEN")
    
    # Example texts in different Indian languages
    texts = [
        "यह एक बहुत अच्छी किताब है।",  # Hindi
        "हे एक चांगले पुस्तक आहे।",     # Marathi
        "ಇದು ಒಳ್ಳೆಯ ಪುಸ್ತಕ ಆಗಿದೆ।",    # Kannada
    ]
    
    try:
        # Initialize tokenizer and model
        print("Loading model and tokenizer...")
        tokenizer, model = setup_model()
        print("Model and tokenizer loaded successfully!")
        
        # Process each text
        for text in texts:
            print(f"\nProcessing text: {text}")
            embeddings = process_text(text, tokenizer, model)
            print(f"Embedding shape: {embeddings.shape}")
            print(f"First few values of embedding: {embeddings[0][:5]}")
            
            # If you want to use the Hugging Face API instead
            try:
                api_url = "https://api-inference.huggingface.co/models/ai4bharat/indic-bert"
                headers = {"Authorization": f"Bearer {API_TOKEN}"}
                
                api_response = requests.post(
                    api_url,
                    headers=headers,
                    json={
                        "inputs": text,
                        "parameters": {
                            "max_length": 128
                        }
                    }
                )
                
                if api_response.status_code == 200:
                    print(f"API Response successful!")
                else:
                    print(f"API Error: {api_response.status_code}")
                    
            except Exception as e:
                print(f"API request error: {str(e)}")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure you have the latest transformers library installed:")
        print("pip install --upgrade transformers torch")

if __name__ == "__main__":
    main()