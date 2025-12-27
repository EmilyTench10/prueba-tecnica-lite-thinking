import { Card, CardContent, CardActions, Box } from '@mui/material';
import { Typography } from '../../atoms';

export function DataCard({
  title,
  subtitle,
  content,
  actions,
  onClick,
  elevation = 1,
  ...props
}) {
  return (
    <Card
      elevation={elevation}
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': onClick ? {
          transform: 'translateY(-4px)',
          boxShadow: 4,
        } : {},
      }}
      onClick={onClick}
      {...props}
    >
      <CardContent sx={{ flexGrow: 1 }}>
        {title && (
          <Typography variant="h6" gutterBottom>
            {title}
          </Typography>
        )}
        {subtitle && (
          <Typography variant="body2" color="textSecondary" gutterBottom>
            {subtitle}
          </Typography>
        )}
        {content && (
          <Box sx={{ mt: 1 }}>
            {content}
          </Box>
        )}
      </CardContent>
      {actions && (
        <CardActions sx={{ justifyContent: 'flex-end', p: 2 }}>
          {actions}
        </CardActions>
      )}
    </Card>
  );
}
