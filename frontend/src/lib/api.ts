import axios, { type AxiosInstance } from "axios";
import { getIdToken } from "./firebase";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api/academy";

export const api: AxiosInstance = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(async (config) => {
  const token = await getIdToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
