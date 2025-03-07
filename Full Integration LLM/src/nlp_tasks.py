import streamlit as st
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Conversation History Functions
def init_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def add_to_history(role, message):
    st.session_state.chat_history.append({"role": role, "content": message})
    logging.info(f"Added to history: {role} - {message}")

def get_history_text():
    return "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history])


#* Summarization task
def summarization_task(text_input, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"""
                    You are a summarising model. You will receive text and you will proceed to summarise the entire 
                    text to the best of your ability. If it does not make sense, make that explicitly clear and ask 
                    for more input rather than guessing. Summarise the following text: \n{text_input}
                    """
    prompt = add_document_context(apply_persona(base_prompt, persona_style), document_context)
    return llm.generate_response(prompt)

#* Sentiment analysis task
def sentiment_analysis_task(text_input, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"Analyze the sentiment of the following text as positive, negative, or neutral:\n{text_input}"
    prompt = add_document_context(apply_persona(base_prompt, persona_style), document_context)
    return llm.generate_response(prompt)

def ner_task(text_input, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"Extract and list the names, locations, and dates mentioned in the text:\n{text_input}"
    prompt = add_document_context(apply_persona(base_prompt, persona_style), document_context)
    return llm.generate_response(prompt)

def question_answering_task(context, question, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    prompt = add_document_context(apply_persona(base_prompt, persona_style), document_context)
    return llm.generate_response(prompt)

def code_generation_task(code_description, language, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"Generate {language} code for the following problem:\n{code_description}"
    prompt = add_document_context(apply_persona(base_prompt, persona_style), document_context)
    return llm.generate_response(prompt)

# Document QA (Conversational QA Chain)
def get_conversational_chain():
    prompt_template = """
Answer the question in as much detail as possible from the provided context.
If the answer is not found in the provided context, reply: "Answer is not available in the documents."
Context:
{context}
Question:
{question}
Answer:
"""
    model_chain = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model_chain, chain_type="stuff", prompt=prompt)
    return chain

def document_qa_task(document_context, user_question):
    if document_context:
        chain = get_conversational_chain()
        response = chain({"input_documents": [document_context], "question": user_question}, return_only_outputs=True)
        return response["output_text"]
    else:
        return "No document context available."
