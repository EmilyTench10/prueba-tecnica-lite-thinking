import { useState, useEffect } from 'react';
import { Grid, Card, CardContent, Box } from '@mui/material';
import BusinessIcon from '@mui/icons-material/Business';
import CategoryIcon from '@mui/icons-material/Category';
import InventoryIcon from '@mui/icons-material/Inventory';
import LinkIcon from '@mui/icons-material/Link';

import { Typography, Loader } from '../../components/atoms';
import { useAuth } from '../../hooks/useAuth';
import { getEmpresasApi } from '../../api/empresas';
import { getProductosApi } from '../../api/productos';
import { getInventarioApi } from '../../api/inventario';
import { getEstadisticasBlockchainApi } from '../../api/blockchain';

export function Dashboard() {
  const { auth } = useAuth();
  const [stats, setStats] = useState({
    empresas: 0,
    productos: 0,
    inventario: 0,
    blockchain: { total_bloques: 0, integridad: true },
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [empresas, productos, inventario, blockchain] = await Promise.all([
        getEmpresasApi().catch(() => []),
        getProductosApi().catch(() => []),
        getInventarioApi().catch(() => []),
        getEstadisticasBlockchainApi().catch(() => ({ total_bloques: 0, integridad: true })),
      ]);

      setStats({
        empresas: empresas.length,
        productos: productos.length,
        inventario: inventario.length,
        blockchain,
      });
    } catch (error) {
      console.error('Error cargando estadísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader />;

  const cards = [
    {
      title: 'Empresas',
      value: stats.empresas,
      icon: <BusinessIcon sx={{ fontSize: 50 }} />,
      color: '#1976d2',
    },
    {
      title: 'Productos',
      value: stats.productos,
      icon: <CategoryIcon sx={{ fontSize: 50 }} />,
      color: '#9c27b0',
    },
    {
      title: 'Items en Inventario',
      value: stats.inventario,
      icon: <InventoryIcon sx={{ fontSize: 50 }} />,
      color: '#2e7d32',
    },
    {
      title: 'Bloques Blockchain',
      value: stats.blockchain.total_bloques,
      icon: <LinkIcon sx={{ fontSize: 50 }} />,
      color: stats.blockchain.integridad ? '#ff9800' : '#d32f2f',
      subtitle: stats.blockchain.integridad ? 'Integridad OK' : 'Error de integridad',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="body1" color="textSecondary" sx={{ mb: 4 }}>
        Bienvenido, {auth.user.email}
      </Typography>

      <Grid container spacing={3}>
        {cards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                borderLeft: `4px solid ${card.color}`,
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="h3" sx={{ color: card.color }}>
                      {card.value}
                    </Typography>
                    <Typography variant="h6" color="textSecondary">
                      {card.title}
                    </Typography>
                    {card.subtitle && (
                      <Typography variant="caption" color={card.color === '#d32f2f' ? 'error' : 'success.main'}>
                        {card.subtitle}
                      </Typography>
                    )}
                  </Box>
                  <Box sx={{ color: card.color, opacity: 0.3 }}>
                    {card.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
