import { Navigate } from 'react-router-dom';
import { Box } from '@mui/material';

import { useAuth } from '../../hooks/useAuth';
import { Loader } from '../../components/atoms';

export function AuthLayout({ children }) {
  const { auth, loading } = useAuth();

  if (loading) {
    return <Loader fullScreen />;
  }

  if (auth) {
    return <Navigate to="/admin" replace />;
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        bgcolor: 'background.default',
        p: 2,
      }}
    >
      {children}
    </Box>
  );
}
