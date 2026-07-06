import axios from 'axios';

// Base URL for the FastAPI backend. Falls back to local dev default so the
// app still works if a teammate forgets to set up their .env file.
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL,
  timeout: 10000,
});

/**
 * POST /predict — disease risk prediction (dummy response for now).
 * Real implementation lives in backend/ml/ (owned by the ML engineer).
 */
export function predictDisease(payload) {
  return api.post('/predict', payload).then((res) => res.data);
}

/**
 * POST /chat — medical Q&A / symptom chat (dummy response for now).
 * Real implementation lives in backend/rag/ (owned by the GenAI engineer).
 */
export function sendChatMessage(payload) {
  return api.post('/chat', payload).then((res) => res.data);
}

export default api;
