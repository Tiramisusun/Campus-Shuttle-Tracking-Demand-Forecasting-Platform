import { useState, useEffect } from "react";
import { getSchedules, bookSeat } from "../../services/api";

function Toast({ message, type }) {
  if (!message) return null;
  const bg = type === "success" ? "#16a34a" : "#dc2626";
  return (
    <div style={{
      position: "fixed", bottom: 24, right: 24,
      background: bg, color: "#fff",
      padding: "12px 20px", borderRadius: 8,
      boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
      zIndex: 1000, fontSize: 14,
    }}>
      {message}
    </div>
  );
}

export default function ScheduleList({ route }) {
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    setLoading(true);
    getSchedules(route)
      .then(setSchedules)
      .finally(() => setLoading(false));
  }, [route]);

  const showToast = (message, type) => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleBook = async (id) => {
    try {
      const res = await bookSeat(id);
      setSchedules((prev) =>
        prev.map((s) => (s.id === id ? { ...s, available_seats: res.remaining_seats } : s))
      );
      showToast("Seat booked successfully!", "success");
    } catch {
      showToast("Booking failed — no seats available.", "error");
    }
  };

  return (
    <div>
      <h2>Schedules — {route}</h2>
      {loading ? (
        <p style={{ color: "#6b7280" }}>Loading schedules...</p>
      ) : schedules.length === 0 ? (
        <p style={{ color: "#6b7280" }}>No schedules found for this route.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Route</th>
              <th>Departure</th>
              <th>Seats</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {schedules.map((s) => (
              <tr key={s.id}>
                <td>{s.route}</td>
                <td>{new Date(s.departure_time).toLocaleTimeString()}</td>
                <td>{s.available_seats}</td>
                <td>
                  <button onClick={() => handleBook(s.id)} disabled={s.available_seats === 0}>
                    {s.available_seats === 0 ? "Full" : "Book"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <Toast message={toast?.message} type={toast?.type} />
    </div>
  );
}
