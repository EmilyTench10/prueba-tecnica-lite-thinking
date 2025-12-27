import { Box } from '@mui/material';
import { Input } from '../../atoms';

export function FormField({
  name,
  label,
  type = 'text',
  formik,
  required = false,
  disabled = false,
  multiline = false,
  rows = 4,
  ...props
}) {
  return (
    <Box sx={{ mb: 2 }}>
      <Input
        name={name}
        label={label}
        type={type}
        value={formik.values[name]}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        error={formik.touched[name] && Boolean(formik.errors[name])}
        helperText={formik.touched[name] && formik.errors[name]}
        required={required}
        disabled={disabled}
        multiline={multiline}
        rows={rows}
        {...props}
      />
    </Box>
  );
}
