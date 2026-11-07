import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    with open('data/records.json', 'r') as f:
        return json.load(f)

def search_records(query: str):
    records = load_data()
    if not records or not query:
        return []
    
    # Combine fields to create searchable documents
    docs = [f"{r.get('activity_head', '')} {r.get('sub_activity', '')} {r.get('evidence_document', '')}" for r in records]
    
    # Calculate TF-IDF and Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)
    query_vec = vectorizer.transform([query])
    
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Rank and filter results
    ranked_indices = similarities.argsort()[::-1]
    results = []
    
    for idx in ranked_indices:
        if similarities[idx] > 0.05:  # Only return somewhat relevant matches
            record = records[idx].copy()
            record['relevance_score'] = round(float(similarities[idx]), 3)
            results.append(record)
            
    return results