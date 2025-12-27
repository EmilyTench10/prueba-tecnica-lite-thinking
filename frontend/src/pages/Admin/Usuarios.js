import { useState, useEffect } from 'react';
import { Box, Dialog, DialogTitle, DialogContent, DialogActions, Chip, Divider } from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import AddIcon from '@mui/icons-material/Add';

import { Typography, Button } from '../../components/atoms';
import { FormField, ConfirmDialog, SearchBar } from '../../components/molecules';
import { DataTable } from '../../components/organisms';
import { Select } from '../../components/atoms/Select';
import { BASE_API_URL } from '../../utils/constants';
import { getToken } from '../../api/token';

const columns = [
  { id: 'email', label: 'Email', minWidth: 200 },
  { id: 'first_name', label: 'Nombre', minWidth: 120 },
  { id: 'last_name', label: 'Apellido', minWidth: 120 },
  {
    id: 'role',
    label: 'Rol',
    minWidth: 100,
    format: (v) => (
      <Chip
        label={v === 'admin' ? 'Admin' : 'Externo'}
        color={v === 'admin' ? 'secondary' : 'default'}
        size="small"
      />
    ),
  },
  {
    id: 'is_active',
    label: 'Estado',
    minWidth: 80,
    format: (v) => (
      <Chip
        label={v ? 'Activo' : 'Inactivo'}
        color={v ? 'success' : 'error'}
        size="small"
      />
    ),
  },
];

const validationSchema = Yup.object({
  email: Yup.string().email('Email inválido').required('El email es requerido'),
  password: Yup.string().min(6, 'Mínimo 6 caracteres'),
  first_name: Yup.string(),
  last_name: Yup.string(),
  role: Yup.string().required('El rol es requerido'),
});

export function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [filteredUsuarios, setFilteredUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingUsuario, setEditingUsuario] = useState(null);
  const [deleteDialog, setDeleteDialog] = useState({ open: false, usuario: null });
  const [viewDialog, setViewDialog] = useState({ open: false, usuario: null });

  useEffect(() => {
    loadUsuarios();
  }, []);

  const loadUsuarios = async () => {
    try {
      const response = await fetch(`${BASE_API_URL}users/`, {
        headers: {
          Authorization: `Bearer ${getToken()}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUsuarios(data);
        setFilteredUsuarios(data);
      }
    } catch (error) {
      toast.error('Error al cargar usuarios');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    const filtered = usuarios.filter(
      (u) =>
        u.email.toLowerCase().includes(query.toLowerCase()) ||
        u.first_name?.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredUsuarios(filtered);
  };

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      role: 'externo',
      is_active: true,
    },
    validationSchema,
    onSubmit: async (values, { setSubmitting, resetForm }) => {
      try {
        const data = { ...values };
        if (!data.password) delete data.password;

        const url = editingUsuario
          ? `${BASE_API_URL}users/${editingUsuario.id}/`
          : `${BASE_API_URL}users/`;

        const response = await fetch(url, {
          method: editingUsuario ? 'PUT' : 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${getToken()}`,
          },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          toast.success(editingUsuario ? 'Usuario actualizado' : 'Usuario creado');
          resetForm();
          setOpenDialog(false);
          setEditingUsuario(null);
          loadUsuarios();
        } else {
          const error = await response.json();
          toast.error(error.detail || 'Error al guardar usuario');
        }
      } catch (error) {
        toast.error('Error al guardar usuario');
      } finally {
        setSubmitting(false);
      }
    },
  });

  const handleEdit = (usuario) => {
    setEditingUsuario(usuario);
    formik.setValues({
      email: usuario.email,
      password: '',
      first_name: usuario.first_name || '',
      last_name: usuario.last_name || '',
      role: usuario.role,
      is_active: usuario.is_active,
    });
    setOpenDialog(true);
  };

  const handleDelete = async () => {
    try {
      const response = await fetch(`${BASE_API_URL}users/${deleteDialog.usuario.id}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${getToken()}`,
        },
      });

      if (response.ok) {
        toast.success('Usuario eliminado');
        setDeleteDialog({ open: false, usuario: null });
        loadUsuarios();
      }
    } catch (error) {
      toast.error('Error al eliminar usuario');
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingUsuario(null);
    formik.resetForm();
  };

  const handleView = (usuario) => {
    setViewDialog({ open: true, usuario });
  };

  const roleOptions = [
    { value: 'admin', label: 'Administrador' },
    { value: 'externo', label: 'Externo' },
  ];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Usuarios</Typography>
        <Button startIcon={<AddIcon />} onClick={() => setOpenDialog(true)}>
          Nuevo Usuario
        </Button>
      </Box>

      <Box sx={{ mb: 3, maxWidth: 400 }}>
        <SearchBar placeholder="Buscar por email o nombre..." onSearch={handleSearch} />
      </Box>

      <DataTable
        columns={columns}
        data={filteredUsuarios}
        loading={loading}
        onView={handleView}
        onEdit={handleEdit}
        onDelete={(usuario) => setDeleteDialog({ open: true, usuario })}
        showActions={true}
        emptyMessage="No hay usuarios registrados"
      />

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth disableRestoreFocus>
        <DialogTitle>
          {editingUsuario ? 'Editar Usuario' : 'Nuevo Usuario'}
        </DialogTitle>
        <Box component="form" onSubmit={formik.handleSubmit}>
          <DialogContent>
            <FormField
              name="email"
              label="Email"
              type="email"
              formik={formik}
              required
            />
            <FormField
              name="password"
              label={editingUsuario ? 'Nueva contraseña (opcional)' : 'Contraseña'}
              type="password"
              formik={formik}
              required={!editingUsuario}
            />
            <FormField name="first_name" label="Nombre" formik={formik} />
            <FormField name="last_name" label="Apellido" formik={formik} />
            <Box sx={{ mb: 2 }}>
              <Select
                name="role"
                label="Rol"
                value={formik.values.role}
                onChange={formik.handleChange}
                options={roleOptions}
                required
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} color="inherit">
              Cancelar
            </Button>
            <Button type="submit" loading={formik.isSubmitting}>
              {editingUsuario ? 'Actualizar' : 'Crear'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>

      {/* Dialog para ver detalles */}
      <Dialog
        open={viewDialog.open}
        onClose={() => setViewDialog({ open: false, usuario: null })}
        maxWidth="sm"
        fullWidth
        disableRestoreFocus
      >
        <DialogTitle>Detalles del Usuario</DialogTitle>
        <DialogContent>
          {viewDialog.usuario && (
            <Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Email</Typography>
                <Typography variant="body1">{viewDialog.usuario.email}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Nombre</Typography>
                <Typography variant="body1">
                  {viewDialog.usuario.first_name || 'No especificado'} {viewDialog.usuario.last_name || ''}
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Rol</Typography>
                <Chip
                  label={viewDialog.usuario.role === 'admin' ? 'Administrador' : 'Externo'}
                  color={viewDialog.usuario.role === 'admin' ? 'secondary' : 'default'}
                  size="small"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Estado</Typography>
                <Chip
                  label={viewDialog.usuario.is_active ? 'Activo' : 'Inactivo'}
                  color={viewDialog.usuario.is_active ? 'success' : 'error'}
                  size="small"
                />
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialog({ open: false, usuario: null })}>
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteDialog.open}
        title="Eliminar Usuario"
        message={`¿Está seguro de eliminar el usuario ${deleteDialog.usuario?.email}?`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteDialog({ open: false, usuario: null })}
        confirmColor="error"
      />
    </Box>
  );
}
