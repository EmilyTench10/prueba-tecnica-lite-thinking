import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { Box, Toolbar, useMediaQuery, useTheme } from '@mui/material';

import { Navbar, Sidebar, ChatWidget } from '../../components/organisms';
import { useAuth } from '../../hooks/useAuth';
import { Loader } from '../../components/atoms';

export function AdminLayout({ children }) {
  const { auth, loading } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  if (loading) {
    return <Loader fullScreen />;
  }

  if (!auth) {
    return <Navigate to="/login" replace />;
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <Navbar onMenuClick={handleDrawerToggle} />

      {isMobile ? (
        <Sidebar
          open={mobileOpen}
          onClose={handleDrawerToggle}
          variant="temporary"
        />
      ) : (
        <Sidebar open variant="permanent" />
      )}

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - 240px)` },
          minHeight: '100vh',
          bgcolor: 'background.default',
        }}
      >
        <Toolbar />
        {children}
      </Box>

      <ChatWidget />
    </Box>
  );
}
