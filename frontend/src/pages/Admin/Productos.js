import { useState, useEffect } from 'react';
import {
  Box, Dialog, DialogTitle, DialogContent, DialogActions,
  Grid, IconButton, Chip, Divider
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';

import { Typography, Button, Input } from '../../components/atoms';
import { FormField, SearchBar } from '../../components/molecules';
import { DataTable } from '../../components/organisms';
import { Select } from '../../components/atoms/Select';
import { useAuth } from '../../hooks/useAuth';
import { MONEDAS } from '../../utils/constants';
import {
  getProductosApi,
  createProductoApi,
  updateProductoApi,
  deleteProductoApi,
} from '../../api/productos';
import { getEmpresasApi } from '../../api/empresas';
import { ConfirmDialog } from '../../components/molecules';

const columns = [
  { id: 'codigo', label: 'Código', minWidth: 100 },
  { id: 'nombre', label: 'Nombre', minWidth: 200 },
  { id: 'empresa_nombre', label: 'Empresa', minWidth: 150 },
  {
    id: 'precio_cop',
    label: 'Precio COP',
    minWidth: 120,
    format: (value) => value ? `$ ${value.toLocaleString()}` : 'N/A',
  },
];

const validationSchema = Yup.object({
  codigo: Yup.string().required('El código es requerido'),
  nombre: Yup.string().required('El nombre es requerido'),
  empresa: Yup.string().required('La empresa es requerida'),
});

export function Productos() {
  const { auth } = useAuth();
  const isAdmin = auth?.user?.role === 'admin' || auth?.user?.is_superuser;

  const [productos, setProductos] = useState([]);
  const [filteredProductos, setFilteredProductos] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingProducto, setEditingProducto] = useState(null);
  const [deleteDialog, setDeleteDialog] = useState({ open: false, producto: null });
  const [precios, setPrecios] = useState([{ moneda: 'COP', precio: '' }]);
  const [viewDialog, setViewDialog] = useState({ open: false, producto: null });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [productosData, empresasData] = await Promise.all([
        getProductosApi(),
        getEmpresasApi(),
      ]);
      setProductos(productosData);
      setFilteredProductos(productosData);
      setEmpresas(empresasData);
    } catch (error) {
      toast.error('Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    const filtered = productos.filter(
      (p) =>
        p.codigo.toLowerCase().includes(query.toLowerCase()) ||
        p.nombre.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredProductos(filtered);
  };

  const formik = useFormik({
    initialValues: {
      codigo: '',
      nombre: '',
      caracteristicas: '',
      empresa: '',
    },
    validationSchema,
    onSubmit: async (values, { setSubmitting, resetForm }) => {
      try {
        const data = {
          ...values,
          precios: precios.filter((p) => p.precio).map((p) => ({
            moneda: p.moneda,
            precio: parseFloat(p.precio),
          })),
        };

        if (editingProducto) {
          await updateProductoApi(editingProducto.id, data);
          toast.success('Producto actualizado correctamente');
        } else {
          await createProductoApi(data);
          toast.success('Producto creado correctamente');
        }
        resetForm();
        setPrecios([{ moneda: 'COP', precio: '' }]);
        setOpenDialog(false);
        setEditingProducto(null);
        loadData();
      } catch (error) {
        toast.error(error.message);
      } finally {
        setSubmitting(false);
      }
    },
  });

  const handleEdit = (producto) => {
    setEditingProducto(producto);
    formik.setValues({
      codigo: producto.codigo,
      nombre: producto.nombre,
      caracteristicas: producto.caracteristicas || '',
      empresa: producto.empresa,
    });
    if (producto.precios && producto.precios.length > 0) {
      setPrecios(producto.precios.map((p) => ({ moneda: p.moneda, precio: p.precio.toString() })));
    }
    setOpenDialog(true);
  };

  const handleDelete = async () => {
    try {
      await deleteProductoApi(deleteDialog.producto.id);
      toast.success('Producto eliminado correctamente');
      setDeleteDialog({ open: false, producto: null });
      loadData();
    } catch (error) {
      toast.error('Error al eliminar producto');
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingProducto(null);
    setPrecios([{ moneda: 'COP', precio: '' }]);
    formik.resetForm();
  };

  const addPrecio = () => {
    setPrecios([...precios, { moneda: 'USD', precio: '' }]);
  };

  const removePrecio = (index) => {
    setPrecios(precios.filter((_, i) => i !== index));
  };

  const updatePrecio = (index, field, value) => {
    const newPrecios = [...precios];
    newPrecios[index][field] = value;
    setPrecios(newPrecios);
  };

  const handleView = (producto) => {
    setViewDialog({ open: true, producto });
  };

  const empresaOptions = empresas.map((e) => ({ value: e.nit, label: e.nombre }));
  const monedaOptions = MONEDAS.map((m) => ({ value: m.codigo, label: `${m.codigo} - ${m.nombre}` }));

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Productos</Typography>
        {isAdmin && (
          <Button startIcon={<AddIcon />} onClick={() => setOpenDialog(true)}>
            Nuevo Producto
          </Button>
        )}
      </Box>

      <Box sx={{ mb: 3, maxWidth: 400 }}>
        <SearchBar placeholder="Buscar por código o nombre..." onSearch={handleSearch} />
      </Box>

      <DataTable
        columns={columns}
        data={filteredProductos}
        loading={loading}
        onView={handleView}
        onEdit={isAdmin ? handleEdit : null}
        onDelete={isAdmin ? (producto) => setDeleteDialog({ open: true, producto }) : null}
        showActions={true}
        emptyMessage="No hay productos registrados"
      />

      {/* Dialog para crear/editar */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth disableRestoreFocus>
        <DialogTitle>
          {editingProducto ? 'Editar Producto' : 'Nuevo Producto'}
        </DialogTitle>
        <Box component="form" onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <FormField name="codigo" label="Código" formik={formik} required />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Box sx={{ mb: 2 }}>
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
                </Box>
              </Grid>
              <Grid item xs={12}>
                <FormField name="nombre" label="Nombre del producto" formik={formik} required />
              </Grid>
              <Grid item xs={12}>
                <FormField
                  name="caracteristicas"
                  label="Características"
                  formik={formik}
                  multiline
                  rows={3}
                />
              </Grid>
            </Grid>

            <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
              Precios por moneda
            </Typography>
            {precios.map((precio, index) => (
              <Grid container spacing={2} key={index} sx={{ mb: 2 }} alignItems="center">
                <Grid item xs={5}>
                  <Select
                    label="Moneda"
                    value={precio.moneda}
                    onChange={(e) => updatePrecio(index, 'moneda', e.target.value)}
                    options={monedaOptions}
                  />
                </Grid>
                <Grid item xs={5}>
                  <Input
                    label="Precio"
                    type="number"
                    value={precio.precio}
                    onChange={(e) => updatePrecio(index, 'precio', e.target.value)}
                  />
                </Grid>
                <Grid item xs={2}>
                  {precios.length > 1 && (
                    <IconButton color="error" onClick={() => removePrecio(index)}>
                      <DeleteIcon />
                    </IconButton>
                  )}
                </Grid>
              </Grid>
            ))}
            <Button variant="outlined" size="small" onClick={addPrecio} startIcon={<AddIcon />}>
              Agregar precio
            </Button>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} color="inherit">
              Cancelar
            </Button>
            <Button type="submit" loading={formik.isSubmitting}>
              {editingProducto ? 'Actualizar' : 'Crear'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>

      {/* Dialog para ver detalles */}
      <Dialog
        open={viewDialog.open}
        onClose={() => setViewDialog({ open: false, producto: null })}
        maxWidth="sm"
        fullWidth
        disableRestoreFocus
      >
        <DialogTitle>Detalles del Producto</DialogTitle>
        <DialogContent>
          {viewDialog.producto && (
            <Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Código</Typography>
                <Typography variant="body1">{viewDialog.producto.codigo}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Nombre</Typography>
                <Typography variant="body1">{viewDialog.producto.nombre}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Empresa</Typography>
                <Typography variant="body1">{viewDialog.producto.empresa_nombre}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Características</Typography>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                  {viewDialog.producto.caracteristicas || 'Sin características'}
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle2" color="textSecondary" sx={{ mb: 1 }}>
                Precios por Moneda
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {viewDialog.producto.precios && viewDialog.producto.precios.length > 0 ? (
                  viewDialog.producto.precios.map((precio, index) => (
                    <Chip
                      key={index}
                      label={`${precio.moneda}: ${precio.precio.toLocaleString()}`}
                      color="primary"
                      variant="outlined"
                    />
                  ))
                ) : (
                  <Typography variant="body2" color="textSecondary">
                    Sin precios registrados
                  </Typography>
                )}
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialog({ open: false, producto: null })}>
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteDialog.open}
        title="Eliminar Producto"
        message={`¿Está seguro de eliminar el producto ${deleteDialog.producto?.nombre}?`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteDialog({ open: false, producto: null })}
        confirmColor="error"
      />
    </Box>
  );
}
