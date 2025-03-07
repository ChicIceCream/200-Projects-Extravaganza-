# Technical Report 
## Overview

This technical report summarizes the design choices, technical decisions, and optimizations implemented in the AI Assistant project. The goal was to build a robust, modular Streamlit application that integrates multiple NLP functionalities by using external APIs, efficient document processing, and best practices in caching and logging.

## Design Choices and Technical Decisions

### Document Processing
- **PyPDF2 vs. pdf2image:**  
  I chose **PyPDF2** for extracting text from PDFs because it is faster and more lightweight compared to pdf2image after testing with multipel pdfs. This choice improves processing speed and reduces resource usage, which is crucial when handling multiple documents in a real-time web app.

- **Pandas for CSV Understanding:**  
  **Pandas** was used to read CSV files since it provides robust handling of tabular data, enabling us to quickly concatenate cell values into a unified text string for NLP processing.

- **Text Files Handling:**  
  Direct decoding for TXT files was implemented to quickly load and process plain text documents without additional overhead.

- **In-Streamlit Processing:**  
  By processing documents directly within Streamlit, I avoided the need for a dedicated backend server. This reduces complexity and potential server issues.

### API Integration
- **Gemini API for Free Testing:**  
  I integrated the **Gemini API** for testing purposes because it is available for free and still almost on par with other proprietary models

- **Groq API for OpenAI Compatibility:**  
  The **Groq API** was used for production-like scenarios to be similar to OpenAI’s behavior while keeping operational costs zero.

### Caching and Logging
- **Caching:**  
  I implemented caching using Streamlit's `@st.cache_data` decorator in the document processing module. This should help avoid redundant processing of identical documents and reduce computation time.

- **Logging:**  
  Comprehensive logging is implemented across major operations (file processing, API calls, and NLP task execution).

### NLP Tasks and QA Chain
- **LangChain for QA Chain:**  
  I used **LangChain** to implement the document QA chain because it simplifies the construction of prompt templates and chains for question answering.

- **Improved Prompts:**  
  Prompts have been carefully designed and enhanced with persona-based modifications and optional document context. This ensures that the LLM receives clear, well-structured instructions.

## Optimization and Debugging Strategies

- **Efficient Document Extraction:**  
  By leveraging PyPDF2 and pandas, I ensure that document extraction is efficient even for large files. The caching mechanism further reduces repeated work.

- **Real-Time Processing in Streamlit:**  
  Processing documents within Streamlit minimizes external dependencies and potential server bottlenecks. This real-time integration allows for seamless user interactions.

- **Caching:**  
  Caching not only speeds up repeated operations but also makes debugging easier by ensuring that once a file is processed, the cached result is used, thus isolating issues in other parts of the system.

- **Logging:**  
  Detailed logging at key stages of the application (e.g., file processing, API calls, and task execution) allows developers to quickly pinpoint issues and measure performance.

- **Unit Testing:**  
  The project includes unit tests for core functionalities (document processing, text preprocessing, conversation history, etc.), which aids in continuous integration and deployment while catching regressions early.

## Ethical Considerations and Data Handling Policies

- **Prompt Ethics:**  
  The prompts are designed to be as clear and neutral as possible. I have added instructions to handle situations where the answer is not available to avoid misinformation.

- **Data Privacy:**  
  Uploaded documents are processed on the client side (within the Streamlit session) and are not stored persistently on external servers unless explicitly saved by the user. 

## Potential Enhancements for Future Iterations

- **Advanced Text Preprocessing:**  
  Future enhancements could include more sophisticated NLP techniques such as lemmatization or stemming, using libraries like NLTK or spaCy.

- **Extended Caching Strategies:**  
  Implementing additional caching layers (e.g., in-memory caching using Redis) might improve performance for high-traffic scenarios.

- **Enhanced QA Chain:**  
  Further refinement of the QA chain by incorporating more advanced context retrieval methods (if needed) or integrating external vector databases for semantic search.

- **User Interface Improvements:**  
  Additional UI components, such as interactive document viewers and real-time progress indicators, can enhance user experience.

- **Scalability and Deployment:**  
  Future iterations might include containerization (e.g., Docker) and orchestration (e.g., Kubernetes) for production-grade deployments, along with dedicated monitoring tools.

---