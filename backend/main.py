import os
from io import BytesIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Blob Storage'dan CSV'yi indir ve hafızaya yükle
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client("spotify-data")
blob_client = container_client.get_blob_client("tr_top_spotify_songs.csv")

print("Azure'dan veri indiriliyor...")
blob_data = blob_client.download_blob().readall()
df = pd.read_csv(BytesIO(blob_data))
print("Veri yüklendi:", len(df), "satır")

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
@app.get("/top-artists")
def top_artists(country: str = "TR", limit: int = 10):
    filtered = df[df["country"] == country].copy()
    filtered["artists"] = filtered["artists"].astype(str)
    artist_counts = filtered["artists"].value_counts().head(limit)
    result = [{"artist": artist, "count": int(count)} for artist, count in artist_counts.items()]
    return {"country": country, "artists": result}

@app.get("/popularity-trend")
def popularity_trend(country: str = "TR"):
    filtered = df[df["country"] == country].copy()
    trend = filtered.groupby("snapshot_date")["popularity"].mean().reset_index()
    trend = trend.sort_values("snapshot_date")
    result = [{"date": row["snapshot_date"], "avg_popularity": round(row["popularity"], 2)} for _, row in trend.iterrows()]
    return {"country": country, "trend": result}
