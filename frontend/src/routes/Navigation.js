import { Routes, Route, Navigate } from 'react-router-dom';

import { AdminLayout, AuthLayout, ClientLayout } from '../layouts';
import {
  Login,
  Dashboard,
  Empresas,
  Productos,
  Inventario,
  Blockchain,
  Chatbot,
  Usuarios,
  Home,
} from '../pages';

export function Navigation() {
  return (
    <Routes>
      {/* Rutas públicas */}
      <Route
        path="/"
        element={
          <ClientLayout>
            <Home />
          </ClientLayout>
        }
      />

      {/* Ruta de login */}
      <Route
        path="/login"
        element={
          <AuthLayout>
            <Login />
          </AuthLayout>
        }
      />

      {/* Rutas de administración (protegidas) */}
      <Route
        path="/admin"
        element={
          <AdminLayout>
            <Dashboard />
          </AdminLayout>
        }
      />
      <Route
        path="/admin/empresas"
        element={
          <AdminLayout>
            <Empresas />
          </AdminLayout>
        }
      />
      <Route
        path="/admin/productos"
        element={
          <AdminLayout>
            <Productos />
          </AdminLayout>
        }
      />
      <Route
        path="/admin/inventario"
        element={
          <AdminLayout>
            <Inventario />
          </AdminLayout>
        }
      />
      <Route
        path="/admin/blockchain"
        element={
          <AdminLayout>
            <Blockchain />
          </AdminLayout>
        }
      />
      <Route
        path="/admin/chatbot"
        element={
          <AdminLayout>
            <Chatbot />
          </AdminLayout>
        }
      />
      <Route
        path="/admin/usuarios"
        element={
          <AdminLayout>
            <Usuarios />
          </AdminLayout>
        }
      />

      {/* Ruta 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
