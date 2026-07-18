import axios from 'axios';

// Base URL for the FastAPI backend. Falls back to local dev default so the
// app still works if a teammate forgets to set up their .env file.
const baseURL = import.meta.env.VITE_API_BASE_URL || 'https://medintel-ai-k39i.onrender.com';

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
 * POST /chat/ — medical Q&A / symptom chat.
 * Backed by the GenAI engineer's RAG + Gemini pipeline in backend/rag/,
 * with an automatic dummy fallback (see backend/main.py) while that isn't
 * configured locally. Request/response shape: { question } -> { answer, sources }.
 */
export function sendChatMessage(question) {
  return api.post('/chat/', { question }).then((res) => res.data);
}

/**
 * POST /upload — send a selected medical report PDF to the backend.
 * Placeholder response for now (backend/routers/upload.py) — real PDF
 * parsing belongs to backend/pdf_processing/ and isn't implemented yet.
 */
export function uploadReport(file) {
  const formData = new FormData();
  formData.append('file', file);
  // Let axios set the multipart Content-Type (with boundary) itself.
  return api.post('/upload', formData).then((res) => res.data);
}

/**
 * GET /history — prediction history for the Dashboard.
 * Placeholder data for now (backend/routers/history.py) — real persistence
 * belongs to backend/database/ (MongoDB) and isn't implemented yet.
 */
export function getHistory() {
  return api.get('/history').then((res) => res.data);
}

export default api;
