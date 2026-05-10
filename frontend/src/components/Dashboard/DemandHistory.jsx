import { useState, useEffect } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import { getDemand } from "../../services/api";

export default function DemandHistory({ route }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getDemand(route).then((records) => {
      // Aggregate by hour
      const byHour = {};
      records.forEach((r) => {
        const hour = new Date(r.timestamp).getHours();
        byHour[hour] = (byHour[hour] || 0) + r.passenger_count;
      });
      setData(
        Object.entries(byHour)
          .sort(([a], [b]) => a - b)
          .map(([hour, count]) => ({ hour: `${hour}:00`, count }))
      );
    }).finally(() => setLoading(false));
  }, [route]);

  if (loading) return <div><h2>Historical Demand by Hour</h2><p style={{ color: "#6b7280" }}>Loading history...</p></div>;

  return (
    <div>
      <h2>Historical Demand by Hour</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="hour" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#2563eb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
