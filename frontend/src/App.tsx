import { useEffect, useState } from "react";

interface Track {
  daily_rank: number;
  name: string;
  artists: string;
  popularity: number;
}

interface ApiResponse {
  country: string;
  date: string;
  tracks: Track[];
}

function App() {
  const [data, setData] = useState<ApiResponse | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/top-tracks?country=TR")
      .then((res) => res.json())
      .then((json) => setData(json));
  }, []);

  if (!data) return <p>Yükleniyor...</p>;

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Türkiye Top 10 ({data.date})</h1>
      <ol>
        {data.tracks.map((track) => (
          <li key={track.daily_rank}>
            <strong>{track.name}</strong> — {track.artists} (popülerlik: {track.popularity})
          </li>
        ))}
      </ol>
    </div>
  );
}

export default App;