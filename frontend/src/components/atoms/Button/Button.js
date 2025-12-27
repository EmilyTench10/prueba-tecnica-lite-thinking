import { Button as MuiButton, CircularProgress } from '@mui/material';

export function Button({
  children,
  variant = 'contained',
  color = 'primary',
  size = 'medium',
  loading = false,
  disabled = false,
  startIcon,
  endIcon,
  fullWidth = false,
  onClick,
  type = 'button',
  ...props
}) {
  return (
    <MuiButton
      variant={variant}
      color={color}
      size={size}
      disabled={disabled || loading}
      startIcon={loading ? <CircularProgress size={20} color="inherit" /> : startIcon}
      endIcon={endIcon}
      fullWidth={fullWidth}
      onClick={onClick}
      type={type}
      {...props}
    >
      {children}
    </MuiButton>
  );
}
