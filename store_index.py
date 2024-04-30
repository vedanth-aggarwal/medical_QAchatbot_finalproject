from src.helper import load_pdf,text_split,download_hf_embeddings
from dotenv import load_dotenv
import os

load_dotenv()

from pinecone import Pinecone, ServerlessSpec
import os

extracted_data = load_pdf('data/')
text_chunks = text_split(extracted_data)
embeddings = download_hf_embeddings()

pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
from langchain_pinecone import PineconeVectorStore

index_name = "medical-chatbot"
index = pc.Index('medical-chatbot')

os.environ['PINECONE_API_KEY'] = 'ed6b1ca9-cbb9-41b7-b8b6-86f044793754'
docsearch = PineconeVectorStore.from_texts(
        [t.page_content for t in text_chunks],
        index_name=index_name,
        embedding=embeddings)

