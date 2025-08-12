from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
import json

# ----------------------
# 1. Load Embedding Model
# ----------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# ----------------------
# 2. Read and Parse Data
# ----------------------
txt_file = "bom_loan_products.txt"
documents = []

with open(txt_file, "r", encoding="utf-8") as f:
    raw_content = f.read()

# Split by double newlines (each loan section separated by blank line)
sections = raw_content.strip().split("\n\n")

for section in sections[1:]:  # Skip first if it's a heading
    lines = section.strip().split("\n")

    if len(lines) >= 4:
        loan_type = lines[0].strip()
        url = lines[1].replace("URL: ", "").strip()
        key_info = lines[2].replace("Key Info Highlights: ", "").strip()
        details = lines[3].replace("Details: ", "").strip()

        documents.append({
            "loan_type": loan_type,
            "url": url,
            "key_info": key_info,
            "details": details
        })

# ----------------------
# 3. Chunking
# ----------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # characters per chunk
    chunk_overlap=50,
    length_function=len
)

chunked_docs = []
for doc in documents:
    chunks = text_splitter.split_text(doc["details"])
    for i, chunk in enumerate(chunks):
        chunked_docs.append({
            "loan_type": doc["loan_type"],
            "url": doc["url"],
            "key_info": doc["key_info"],
            "chunk_id": f"{doc['loan_type'].replace(' ', '_')}_chunk_{i+1}",
            "content": chunk
        })

# ----------------------
# 4. Create Embeddings
# ----------------------
texts = [c["content"] for c in chunked_docs]
embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

# ----------------------
# 5. Create FAISS Index
# ----------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ----------------------
# 6. Save Index & Metadata
# ----------------------
faiss.write_index(index, "bom_loan_index.faiss")

with open("bom_loan_metadata.json", "w", encoding="utf-8") as f:
    json.dump(chunked_docs, f, ensure_ascii=False, indent=2)

print(f"✅ Saved FAISS index with {len(chunked_docs)} chunks and metadata.")
