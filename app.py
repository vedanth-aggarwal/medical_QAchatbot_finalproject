from flask import Flask, render_template, jsonify, request
from src.helper import download_hf_embeddings
from langchain_community.vectorstores import Pinecone
import pinecone
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
#from src.prompt import prompt_template
import os

prompt_template="""
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

app = Flask(__name__)

load_dotenv()

from pinecone import Pinecone, ServerlessSpec

embeddings = download_hf_embeddings()
pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
from langchain_pinecone import PineconeVectorStore

index_name = "medical-chatbot"
os.environ['PINECONE_API_KEY'] = 'ed6b1ca9-cbb9-41b7-b8b6-86f044793754'

docsearch = PineconeVectorStore.from_existing_index(index_name,embeddings)

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})


qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get',methods=['GET','POST'])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa.invoke({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])


if __name__ == '__main__':
    app.run(debug=True) # change host = 0.0.0.0 port = 8080

# bootstrap 