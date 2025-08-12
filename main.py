from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import faiss
import json
import openai
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load your embedding model & FAISS index
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("bom_loan_index.faiss")

# Load metadata
with open("bom_loan_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Decode SYSTEM_PROMPT from base64 env var
encoded_prompt = os.getenv("ENCODED_SYSTEM_PROMPT")
if not encoded_prompt:
    raise ValueError("ENCODED_SYSTEM_PROMPT env variable not found")
SYSTEM_PROMPT = base64.b64decode(encoded_prompt).decode()

def search(query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1:
            results.append({
                "loan_type": metadata[idx]["loan_type"],
                "url": metadata[idx]["url"],
                "key_info": metadata[idx]["key_info"],
                "chunk_id": metadata[idx]["chunk_id"],
                "content": metadata[idx]["content"],
                "distance": float(dist)
            })
    return results

def ask_llm(query, retrieved_docs):
    context_text = "\n\n".join(
        [f"Loan Type: {doc['loan_type']}\nKey Info: {doc['key_info']}\nContent: {doc['content']}"
         for doc in retrieved_docs]
    )
    prompt = f"""
You are a Loan Product Assistant. Use the following loan document context to answer the question.
Context:
{context_text}
Question: {query}
Answer in a clear, concise way.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )
    return response.choices[0].message["content"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('question', '')
    results = search(query, top_k=3)
    llm_answer = ask_llm(query, results)
    return jsonify({"answer": llm_answer})

if __name__ == '__main__':
    app.run(debug=True)
