from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Frontend'in (localhost:5173) backend'e istek atabilmesi için CORS izni
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# CSV'yi uygulama başlarken bir kere hafızaya yükle
df = pd.read_csv("../data/universal_top_spotify_songs.csv")

@app.get("/")
def root():
    return {"message": "Spotify Trend Intelligence API"}

@app.get("/top-tracks")
def top_tracks(country: str = "TR", limit: int = 10):
    filtered = df[df["country"] == country]
    latest_date = filtered["snapshot_date"].max()
    latest = filtered[filtered["snapshot_date"] == latest_date]
    latest = latest.sort_values("daily_rank").head(limit)

    result = latest[["daily_rank", "name", "artists", "popularity"]].to_dict(orient="records")
    return {"country": country, "date": latest_date, "tracks": result}