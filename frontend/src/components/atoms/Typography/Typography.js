import { Typography as MuiTypography } from '@mui/material';

export function Typography({
  children,
  variant = 'body1',
  color = 'textPrimary',
  align = 'left',
  gutterBottom = false,
  noWrap = false,
  component,
  ...props
}) {
  return (
    <MuiTypography
      variant={variant}
      color={color}
      align={align}
      gutterBottom={gutterBottom}
      noWrap={noWrap}
      component={component}
      {...props}
    >
      {children}
    </MuiTypography>
  );
}
