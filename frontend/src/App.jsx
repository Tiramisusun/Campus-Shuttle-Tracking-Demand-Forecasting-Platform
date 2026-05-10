import { useState } from "react";
import ShuttleMap from "./components/Map/ShuttleMap";
import ScheduleList from "./components/Schedule/ScheduleList";
import ForecastChart from "./components/Forecast/ForecastChart";
import DemandHistory from "./components/Dashboard/DemandHistory";
import { useVehicleLocations } from "./hooks/useWebSocket";

const ROUTES = ["Main Gate → Library", "Main Gate → Dorm A", "Library → Lab Building"];

export default function App() {
  const [selectedRoute, setSelectedRoute] = useState(ROUTES[0]);
  const vehicles = useVehicleLocations();

  return (
    <div style={{ fontFamily: "sans-serif", maxWidth: 1100, margin: "0 auto", padding: 24 }}>
      <h1>Campus Shuttle Tracker</h1>

      <div style={{ marginBottom: 16 }}>
        <label>Route: </label>
        <select value={selectedRoute} onChange={(e) => setSelectedRoute(e.target.value)}>
          {ROUTES.map((r) => <option key={r}>{r}</option>)}
        </select>
      </div>

      <ShuttleMap vehicles={vehicles} />

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32, marginTop: 32 }}>
        <ScheduleList route={selectedRoute} />
        <ForecastChart route={selectedRoute} />
      </div>

      <div style={{ marginTop: 32 }}>
        <DemandHistory route={selectedRoute} />
      </div>
    </div>
  );
}
