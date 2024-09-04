from fastapi import FastAPI, Query
import pandas as pd
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize FastAPI
app = FastAPI()

# Global variables to store the data and models
grouped_df = None
vectorizer = None
similarity_matrix = None
X = None

@app.on_event("startup")
def load_data():
    global grouped_df, vectorizer, similarity_matrix, X
    # Load and prepare data
    all_sf_data = pd.concat([pd.read_csv('../archive/sf_aliens.csv').assign(type='aliens'),
                             pd.read_csv('../archive/sf_alternate_history.csv').assign(type='history'),
                             pd.read_csv('../archive/sf_alternate_universe.csv').assign(type='universe'),
                             pd.read_csv('../archive/sf_apocalyptic.csv').assign(type='apocalyptic'),
                             pd.read_csv('../archive/sf_cyberpunk.csv').assign(type='cyberpunk'),
                             pd.read_csv('../archive/sf_dystopia.csv').assign(type='dystopia'),
                             pd.read_csv('../archive/sf_military.csv').assign(type='military'),
                             pd.read_csv('../archive/sf_robots.csv').assign(type='robots'),
                             pd.read_csv('../archive/sf_space_opera.csv').assign(type='space opera'),
                             pd.read_csv('../archive/sf_steampunk.csv').assign(type='steampunk'),
                             pd.read_csv('../archive/sf_time_travel.csv').assign(type='time travel')], ignore_index=True)

    grouped_df = all_sf_data.groupby('Book_Title').agg({
        'Book_Description': 'first',
        'Rating_score': 'first',
        'type': lambda x: ', '.join(sorted(set(x)))
    }).reset_index()
    
    grouped_df = grouped_df.dropna().reset_index(drop=True)
    
    # Calculate TF-IDF matrix and similarity matrix
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(grouped_df['Book_Description'])
    similarity_matrix = X.dot(X.T).toarray()

@app.get("/query")
def query_route(query: str = Query(..., description="Search query"),
                type_filter: str = Query(None, description="Comma-separated list of types to filter by")):
    global X, vectorizer, grouped_df

    # Process type filter
    type_filter_list = type_filter.split(",") if type_filter else None
    
    # Perform search
    results = search_books(query, X, vectorizer, grouped_df, top_n=10, type_filter=type_filter_list)

    # Prepare the response
    response = {
        "results": [
            {
                "title": row['Book_Title'],
                "Description": row['Book_Description'],  # First 500 words
                "Rating": row['Rating'],
                "Genere": row['Type'],
                "relevance": row['Relevance']
            }
            for _, row in results.iterrows()
        ],
        "message": "OK"
    }
    return response

@app.get("/recommend")
def recommend_route(book_title: str = Query(..., description="Book title to base recommendations on"),
                    type_filter: str = Query(None, description="Comma-separated list of types to filter by"),
                    top_n: int = Query(5, description="Number of recommendations to return")):
    global grouped_df, similarity_matrix

    # Process type filter
    type_filter_list = type_filter.split(",") if type_filter else None
    
    # Perform recommendation
    recommendations = recommend_books(book_title, grouped_df, similarity_matrix, top_n=top_n, type_filter=type_filter_list)
    
    # Prepare the response
    response = {
        "results": [
            {
                "title": row['Book_Title'],
                "Description": row['Book_Description'],  # First 500 words
                "Rating": row['Rating'],
                "Genere": row['Type'],
                "similarity": row['Similarity']
            }
            for _, row in recommendations.iterrows()
        ],
        "message": "OK"
    }
    return response

def search_books(query, X, vectorizer, grouped_df, top_n=10, type_filter=None):
    query_vec = vectorizer.transform([query])
    relevance_scores = X.dot(query_vec.T).toarray().flatten()

    valid_indices = [i for i, score in enumerate(relevance_scores) if score > 0]
    
    if type_filter:
        # Get indices where the type matches the filter and relevance is greater than 0
        filtered_indices = [
            i for i in valid_indices if any(t in grouped_df.iloc[i]['type'] for t in type_filter)
        ]
    else:
        filtered_indices = valid_indices

    # Sort the filtered indices based on relevance scores and take top N
    filtered_scores = [(i, relevance_scores[i]) for i in filtered_indices]
    filtered_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Limit results to top N
    final_indices = [idx for idx, score in filtered_scores[:top_n]]
    
    results = pd.DataFrame({
        'Book_Title': grouped_df.iloc[final_indices]['Book_Title'],
        'Book_Description': grouped_df.iloc[final_indices]['Book_Description'],
        'Rating': grouped_df.iloc[final_indices]['Rating_score'],
        'Type': grouped_df.iloc[final_indices]['type'],
        'Relevance': relevance_scores[final_indices]
    })
    
    return results

def recommend_books(book_title, grouped_df, similarity_matrix, top_n=5, type_filter=None):
    book_idx = grouped_df.index[grouped_df['Book_Title'] == book_title].tolist()[0]
    similarity_scores = similarity_matrix[book_idx]
    similarity_scores[book_idx] = 0
    
    if type_filter:
        filtered_indices = grouped_df[grouped_df['type'].apply(lambda x: any(t in x for t in type_filter))].index.tolist()
        filtered_scores = [(idx, similarity_scores[idx]) for idx in filtered_indices]
        filtered_scores.sort(key=lambda x: x[1], reverse=True)
        final_indices = [idx for idx, score in filtered_scores[:top_n]]
    else:
        final_indices = similarity_scores.argsort()[::-1][1:top_n+1]
    
    results = pd.DataFrame({
        'Book_Title': grouped_df.iloc[final_indices]['Book_Title'],
        'Book_Description': grouped_df.iloc[final_indices]['Book_Description'],
        'Rating': grouped_df.iloc[final_indices]['Rating_score'],
        'Type': grouped_df.iloc[final_indices]['type'],
        'Similarity': similarity_scores[final_indices]
    })
    
    return results

def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
