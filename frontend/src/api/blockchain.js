import { BASE_API_URL } from '../utils/constants';
import { getToken } from './token';

const getHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

export async function getBlockchainApi() {
  const response = await fetch(`${BASE_API_URL}blockchain/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener blockchain');
  return response.json();
}

export async function verificarBlockchainApi() {
  const response = await fetch(`${BASE_API_URL}blockchain/verificar/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al verificar blockchain');
  return response.json();
}

export async function getEstadisticasBlockchainApi() {
  const response = await fetch(`${BASE_API_URL}blockchain/estadisticas/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener estadísticas');
  return response.json();
}
