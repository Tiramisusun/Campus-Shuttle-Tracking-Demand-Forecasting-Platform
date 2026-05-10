import { useEffect, useState } from "react";
import { io } from "socket.io-client";

const SOCKET_URL = import.meta.env.VITE_API_URL?.replace("/api", "") || "http://localhost:5000";

export function useVehicleLocations() {
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => {
    const socket = io(SOCKET_URL);

    socket.on("vehicle_update", (data) => {
      setVehicles((prev) =>
        prev.map((v) => (v.id === data.id ? { ...v, lat: data.lat, lng: data.lng } : v))
      );
    });

    socket.on("vehicles_initial", (data) => setVehicles(data));

    return () => socket.disconnect();
  }, []);

  return vehicles;
}
