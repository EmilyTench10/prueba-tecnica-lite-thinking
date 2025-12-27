import { BASE_API_URL } from '../utils/constants';
import { getToken } from './token';

const getHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

export async function getInventarioApi() {
  const response = await fetch(`${BASE_API_URL}inventario/`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener inventario');
  return response.json();
}

export async function getInventarioPorEmpresaApi(nit) {
  const response = await fetch(`${BASE_API_URL}inventario/por_empresa/?nit=${nit}`, {
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al obtener inventario');
  return response.json();
}

export async function createInventarioApi(data) {
  const response = await fetch(`${BASE_API_URL}inventario/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al crear inventario');
  }
  return response.json();
}

export async function updateInventarioApi(id, data) {
  const response = await fetch(`${BASE_API_URL}inventario/${id}/`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Error al actualizar inventario');
  return response.json();
}

export async function deleteInventarioApi(id) {
  const response = await fetch(`${BASE_API_URL}inventario/${id}/`, {
    method: 'DELETE',
    headers: getHeaders(),
  });

  if (!response.ok) throw new Error('Error al eliminar inventario');
  return true;
}

export function getDescargarPdfUrl(nit = null) {
  const base = `${BASE_API_URL}inventario/descargar-pdf/`;
  return nit ? `${base}?nit=${nit}` : base;
}

export async function enviarPdfEmailApi(email, empresaNit = null) {
  const response = await fetch(`${BASE_API_URL}inventario/enviar-pdf/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ email, empresa_nit: empresaNit }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al enviar PDF');
  }
  return response.json();
}
