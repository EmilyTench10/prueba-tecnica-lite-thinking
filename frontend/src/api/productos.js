import { BASE_API_URL } from '../utils/constants';
import { getToken } from './token';

const getHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

export async function getProductosApi() {
  const response = await fetch(`${BASE_API_URL}productos/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener productos');
  return response.json();
}

export async function getProductoApi(id) {
  const response = await fetch(`${BASE_API_URL}productos/${id}/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener producto');
  return response.json();
}

export async function getProductosPorEmpresaApi(nit) {
  const response = await fetch(`${BASE_API_URL}productos/por_empresa/?nit=${nit}`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener productos');
  return response.json();
}

export async function createProductoApi(data) {
  const response = await fetch(`${BASE_API_URL}productos/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al crear producto');
  }
  return response.json();
}

export async function updateProductoApi(id, data) {
  const response = await fetch(`${BASE_API_URL}productos/${id}/`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Error al actualizar producto');
  return response.json();
}

export async function deleteProductoApi(id) {
  const response = await fetch(`${BASE_API_URL}productos/${id}/`, {
    method: 'DELETE',
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al eliminar producto');
  return true;
}
