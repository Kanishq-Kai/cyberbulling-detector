import axios from "axios";

const BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

const api = axios.create({ baseURL: BASE, timeout: 15000 });

export const predictToxicity = (text) =>
  api.post("/predict", { text }).then((r) => r.data);

export const getHistory = (page = 1, perPage = 20) =>
  api.get("/history", { params: { page, per_page: perPage } }).then((r) => r.data);

export const getAnalytics = () =>
  api.get("/analytics").then((r) => r.data);

export const rewriteComment = (text) =>
  api.post("/rewrite-comment", { text }).then((r) => r.data);

export const healthCheck = () =>
  api.get("/health").then((r) => r.data);

export default api;
