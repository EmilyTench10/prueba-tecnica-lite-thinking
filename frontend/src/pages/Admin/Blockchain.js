import { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Chip, Paper, Alert,
  Dialog, DialogTitle, DialogContent, DialogActions, Divider
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import RefreshIcon from '@mui/icons-material/Refresh';

import { Typography, Button, Loader } from '../../components/atoms';
import { DataTable } from '../../components/organisms';
import { getBlockchainApi, verificarBlockchainApi, getEstadisticasBlockchainApi } from '../../api/blockchain';

const columns = [
  { id: 'indice', label: '#', minWidth: 50 },
  {
    id: 'tipo',
    label: 'Tipo',
    minWidth: 150,
    format: (v) => v.replace('_', ' ').toUpperCase(),
  },
  { id: 'usuario', label: 'Usuario', minWidth: 150 },
  {
    id: 'timestamp',
    label: 'Fecha',
    minWidth: 150,
    format: (v) => new Date(v).toLocaleString(),
  },
  {
    id: 'hash_actual',
    label: 'Hash',
    minWidth: 200,
    format: (v) => `${v.substring(0, 16)}...`,
  },
];

export function Blockchain() {
  const [registros, setRegistros] = useState([]);
  const [estadisticas, setEstadisticas] = useState(null);
  const [verificacion, setVerificacion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [verificando, setVerificando] = useState(false);
  const [viewDialog, setViewDialog] = useState({ open: false, registro: null });

  const handleView = (registro) => {
    setViewDialog({ open: true, registro });
  };

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [registrosData, statsData] = await Promise.all([
        getBlockchainApi(),
        getEstadisticasBlockchainApi(),
      ]);
      setRegistros(registrosData);
      setEstadisticas(statsData);
    } catch (error) {
      console.error('Error cargando blockchain:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerificar = async () => {
    setVerificando(true);
    try {
      const result = await verificarBlockchainApi();
      setVerificacion(result);
    } catch (error) {
      console.error('Error verificando:', error);
    } finally {
      setVerificando(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Blockchain</Typography>
        <Button
          startIcon={<RefreshIcon />}
          onClick={handleVerificar}
          loading={verificando}
        >
          Verificar Integridad
        </Button>
      </Box>

      {/* Estadísticas */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h3" color="primary">
                {estadisticas?.total_bloques || 0}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total de Bloques
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Chip
                icon={estadisticas?.integridad ? <CheckCircleIcon /> : <ErrorIcon />}
                label={estadisticas?.integridad ? 'Integridad OK' : 'Error'}
                color={estadisticas?.integridad ? 'success' : 'error'}
                sx={{ mb: 1 }}
              />
              <Typography variant="body2" color="textSecondary">
                Estado de la Cadena
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="body1">
                {estadisticas?.primer_bloque
                  ? new Date(estadisticas.primer_bloque).toLocaleDateString()
                  : 'N/A'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Primer Bloque
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="body1">
                {estadisticas?.ultimo_bloque
                  ? new Date(estadisticas.ultimo_bloque).toLocaleDateString()
                  : 'N/A'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Último Bloque
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Resultado de verificación */}
      {verificacion && (
        <Alert
          severity={verificacion.valido ? 'success' : 'error'}
          sx={{ mb: 3 }}
          onClose={() => setVerificacion(null)}
        >
          {verificacion.valido
            ? `La cadena de ${verificacion.total_bloques} bloques es válida. No se detectaron manipulaciones.`
            : `Error de integridad: ${verificacion.errores.length} errores encontrados.`}
        </Alert>
      )}

      {/* Transacciones por tipo */}
      {estadisticas?.por_tipo && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Transacciones por Tipo
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {estadisticas.por_tipo.map((stat) => (
              <Chip
                key={stat.tipo}
                label={`${stat.tipo.replace('_', ' ')}: ${stat.total}`}
                variant="outlined"
              />
            ))}
          </Box>
        </Paper>
      )}

      {/* Tabla de registros */}
      <Typography variant="h6" gutterBottom>
        Registros de la Cadena
      </Typography>
      <DataTable
        columns={columns}
        data={registros}
        onView={handleView}
        showActions={true}
        emptyMessage="No hay registros en la blockchain"
      />

      {/* Dialog para ver detalles */}
      <Dialog
        open={viewDialog.open}
        onClose={() => setViewDialog({ open: false, registro: null })}
        maxWidth="md"
        fullWidth
        disableRestoreFocus
      >
        <DialogTitle>Detalles del Bloque #{viewDialog.registro?.indice}</DialogTitle>
        <DialogContent>
          {viewDialog.registro && (
            <Box>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Índice</Typography>
                    <Typography variant="body1">{viewDialog.registro.indice}</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Tipo</Typography>
                    <Chip
                      label={viewDialog.registro.tipo.replace('_', ' ').toUpperCase()}
                      color="primary"
                      size="small"
                    />
                  </Box>
                </Grid>
              </Grid>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Usuario</Typography>
                <Typography variant="body1">{viewDialog.registro.usuario}</Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Fecha y Hora</Typography>
                <Typography variant="body1">
                  {new Date(viewDialog.registro.timestamp).toLocaleString()}
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Datos de la Transacción</Typography>
                <Paper sx={{ p: 2, bgcolor: 'grey.100', mt: 1 }}>
                  <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                    {JSON.stringify(viewDialog.registro.datos, null, 2)}
                  </pre>
                </Paper>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Hash Anterior</Typography>
                <Typography variant="body2" sx={{ fontFamily: 'monospace', wordBreak: 'break-all' }}>
                  {viewDialog.registro.hash_anterior}
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">Hash Actual</Typography>
                <Typography variant="body2" sx={{ fontFamily: 'monospace', wordBreak: 'break-all' }}>
                  {viewDialog.registro.hash_actual}
                </Typography>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialog({ open: false, registro: null })}>
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
