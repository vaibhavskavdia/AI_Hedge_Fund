import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ??
    "https://web-production-9837e.up.railway.app",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000,
});

export default api;