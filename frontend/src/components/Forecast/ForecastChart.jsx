import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import { getForecast } from "../../services/api";

export default function ForecastChart({ route }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getForecast(route)
      .then((records) =>
        setData(
          records.map((r) => ({
            time: new Date(r.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            predicted: Math.round(r.predicted),
            upper: Math.round(r.upper_bound),
            lower: Math.round(r.lower_bound),
          }))
        )
      )
      .finally(() => setLoading(false));
  }, [route]);

  if (loading) return <div><h2>Demand Forecast — next 12 hours</h2><p style={{ color: "#6b7280" }}>Loading forecast...</p></div>;

  return (
    <div>
      <h2>Demand Forecast — next 12 hours</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="predicted" stroke="#2563eb" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="upper" stroke="#93c5fd" strokeDasharray="4 4" dot={false} />
          <Line type="monotone" dataKey="lower" stroke="#93c5fd" strokeDasharray="4 4" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
