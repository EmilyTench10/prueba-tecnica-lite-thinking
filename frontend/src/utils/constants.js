// Variables de entorno
export const BASE_API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api/';

// Claves de almacenamiento local
export const TOKEN_KEY = 'litethinking_token';
export const REFRESH_TOKEN_KEY = 'litethinking_refresh_token';

export const MONEDAS = [
  { codigo: 'COP', nombre: 'Peso Colombiano', simbolo: '$' },
  { codigo: 'USD', nombre: 'Dólar Estadounidense', simbolo: '$' },
  { codigo: 'EUR', nombre: 'Euro', simbolo: '€' },
  { codigo: 'MXN', nombre: 'Peso Mexicano', simbolo: '$' },
  { codigo: 'BRL', nombre: 'Real Brasileño', simbolo: 'R$' },
  { codigo: 'ARS', nombre: 'Peso Argentino', simbolo: '$' },
  { codigo: 'GBP', nombre: 'Libra Esterlina', simbolo: '£' },
];

export const ROLES = {
  ADMIN: 'admin',
  EXTERNO: 'externo',
};
