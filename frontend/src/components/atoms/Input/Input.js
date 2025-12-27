import { TextField } from '@mui/material';

export function Input({
  name,
  label,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  helperText,
  placeholder,
  required = false,
  disabled = false,
  fullWidth = true,
  multiline = false,
  rows = 4,
  size = 'medium',
  ...props
}) {
  return (
    <TextField
      name={name}
      label={label}
      type={type}
      value={value}
      onChange={onChange}
      onBlur={onBlur}
      error={error}
      helperText={helperText}
      placeholder={placeholder}
      required={required}
      disabled={disabled}
      fullWidth={fullWidth}
      multiline={multiline}
      rows={multiline ? rows : undefined}
      size={size}
      variant="outlined"
      {...props}
    />
  );
}
