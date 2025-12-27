import { BASE_API_URL } from '../utils/constants';
import { getToken } from './token';

const getHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

export async function getEmpresasApi() {
  const response = await fetch(`${BASE_API_URL}empresas/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener empresas');
  return response.json();
}

export async function getEmpresaApi(nit) {
  const response = await fetch(`${BASE_API_URL}empresas/${nit}/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener empresa');
  return response.json();
}

export async function createEmpresaApi(data) {
  const response = await fetch(`${BASE_API_URL}empresas/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al crear empresa');
  }
  return response.json();
}

export async function updateEmpresaApi(nit, data) {
  const response = await fetch(`${BASE_API_URL}empresas/${nit}/`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Error al actualizar empresa');
  return response.json();
}

export async function deleteEmpresaApi(nit) {
  const response = await fetch(`${BASE_API_URL}empresas/${nit}/`, {
    method: 'DELETE',
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al eliminar empresa');
  return true;
}
