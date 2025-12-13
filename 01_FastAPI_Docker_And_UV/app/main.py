from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd


app = FastAPI()

desc_vectorizer = joblib.load("artifacts/vectorizer.pkl")
knn = joblib.load("artifacts/knn.pkl")
df = pd.read_csv("dataset/movies.csv")


def recommend_movies(id, no_of_movies=5):
    match = df.loc[df['id'] == id]
    if match.empty:
        return []

    row = match.iloc[0]
    query_vector = desc_vectorizer.transform([row['description']])
    distances, indices = knn.kneighbors(query_vector, n_neighbors=no_of_movies+1)
    distances = distances[0][1:]
    idxs = indices[0][1:]
    confidences = 1 / (1 + distances)
    recs = df.iloc[idxs][['id', 'title']].copy()
    recs['confidence'] = confidences.round(2)
    return recs.to_dict(orient='records')


@app.get("/recommad")
async def recommend(movie_id: int, no_of_recommendations: int = 10):
    try:
        return recommend_movies(movie_id, no_of_recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
