import { useState, useEffect } from 'react';
import { Grid, Card, CardContent, Box, Chip, Typography } from '@mui/material';
import BusinessIcon from '@mui/icons-material/Business';
import CategoryIcon from '@mui/icons-material/Category';
import SecurityIcon from '@mui/icons-material/Security';
import ChatIcon from '@mui/icons-material/Chat';
import PhoneIcon from '@mui/icons-material/Phone';

import { Button } from '../../components/atoms';
import { getEmpresasApi } from '../../api/empresas';

const features = [
  {
    icon: <BusinessIcon sx={{ fontSize: 48 }} />,
    title: 'Gestión de Empresas',
    description: 'Administra empresas con NIT, nombre, dirección y teléfono de forma eficiente.',
    color: '#6366f1',
  },
  {
    icon: <CategoryIcon sx={{ fontSize: 48 }} />,
    title: 'Catálogo de Productos',
    description: 'Gestiona productos con precios en múltiples monedas internacionales.',
    color: '#8b5cf6',
  },
  {
    icon: <SecurityIcon sx={{ fontSize: 48 }} />,
    title: 'Blockchain',
    description: 'Verificación de integridad y trazabilidad con tecnología blockchain.',
    color: '#10b981',
  },
  {
    icon: <ChatIcon sx={{ fontSize: 48 }} />,
    title: 'Chatbot IA',
    description: 'Asistente virtual inteligente para consultas y soporte 24/7.',
    color: '#3b82f6',
  },
];

export function Home() {
  const [empresas, setEmpresas] = useState([]);

  useEffect(() => {
    loadEmpresas();
  }, []);

  const loadEmpresas = async () => {
    try {
      const data = await getEmpresasApi();
      setEmpresas(data);
    } catch (error) {
      console.error('Error cargando empresas:', error);
    }
  };

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          py: { xs: 8, md: 12 },
          px: 3,
          background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
          borderRadius: 4,
          mb: 6,
        }}
      >
        <Typography
          variant="h1"
          sx={{
            mb: 2,
            fontSize: { xs: '2.5rem', md: '3.5rem' },
            fontWeight: 700,
            color: '#ffffff',
          }}
        >
          Lite Thinking
        </Typography>
        <Typography
          variant="h5"
          sx={{
            mb: 3,
            color: 'rgba(255,255,255,0.9)',
            fontWeight: 400,
            fontSize: { xs: '1.1rem', md: '1.4rem' },
          }}
        >
          Sistema de Gestión Empresarial Inteligente
        </Typography>
        <Typography
          variant="body1"
          sx={{
            mb: 5,
            maxWidth: 600,
            color: 'rgba(255,255,255,0.7)',
            lineHeight: 1.8,
          }}
        >
          Plataforma integral para la gestión de empresas, productos e inventario
          con tecnología de punta: Inteligencia Artificial y Blockchain.
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant="contained"
            color="secondary"
            size="large"
            href="/login"
            sx={{
              px: 4,
              py: 1.5,
              fontSize: '1rem',
            }}
          >
            Comenzar Ahora
          </Button>
          <Button
            variant="outlined"
            size="large"
            href="#features"
            sx={{
              px: 4,
              py: 1.5,
              borderColor: 'rgba(255,255,255,0.5)',
              color: 'white',
              '&:hover': {
                borderColor: 'white',
                bgcolor: 'rgba(255,255,255,0.1)',
              },
            }}
          >
            Conocer más
          </Button>
        </Box>
      </Box>

      {/* Features */}
      <Box id="features" sx={{ mb: 8 }}>
        <Typography
          variant="h3"
          align="center"
          gutterBottom
          sx={{ mb: 2, fontWeight: 700 }}
        >
          Características Principales
        </Typography>
        <Typography
          variant="body1"
          align="center"
          color="textSecondary"
          sx={{ mb: 6, maxWidth: 600, mx: 'auto' }}
        >
          Todo lo que necesitas para gestionar tu empresa de manera eficiente y segura.
        </Typography>
        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                sx={{
                  height: '100%',
                  textAlign: 'center',
                  p: 3,
                  cursor: 'pointer',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                  },
                }}
              >
                <Box
                  sx={{
                    width: 80,
                    height: 80,
                    borderRadius: 3,
                    bgcolor: `${feature.color}15`,
                    color: feature.color,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mx: 'auto',
                    mb: 3,
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {feature.description}
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Empresas Preview */}
      {empresas.length > 0 && (
        <Box>
          <Typography
            variant="h3"
            align="center"
            gutterBottom
            sx={{ mb: 2, fontWeight: 700 }}
          >
            Empresas Registradas
          </Typography>
          <Typography
            variant="body1"
            align="center"
            color="textSecondary"
            sx={{ mb: 6 }}
          >
            Conoce las empresas que confían en nuestra plataforma.
          </Typography>
          <Grid container spacing={3}>
            {empresas.slice(0, 6).map((empresa) => (
              <Grid item xs={12} sm={6} md={4} key={empresa.nit}>
                <Card sx={{ p: 1 }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                      {empresa.nombre}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      <Chip
                        label={`NIT: ${empresa.nit}`}
                        size="small"
                        sx={{ bgcolor: '#f1f5f9' }}
                      />
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, color: 'text.secondary' }}>
                      <PhoneIcon sx={{ fontSize: 16 }} />
                      <Typography variant="body2">{empresa.telefono}</Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Box>
  );
}
