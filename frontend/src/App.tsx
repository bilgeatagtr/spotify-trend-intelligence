import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  LineChart, Line, ResponsiveContainer,
} from "recharts";

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

interface ArtistData {
  artist: string;
  count: number;
}

interface TrendPoint {
  date: string;
  avg_popularity: number;
}

function App() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [artists, setArtists] = useState<ArtistData[]>([]);
  const [trend, setTrend] = useState<TrendPoint[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/top-tracks?country=TR")
      .then((res) => res.json())
      .then((json) => setData(json));

    fetch("http://localhost:8000/top-artists?country=TR")
      .then((res) => res.json())
      .then((json) => setArtists(json.artists));

    fetch("http://localhost:8000/popularity-trend?country=TR")
      .then((res) => res.json())
      .then((json) => setTrend(json.trend));
  }, []);

  if (!data) return <p>Yükleniyor...</p>;

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "900px", margin: "0 auto" }}>
      <h1>Türkiye Top 10 ({data.date})</h1>
      <ol>
        {data.tracks.map((track) => (
          <li key={track.daily_rank}>
            <strong>{track.name}</strong> — {track.artists} (popülerlik: {track.popularity})
          </li>
        ))}
      </ol>

      <h2>En Çok Tekrar Eden Sanatçılar</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={artists}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="artist" angle={-30} textAnchor="end" interval={0} height={80} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#1DB954" />
        </BarChart>
      </ResponsiveContainer>

      <h2>Zaman İçinde Ortalama Popülerlik</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={trend}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" tick={false} />
          <YAxis domain={["auto", "auto"]} />
          <Tooltip />
          <Line type="monotone" dataKey="avg_popularity" stroke="#1DB954" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;