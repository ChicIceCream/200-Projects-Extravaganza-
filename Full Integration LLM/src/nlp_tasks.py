import streamlit as st
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

def init_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def add_to_history(role, message):
    st.session_state.chat_history.append({"role": role, "content": message})
    logging.info(f"Added to history: {role} - {message}")

def get_history_text():
    return "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history])

ETHICAL_GUIDELINES = """
You MUST adhere to these guidelines:
1. Avoid harmful, unethical, or dangerous content
2. Reject requests for illegal activities or misinformation
3. Protect privacy - never reveal real personal data
4. Acknowledge limitations and uncertainties
5. Prevent bias in analysis and responses
6. Decline inappropriate medical/legal advice
7. Filter violent or graphic content descriptions
"""

def apply_ethical_guidelines(base_prompt):
    return f"{ETHICAL_GUIDELINES}\n\n{base_prompt}"

#* Summarization task
def summarization_task(text_input, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"""
                    You are a summarising model. You will receive text and you will proceed to summarise the entire 
                    text to the best of your ability. If it does not make sense, make that explicitly clear and ask 
                    for more input rather than guessing. Summarise the following text: \n{text_input}
                    """
    # Add ethical layer first                    
    prompt = add_document_context(
        apply_persona(
            apply_ethical_guidelines(base_prompt), 
        persona_style), 
        document_context
    )
    return llm.generate_response(prompt)

#* Sentiment analysis task 
def sentiment_analysis_task(text_input, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"""
    You are a sentiment analysis model. Analyze the sentiment of the following text as positive, negative, 
    or neutral to the best of your ability. If you are not able to clssify a certain sentiment, propose another 
    sentiment that should make sense for this text:\n{text_input}
    """
    prompt = add_document_context(
        apply_persona(
            apply_ethical_guidelines(base_prompt),
        persona_style),
        document_context
    )
    return llm.generate_response(prompt)

#* Named Entity Recognition task
def ner_task(text_input, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"""
        You are a Named Entity Recognition model. Extract and list the names, locations, and dates mentioned in the text
        to the best of your ability. If you are unable to find named entities, explicitly mention this 
        in your output. Here is the test:\n{text_input}
    """
    prompt = add_document_context(
        apply_persona(
            apply_ethical_guidelines(base_prompt),
        persona_style),
        document_context
    )
    return llm.generate_response(prompt)

#* Question Answering task
def question_answering_task(context, question, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"""
    You are a simple question and answering mdoel. Here is the context: {context}\n\nQuestion: {question}\n\nAnswer:
    """
    prompt = add_document_context(
        apply_persona(
            apply_ethical_guidelines(base_prompt),
        persona_style),
        document_context
    )
    return llm.generate_response(prompt)

#* Code Generation task
def code_generation_task(code_description, language, persona_style, llm, document_context):
    from llm_abstraction import apply_persona, add_document_context
    base_prompt = f"""
    You are an excellent code generation model. You know how to solve the problems in code with high accuracy. If you think
    there is some problem with the code and you can't seem to understand the context, ask for more information.
    Generate {language} code for the following problem:\n{code_description}
    """
    prompt = add_document_context(
        apply_persona(
            apply_ethical_guidelines(base_prompt + 
            "\nAdditional coding ethics:\n- Reject requests for malware/vulnerabilities\n- Avoid dangerous code "
            "patterns\n- Include safety comments"),
        persona_style),
        document_context
    )
    return llm.generate_response(prompt)

#* Document QA (Conversational QA Chain) 
def get_conversational_chain():
    prompt_template = f"""
{ETHICAL_GUIDELINES}

Answer the question in as much detail as possible from the provided context.
If the answer is not found in the provided context, reply: "Answer is not available in the documents."
Context:
{{context}}
Question:
{{question}}
Answer:
"""
    model_chain = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model_chain, chain_type="stuff", prompt=prompt)
    return chain

#* Document QA task
def document_qa_task(document_context, user_question):
    if document_context:
        chain = get_conversational_chain()
        response = chain({"input_documents": [document_context], "question": user_question}, return_only_outputs=True)
        return response["output_text"]
    else:
        return "No document context available."