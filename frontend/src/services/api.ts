import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ??
    "https://aihedgefund-production.up.railway.app",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000,
});

export default api;