from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

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

def process_query_with_docs(document_context, user_question):
    if document_context:
        chain = get_conversational_chain()
        response = chain({"input_documents": [document_context], "question": user_question}, return_only_outputs=True)
        return response["output_text"]
    else:
        return "No document context available."
