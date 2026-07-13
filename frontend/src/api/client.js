import axios from 'axios';

// Base URL for the FastAPI backend. Falls back to local dev default so the
// app still works if a teammate forgets to set up their .env file.
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL,
  timeout: 30000,
});

/**
 * POST /upload/report — send a selected medical report PDF to the backend.
 * Returns { status, data: { report, patient, lab_values } } (Member 2's route).
 */
export function uploadReport(file) {
  const formData = new FormData();
  formData.append('file', file);
  // Let axios set the multipart Content-Type (with boundary) itself.
  return api.post('/upload/report', formData).then((res) => res.data);
}

/**
 * POST /predict — disease risk prediction.
 * Body: { disease, patient, lab_values, manual_values }.
 * Returns either { status: 'needs_user_input', missing_features, mapped_features }
 * or { status: 'success', prediction, risk, confidence, key_factors, ai_summary }.
 */
export function predictDisease(payload) {
  return api.post('/predict', payload).then((res) => res.data);
}

/**
 * GET /predict/features/:disease — full feature spec (used to render a blank
 * manual-entry form when there's no report to pre-fill from).
 */
export function getFeatureSpecs(disease) {
  return api.get(`/predict/features/${disease}`).then((res) => res.data);
}

/**
 * POST /chat/ — medical Q&A / symptom chat (GenAI engineer's RAG + Gemini,
 * with a dummy fallback in the backend). Shape: { question } -> { answer, sources }.
 */
export function sendChatMessage(question) {
  return api.post('/chat/', { question }).then((res) => res.data);
}

/**
 * GET /history — prediction history for the Dashboard.
 */
export function getHistory() {
  return api.get('/history').then((res) => res.data);
}

export default api;
