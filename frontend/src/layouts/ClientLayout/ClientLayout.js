import { Box, AppBar, Toolbar, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import LoginIcon from '@mui/icons-material/Login';
import DashboardIcon from '@mui/icons-material/Dashboard';

import { ChatWidget } from '../../components/organisms';
import { useAuth } from '../../hooks/useAuth';

export function ClientLayout({ children }) {
  const { auth } = useAuth();
  const navigate = useNavigate();

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar>
          <span
            style={{
              flexGrow: 1,
              cursor: 'pointer',
              color: '#FFFFFF',
              fontWeight: 700,
              fontSize: '1.25rem',
            }}
            onClick={() => navigate('/')}
          >
            Lite Thinking
          </span>
          {auth ? (
            <Button
              variant="contained"
              color="secondary"
              startIcon={<DashboardIcon />}
              onClick={() => navigate('/admin')}
              sx={{
                bgcolor: '#6366f1',
                color: 'white',
                fontWeight: 600,
                px: 3,
                '&:hover': {
                  bgcolor: '#4f46e5',
                },
              }}
            >
              Panel Admin
            </Button>
          ) : (
            <Button
              variant="contained"
              color="secondary"
              startIcon={<LoginIcon />}
              onClick={() => navigate('/login')}
              sx={{
                bgcolor: '#6366f1',
                color: 'white',
                fontWeight: 600,
                px: 3,
                '&:hover': {
                  bgcolor: '#4f46e5',
                },
              }}
            >
              Iniciar Sesión
            </Button>
          )}
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        {children}
      </Container>

      <ChatWidget />
    </Box>
  );
}
