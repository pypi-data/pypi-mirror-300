from nexusync import NexuSync

from nexusync.models import set_embedding_model, set_language_model
import os

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
LLM_MODEL = "llama3.2"
TEMPERATURE = 0.4
INPUT_DIRS = ["./sample_docs"]  # can put multiple paths

set_embedding_model(huggingface_model=EMBEDDING_MODEL)
set_language_model(ollama_model=LLM_MODEL, temperature=TEMPERATURE)
ns = NexuSync(input_dirs=INPUT_DIRS)

text_qa_template = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information above, I want you to think step by step to answer the query in a crisp manner. "
    "In case you don't know the answer, say 'I don't know!'.\n"
    "Query: {query_str}\n"
    "Answer: "
)

query = "News about Nvidia?"


response = ns.query(text_qa_template=text_qa_template, query=query)

print(f"Query: {query}")
print(f"Response: {response['response']}")
print(f"Response: {response['metadata']}")
