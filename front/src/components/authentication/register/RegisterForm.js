import React from 'react'
import * as Yup from 'yup';
import { useState } from 'react';
import { Icon } from '@iconify/react';
import { useFormik, Form, FormikProvider } from 'formik';
import eyeFill from '@iconify/icons-eva/eye-fill';
import eyeOffFill from '@iconify/icons-eva/eye-off-fill';
import { useNavigate } from 'react-router-dom';
// material
import { Stack, TextField, IconButton, InputAdornment } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import ReactJson from 'react-json-view';
import { useAuth } from 'src/utils/useAuth';
import { registerSubmit } from 'src/utils/requests';


// ----------------------------------------------------------------------

export default function RegisterForm() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const { login } = useAuth()

  const RegisterSchema = Yup.object().shape({
    address: Yup.string().required('Address is required'),
    userID: Yup.string().required('Phone number is required'),
    password: Yup.string().required('Password is required')
  });

  const formik = useFormik({
    initialValues: {
      address: '',
      userID: '',
      password: ''
    },
    validationSchema: RegisterSchema,
    onSubmit: (values, { resetForm }) => {
      registerSubmit(values)
        .then((res) => {
          login(res.data)
          navigate('/dashboard', { replace: true });
          window.location.reload()
        })
        .catch(() => {
          resetForm()
          // TODO show wrong password or others error for hint
        })
    },
  });

  const { errors, touched, values, handleSubmit, isSubmitting, getFieldProps } = formik;

  return (
    <FormikProvider value={formik}>
      <Form autoComplete="off" noValidate onSubmit={handleSubmit}>
        <Stack spacing={3}>
          <TextField
            fullWidth
            label="Phone Number"
            {...getFieldProps('userID')}
            error={Boolean(touched.userID && errors.userID)}
            helperText={touched.userID && errors.userID}
          />
          <TextField
            fullWidth
            autoComplete="username"
            // type="email"
            // label="Email address"
            label="Address "
            // {...getFieldProps('email')}
            {...getFieldProps('address')}
            error={Boolean(touched.address && errors.address)}
            helperText={touched.address && errors.address}
          />

          <TextField
            fullWidth
            autoComplete="current-password"
            type={showPassword ? 'text' : 'password'}
            label="Password"
            {...getFieldProps('password')}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton edge="end" onClick={() => setShowPassword((prev) => !prev)}>
                    <Icon icon={showPassword ? eyeFill : eyeOffFill} />
                  </IconButton>
                </InputAdornment>
              )
            }}
            error={Boolean(touched.password && errors.password)}
            helperText={touched.password && errors.password}
          />

          <LoadingButton
            fullWidth
            size="large"
            type="submit"
            variant="contained"
            loading={isSubmitting}
          >
            Register
          </LoadingButton>
        </Stack>
      </Form>
    </FormikProvider>
  );
}
