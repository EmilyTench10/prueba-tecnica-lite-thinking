import { useLocation, useNavigate } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Divider,
  Box,
} from '@mui/material';
import BusinessIcon from '@mui/icons-material/Business';
import InventoryIcon from '@mui/icons-material/Inventory';
import CategoryIcon from '@mui/icons-material/Category';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LinkIcon from '@mui/icons-material/Link';
import ChatIcon from '@mui/icons-material/Chat';
import PeopleIcon from '@mui/icons-material/People';

import { useAuth } from '../../../hooks/useAuth';
import { ROLES } from '../../../utils/constants';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/admin', roles: [ROLES.ADMIN, ROLES.EXTERNO] },
  { text: 'Empresas', icon: <BusinessIcon />, path: '/admin/empresas', roles: [ROLES.ADMIN, ROLES.EXTERNO] },
  { text: 'Productos', icon: <CategoryIcon />, path: '/admin/productos', roles: [ROLES.ADMIN, ROLES.EXTERNO] },
  { text: 'Inventario', icon: <InventoryIcon />, path: '/admin/inventario', roles: [ROLES.ADMIN] },
  { text: 'Blockchain', icon: <LinkIcon />, path: '/admin/blockchain', roles: [ROLES.ADMIN, ROLES.EXTERNO] },
  { text: 'Chatbot IA', icon: <ChatIcon />, path: '/admin/chatbot', roles: [ROLES.ADMIN, ROLES.EXTERNO] },
  { text: 'Usuarios', icon: <PeopleIcon />, path: '/admin/usuarios', roles: [ROLES.ADMIN] },
];

export function Sidebar({ open, onClose, variant = 'permanent' }) {
  const { auth } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const userRole = auth?.user?.role || ROLES.EXTERNO;

  const filteredMenuItems = menuItems.filter(
    (item) => item.roles.includes(userRole) || auth?.user?.is_superuser
  );

  const handleNavigate = (path) => {
    navigate(path);
    if (variant === 'temporary') {
      onClose();
    }
  };

  const drawer = (
    <>
      <Toolbar />
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {filteredMenuItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => handleNavigate(item.path)}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: 'primary.light',
                    color: 'white',
                    '& .MuiListItemIcon-root': {
                      color: 'white',
                    },
                  },
                }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        <Divider />
      </Box>
    </>
  );

  return (
    <Drawer
      variant={variant}
      open={open}
      onClose={onClose}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      {drawer}
    </Drawer>
  );
}
