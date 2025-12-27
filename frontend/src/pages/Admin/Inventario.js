import { useState, useEffect } from 'react';
import {
  Box, Dialog, DialogTitle, DialogContent, DialogActions,
  Grid, TextField, Divider
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import AddIcon from '@mui/icons-material/Add';
import DownloadIcon from '@mui/icons-material/Download';
import EmailIcon from '@mui/icons-material/Email';

import { Typography, Button } from '../../components/atoms';
import { FormField, SearchBar, ConfirmDialog } from '../../components/molecules';
import { DataTable } from '../../components/organisms';
import { Select } from '../../components/atoms/Select';
import { useAuth } from '../../hooks/useAuth';
import {
  getInventarioApi,
  createInventarioApi,
  updateInventarioApi,
  deleteInventarioApi,
  getDescargarPdfUrl,
  enviarPdfEmailApi,
} from '../../api/inventario';
import { getEmpresasApi } from '../../api/empresas';
import { getProductosApi } from '../../api/productos';

const columns = [
  { id: 'empresa_detail', label: 'Empresa', minWidth: 150, format: (v) => v?.nombre || 'N/A' },
  { id: 'producto_detail', label: 'Producto', minWidth: 150, format: (v) => v?.nombre || 'N/A' },
  { id: 'cantidad', label: 'Cantidad', minWidth: 100 },
  { id: 'ubicacion', label: 'Ubicación', minWidth: 150 },
];

const validationSchema = Yup.object({
  empresa: Yup.string().required('La empresa es requerida'),
  producto: Yup.number().required('El producto es requerido'),
  cantidad: Yup.number().min(0, 'Cantidad inválida').required('La cantidad es requerida'),
});

export function Inventario() {
  const { auth } = useAuth();
  const isAdmin = auth?.user?.role === 'admin' || auth?.user?.is_superuser;

  const [inventario, setInventario] = useState([]);
  const [filteredInventario, setFilteredInventario] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [deleteDialog, setDeleteDialog] = useState({ open: false, item: null });
  const [emailDialog, setEmailDialog] = useState(false);
  const [emailTo, setEmailTo] = useState('');
  const [sendingEmail, setSendingEmail] = useState(false);
  const [viewDialog, setViewDialog] = useState({ open: false, item: null });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [inventarioData, empresasData, productosData] = await Promise.all([
        getInventarioApi(),
        getEmpresasApi(),
        getProductosApi(),
      ]);
      setInventario(inventarioData);
      setFilteredInventario(inventarioData);
      setEmpresas(empresasData);
      setProductos(productosData);
    } catch (error) {
      toast.error('Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    const filtered = inventario.filter(
      (i) =>
        i.empresa_detail?.nombre?.toLowerCase().includes(query.toLowerCase()) ||
        i.producto_detail?.nombre?.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredInventario(filtered);
  };

  const formik = useFormik({
    initialValues: {
      empresa: '',
      producto: '',
      cantidad: 0,
      ubicacion: '',
    },
    validationSchema,
    onSubmit: async (values, { setSubmitting, resetForm }) => {
      try {
        if (editingItem) {
          await updateInventarioApi(editingItem.id, values);
          toast.success('Inventario actualizado correctamente');
        } else {
          await createInventarioApi(values);
          toast.success('Item de inventario creado correctamente');
        }
        resetForm();
        setOpenDialog(false);
        setEditingItem(null);
        loadData();
      } catch (error) {
        toast.error(error.message);
      } finally {
        setSubmitting(false);
      }
    },
  });

  const handleEdit = (item) => {
    setEditingItem(item);
    formik.setValues({
      empresa: item.empresa,
      producto: item.producto,
      cantidad: item.cantidad,
      ubicacion: item.ubicacion || '',
    });
    setOpenDialog(true);
  };

  const handleDelete = async () => {
    try {
      await deleteInventarioApi(deleteDialog.item.id);
      toast.success('Item eliminado correctamente');
      setDeleteDialog({ open: false, item: null });
      loadData();
    } catch (error) {
      toast.error('Error al eliminar item');
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingItem(null);
    formik.resetForm();
  };

  const handleDownloadPdf = () => {
    window.open(getDescargarPdfUrl(), '_blank');
  };

  const handleSendEmail = async () => {
    if (!emailTo) {
      toast.error('Ingrese un email válido');
      return;
    }
    setSendingEmail(true);
    try {
      await enviarPdfEmailApi(emailTo);
      toast.success(`PDF enviado a ${emailTo}`);
      setEmailDialog(false);
      setEmailTo('');
    } catch (error) {
      toast.error('Error al enviar email');
    } finally {
      setSendingEmail(false);
    }
  };

  const handleView = (item) => {
    setViewDialog({ open: true, item });
  };

  const empresaOptions = empresas.map((e) => ({ value: e.nit, label: e.nombre }));
  const productoOptions = productos.map((p) => ({ value: p.id, label: `${p.codigo} - ${p.nombre}` }));

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, flexWrap: 'wrap', gap: 2 }}>
        <Typography variant="h4">Inventario</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={handleDownloadPdf}
          >
            Descargar PDF
          </Button>
          {isAdmin && (
            <>
              <Button
                variant="outlined"
                color="secondary"
                startIcon={<EmailIcon />}
                onClick={() => setEmailDialog(true)}
              >
                Enviar PDF
              </Button>
              <Button startIcon={<AddIcon />} onClick={() => setOpenDialog(true)}>
                Nuevo Item
              </Button>
            </>
          )}
        </Box>
      </Box>

      <Box sx={{ mb: 3, maxWidth: 400 }}>
        <SearchBar placeholder="Buscar por empresa o producto..." onSearch={handleSearch} />
      </Box>

      <DataTable
        columns={columns}
        data={filteredInventario}
        loading={loading}
        onView={handleView}
        onEdit={isAdmin ? handleEdit : null}
        onDelete={isAdmin ? (item) => setDeleteDialog({ open: true, item }) : null}
        showActions={true}
        emptyMessage="No hay items en inventario"
      />

      {/* Dialog para crear/editar */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth disableRestoreFocus>
        <DialogTitle>
          {editingItem ? 'Editar Item' : 'Nuevo Item de Inventario'}
        </DialogTitle>
        <Box component="form" onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Select
                  name="empresa"
                  label="Empresa"
                  value={formik.values.empresa}
                  onChange={formik.handleChange}
                  options={empresaOptions}
                  error={formik.touched.empresa && Boolean(formik.errors.empresa)}
                  helperText={formik.touched.empresa && formik.errors.empresa}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <Box sx={{ mt: 2 }}>
                  <Select
                    name="producto"
                    label="Producto"
                    value={formik.values.producto}
                    onChange={formik.handleChange}
                    options={productoOptions}
                    error={formik.touched.producto && Boolean(formik.errors.producto)}
                    helperText={formik.touched.producto && formik.errors.producto}
                    required
                  />
                </Box>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Box sx={{ mt: 2 }}>
                  <FormField
                    name="cantidad"
                    label="Cantidad"
                    type="number"
                    formik={formik}
                    required
                  />
                </Box>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Box sx={{ mt: 2 }}>
                  <FormField name="ubicacion" label="Ubicación" formik={formik} />
                </Box>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} color="inherit">
              Cancelar
            </Button>
            <Button type="submit" loading={formik.isSubmitting}>
              {editingItem ? 'Actualizar' : 'Crear'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>

      {/* Dialog para enviar email */}
      <Dialog open={emailDialog} onClose={() => setEmailDialog(false)} maxWidth="sm" fullWidth disableRestoreFocus>
        <DialogTitle>Enviar PDF por Email</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Ingrese el correo electrónico al que desea enviar el reporte de inventario.
          </Typography>
          <TextField
            label="Email destino"
            type="email"
            fullWidth
            value={emailTo}
            onChange={(e) => setEmailTo(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmailDialog(false)} color="inherit">
            Cancelar
          </Button>
          <Button onClick={handleSendEmail} loading={sendingEmail}>
            Enviar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog para ver detalles */}
      <Dialog
        open={viewDialog.open}
        onClose={() => setViewDialog({ open: false, item: null })}
        maxWidth="sm"
        fullWidth
        disableRestoreFocus
      >
        <DialogTitle>Detalles del Item de Inventario</DialogTitle>
        <DialogContent>
          {viewDialog.item && (
            <Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Empresa</Typography>
                <Typography variant="body1">{viewDialog.item.empresa_detail?.nombre || 'N/A'}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Producto</Typography>
                <Typography variant="body1">{viewDialog.item.producto_detail?.nombre || 'N/A'}</Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Cantidad</Typography>
                <Typography variant="body1">{viewDialog.item.cantidad}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Ubicación</Typography>
                <Typography variant="body1">{viewDialog.item.ubicacion || 'No especificada'}</Typography>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialog({ open: false, item: null })}>
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteDialog.open}
        title="Eliminar Item"
        message="¿Está seguro de eliminar este item del inventario?"
        onConfirm={handleDelete}
        onCancel={() => setDeleteDialog({ open: false, item: null })}
        confirmColor="error"
      />
    </Box>
  );
}
