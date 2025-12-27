import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Box, Paper, Alert } from '@mui/material';
import { toast } from 'react-toastify';
import { useState } from 'react';

import { Button, Typography } from '../../atoms';
import { FormField } from '../../molecules';
import { loginApi } from '../../../api/auth';
import { useAuth } from '../../../hooks/useAuth';

const validationSchema = Yup.object({
  email: Yup.string()
    .email('Email inválido')
    .required('El email es requerido'),
  password: Yup.string()
    .min(6, 'Mínimo 6 caracteres')
    .required('La contraseña es requerida'),
});

export function LoginForm() {
  const { login } = useAuth();
  const [error, setError] = useState('');

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
    },
    validationSchema,
    onSubmit: async (values, { setSubmitting }) => {
      setError('');
      try {
        const response = await loginApi(values);
        await login(response.access, response.refresh);
        toast.success('Inicio de sesión exitoso');
      } catch (err) {
        setError(err.message || 'Error al iniciar sesión');
        toast.error('Error al iniciar sesión');
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <Paper
      elevation={3}
      sx={{
        p: 4,
        maxWidth: 400,
        width: '100%',
        borderRadius: 3,
      }}
    >
      <Typography variant="h4" align="center" gutterBottom>
        Iniciar Sesión
      </Typography>
      <Typography variant="body2" color="textSecondary" align="center" sx={{ mb: 3 }}>
        Lite Thinking - Sistema de Gestión
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={formik.handleSubmit}>
        <FormField
          name="email"
          label="Correo electrónico"
          type="email"
          formik={formik}
          required
        />
        <FormField
          name="password"
          label="Contraseña"
          type="password"
          formik={formik}
          required
        />
        <Button
          type="submit"
          fullWidth
          size="large"
          loading={formik.isSubmitting}
          sx={{ mt: 2 }}
        >
          Ingresar
        </Button>
      </Box>
    </Paper>
  );
}
