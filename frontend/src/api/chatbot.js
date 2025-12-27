import { BASE_API_URL } from '../utils/constants';
import { getToken } from './token';

const getHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

export async function sendMessageApi(message, sessionId = null) {
  const body = { message };
  if (sessionId) {
    body.session_id = sessionId;
  }

  const response = await fetch(`${BASE_API_URL}chatbot/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    console.error('Chatbot API error:', response.status, error);
    throw new Error(error.detail || error.error || 'Error al enviar mensaje');
  }
  return response.json();
}

export async function getChatHistorialApi(sessionId) {
  const response = await fetch(`${BASE_API_URL}chatbot/historial/${sessionId}/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener historial');
  return response.json();
}
