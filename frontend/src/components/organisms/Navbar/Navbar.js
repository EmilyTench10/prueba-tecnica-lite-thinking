import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  IconButton,
  Menu,
  MenuItem,
  Box,
  Avatar,
  Chip,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircle from '@mui/icons-material/AccountCircle';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';

import { Button } from '../../atoms';
import { useAuth } from '../../../hooks/useAuth';

export function Navbar({ onMenuClick }) {
  const navigate = useNavigate();
  const { auth, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleClose();
    logout();
  };

  return (
    <AppBar
      position="fixed"
      elevation={1}
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        borderRadius: 0,
        bgcolor: '#0f172a',
      }}
    >
      <Toolbar sx={{ px: { xs: 2, sm: 3 }, color: '#ffffff' }}>
        {auth && (
          <IconButton
            edge="start"
            color="inherit"
            onClick={onMenuClick}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
        )}

        <Box
          onClick={() => navigate('/')}
          sx={{
            flexGrow: 1,
            cursor: 'pointer',
          }}
        >
          <span
            style={{
              color: 'white',
              fontWeight: 700,
              fontSize: '1.25rem',
              WebkitTextFillColor: 'white',
            }}
          >
            Lite Thinking
          </span>
        </Box>

        {auth ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Chip
              label={auth.user.role === 'admin' ? 'Administrador' : 'Externo'}
              color={auth.user.role === 'admin' ? 'secondary' : 'default'}
              size="small"
              sx={{
                bgcolor: auth.user.role === 'admin' ? 'secondary.main' : 'rgba(255,255,255,0.15)',
                color: 'white',
                fontWeight: 500,
              }}
            />
            <IconButton color="inherit" onClick={handleMenu}>
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                {auth.user.email[0].toUpperCase()}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem disabled>
                <AccountCircle sx={{ mr: 1 }} />
                {auth.user.email}
              </MenuItem>
              <MenuItem onClick={handleLogout}>
                <LogoutIcon sx={{ mr: 1 }} />
                Cerrar sesión
              </MenuItem>
            </Menu>
          </Box>
        ) : (
          <Button
            variant="contained"
            color="secondary"
            href="/login"
            startIcon={<LoginIcon />}
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
  );
}
