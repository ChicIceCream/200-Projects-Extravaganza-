# Overview
This is an abstraction layer on top of multiple Large Language Models. It supports multiple NLP tasks such as summarization, sentiment analysis, named entity recognition (NER), question answering, code generation, and multi-turn dialogue with document-based question answering.


# Project Architecture
```
project-root/
├── src/
│   ├── llm_abstraction.py       # LLM classes 
│   ├── data_processing.py       # File processing with caching + text preprocessing (stopwords, normalization, etc.)
│   ├── nlp_tasks.py             # NLP tasks 
│   ├── app.py                   # Streamlit UI
├── tests/
│       ├── test_data_processing.py  # Unit tests for data processing
│       └── test_nlp_tasks.py        # Unit tests for NLP tasks
```

# Setup Instructions
### Prerequisites
- Protobuf library might cause some issues with the transformers library
- Install required packages listed in requirements.txt
### Installation
``` 
git clone **need to change**
cd your-repo-directory
```
Install dependencies using pip:
```
pip install -r requirements.txt
```
### Environment Setup
Create a .env file in /src with the following keys:
```
GOOGLE_API_KEY=  "Your-Key"
GROQ_API_KEY = "Your-Key"
```

# Running the Application
Simply launch the streamlit application:
```
streamlit run src/app.py
```
This command starts the web application.

# Running Tests
Unit tests are provided to ensure the integrity of core functionalities.

To run tests using pytest, execute:
```
pytest tests/
```
This will run tests in test_data_processing.py and test_nlp_tasks.py to verify that data processing functions and NLP task implementations are working as expected.

# Detailed File Descriptions
- llm_abstraction.py 

Contains two primary classes:

- `Gemini`: Uses Google's generative AI (via genai) for generating responses.

- `Groq`: Interacts with the Groq API using an OpenAI-compatible endpoint.

Also includes helper functions to modify prompts based on user-defined persona. Also helps append document data to the LLMs when required

- data_processing.py

Handles document ingestion from PDF, CSV, and TXT files. It includes a caching mechanism (@st.cache_data) to avoid reprocessing identical documents. 

Includes functions to handle data processing such as normalization and tokenization

- nlp_tasks.py

Implements core NLP functionalities: summarization, sentiment analysis, etc.

- app.py

The main Streamlit application file. It sets up the user interface, processes file uploads, and allows users to select from various NLP functionalities.

- tests/

Contains unit tests:

- test_data_processing.py: Tests for file processing and additional text preprocessing functions.
- test_nlp_tasks.py: Tests for conversation history functions and other NLP tasks (e.g., summarization).

# Logging and Caching
- Caching:
Document processing results are cached using Streamlit’s @st.cache_data decorator in data_processing.py, which minimizes redundant processing.

- Logging:
All major operations (file processing, API calls, NLP task execution, and conversation history updates) are logged to app.log for debugging and traceability.
