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
blob_client = container_client.get_blob_client("universal_top_spotify_songs.csv")

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