import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api",
});

export const getVehicles = () => api.get("/vehicles/").then(r => r.data);
export const getSchedules = (route) => api.get("/schedules/", { params: { route } }).then(r => r.data);
export const bookSeat = (scheduleId) => api.post(`/schedules/${scheduleId}/book`).then(r => r.data);
export const getDemand = (route) => api.get("/demand/", { params: { route } }).then(r => r.data);
export const getForecast = (route, periods = 12) =>
  api.get("/forecast/", { params: { route, periods } }).then(r => r.data);
