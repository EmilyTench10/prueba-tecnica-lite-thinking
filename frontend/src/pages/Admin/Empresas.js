import { useState, useEffect } from 'react';
import { Box, Dialog, DialogTitle, DialogContent, DialogActions, Divider } from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import AddIcon from '@mui/icons-material/Add';

import { Typography, Button } from '../../components/atoms';
import { FormField, ConfirmDialog, SearchBar } from '../../components/molecules';
import { DataTable } from '../../components/organisms';
import { useAuth } from '../../hooks/useAuth';
import {
  getEmpresasApi,
  createEmpresaApi,
  updateEmpresaApi,
  deleteEmpresaApi,
} from '../../api/empresas';

const columns = [
  { id: 'nit', label: 'NIT', minWidth: 120 },
  { id: 'nombre', label: 'Nombre', minWidth: 200 },
  { id: 'direccion', label: 'Dirección', minWidth: 200 },
  { id: 'telefono', label: 'Teléfono', minWidth: 120 },
];

const validationSchema = Yup.object({
  nit: Yup.string().required('El NIT es requerido'),
  nombre: Yup.string().required('El nombre es requerido'),
  direccion: Yup.string().required('La dirección es requerida'),
  telefono: Yup.string().required('El teléfono es requerido'),
});

export function Empresas() {
  const { auth } = useAuth();
  const isAdmin = auth?.user?.role === 'admin' || auth?.user?.is_superuser;

  const [empresas, setEmpresas] = useState([]);
  const [filteredEmpresas, setFilteredEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingEmpresa, setEditingEmpresa] = useState(null);
  const [deleteDialog, setDeleteDialog] = useState({ open: false, empresa: null });
  const [viewDialog, setViewDialog] = useState({ open: false, empresa: null });

  useEffect(() => {
    loadEmpresas();
  }, []);

  const loadEmpresas = async () => {
    try {
      const data = await getEmpresasApi();
      setEmpresas(data);
      setFilteredEmpresas(data);
    } catch (error) {
      toast.error('Error al cargar empresas');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    const filtered = empresas.filter(
      (e) =>
        e.nit.toLowerCase().includes(query.toLowerCase()) ||
        e.nombre.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredEmpresas(filtered);
  };

  const formik = useFormik({
    initialValues: {
      nit: '',
      nombre: '',
      direccion: '',
      telefono: '',
    },
    validationSchema,
    onSubmit: async (values, { setSubmitting, resetForm }) => {
      try {
        if (editingEmpresa) {
          await updateEmpresaApi(editingEmpresa.nit, values);
          toast.success('Empresa actualizada correctamente');
        } else {
          await createEmpresaApi(values);
          toast.success('Empresa creada correctamente');
        }
        resetForm();
        setOpenDialog(false);
        setEditingEmpresa(null);
        loadEmpresas();
      } catch (error) {
        toast.error(error.message);
      } finally {
        setSubmitting(false);
      }
    },
  });

  const handleEdit = (empresa) => {
    setEditingEmpresa(empresa);
    formik.setValues({
      nit: empresa.nit,
      nombre: empresa.nombre,
      direccion: empresa.direccion,
      telefono: empresa.telefono,
    });
    setOpenDialog(true);
  };

  const handleDelete = async () => {
    try {
      await deleteEmpresaApi(deleteDialog.empresa.nit);
      toast.success('Empresa eliminada correctamente');
      setDeleteDialog({ open: false, empresa: null });
      loadEmpresas();
    } catch (error) {
      toast.error('Error al eliminar empresa');
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingEmpresa(null);
    formik.resetForm();
  };

  const handleView = (empresa) => {
    setViewDialog({ open: true, empresa });
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Empresas</Typography>
        {isAdmin && (
          <Button startIcon={<AddIcon />} onClick={() => setOpenDialog(true)}>
            Nueva Empresa
          </Button>
        )}
      </Box>

      <Box sx={{ mb: 3, maxWidth: 400 }}>
        <SearchBar placeholder="Buscar por NIT o nombre..." onSearch={handleSearch} />
      </Box>

      <DataTable
        columns={columns}
        data={filteredEmpresas}
        loading={loading}
        onView={handleView}
        onEdit={isAdmin ? handleEdit : null}
        onDelete={isAdmin ? (empresa) => setDeleteDialog({ open: true, empresa }) : null}
        showActions={true}
        emptyMessage="No hay empresas registradas"
      />

      {/* Dialog para crear/editar */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth disableRestoreFocus>
        <DialogTitle>
          {editingEmpresa ? 'Editar Empresa' : 'Nueva Empresa'}
        </DialogTitle>
        <Box component="form" onSubmit={formik.handleSubmit}>
          <DialogContent>
            <FormField
              name="nit"
              label="NIT"
              formik={formik}
              required
              disabled={!!editingEmpresa}
            />
            <FormField name="nombre" label="Nombre de la empresa" formik={formik} required />
            <FormField name="direccion" label="Dirección" formik={formik} required />
            <FormField name="telefono" label="Teléfono" formik={formik} required />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} color="inherit">
              Cancelar
            </Button>
            <Button type="submit" loading={formik.isSubmitting}>
              {editingEmpresa ? 'Actualizar' : 'Crear'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>

      {/* Dialog para ver detalles */}
      <Dialog
        open={viewDialog.open}
        onClose={() => setViewDialog({ open: false, empresa: null })}
        maxWidth="sm"
        fullWidth
        disableRestoreFocus
      >
        <DialogTitle>Detalles de la Empresa</DialogTitle>
        <DialogContent>
          {viewDialog.empresa && (
            <Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">NIT</Typography>
                <Typography variant="body1">{viewDialog.empresa.nit}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Nombre</Typography>
                <Typography variant="body1">{viewDialog.empresa.nombre}</Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Dirección</Typography>
                <Typography variant="body1">{viewDialog.empresa.direccion}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Teléfono</Typography>
                <Typography variant="body1">{viewDialog.empresa.telefono}</Typography>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialog({ open: false, empresa: null })}>
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Confirmación de eliminación */}
      <ConfirmDialog
        open={deleteDialog.open}
        title="Eliminar Empresa"
        message={`¿Está seguro de eliminar la empresa ${deleteDialog.empresa?.nombre}?`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteDialog({ open: false, empresa: null })}
        confirmColor="error"
      />
    </Box>
  );
}
