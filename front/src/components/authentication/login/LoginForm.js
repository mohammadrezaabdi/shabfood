import React from 'react'
import * as Yup from 'yup';
import { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useFormik, Form, FormikProvider } from 'formik';
import { Icon } from '@iconify/react';
import eyeFill from '@iconify/icons-eva/eye-fill';
import eyeOffFill from '@iconify/icons-eva/eye-off-fill';
// material
import {
  Link,
  Stack,
  Checkbox,
  TextField,
  IconButton,
  InputAdornment,
  FormControlLabel,
  FormLabel,
  FormControl,
  RadioGroup,
  Radio
} from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { useAuth } from 'src/utils/useAuth';
import { loginSubmit } from 'src/utils/requests';
import { USER_TYPES } from 'src/utils/values';

// ----------------------------------------------------------------------

export default function LoginForm() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const { login } = useAuth()

  const LoginSchema = Yup.object().shape({
    userID: Yup.string().required('required'),
    password: Yup.string().required('Password is required')
  });

  const formik = useFormik({
    initialValues: {
      userID: '',
      password: '',
      userType: USER_TYPES.customer,
      remember: true
    },
    validationSchema: LoginSchema,
    onSubmit: (values, { resetForm }) => {
      loginSubmit(values)
        .then((res) => {
          login(res.data)
          navigate('/dashboard', { replace: true });
          window.location.reload()
        })
        .catch(() => {
          resetForm()
          // TODO show wrong password or others error
        })
    },
  });

  const { errors, touched, values, isSubmitting, handleSubmit, getFieldProps } = formik;

  const handleShowPassword = () => {
    setShowPassword((show) => !show);
  };

  return (
    <FormikProvider value={formik}>
      <Form autoComplete="off" noValidate onSubmit={handleSubmit}>
        <Stack spacing={3}>

          <TextField
            fullWidth
            autoComplete="username"
            label={values.userType === USER_TYPES.restaurant ? "Email address" : "Phone number"}
            {...getFieldProps('userID')}
            error={Boolean(touched.userID && errors.userID)}
            helperText={touched.userID && errors.userID}
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
                  <IconButton onClick={handleShowPassword} edge="end">
                    <Icon icon={showPassword ? eyeFill : eyeOffFill} />
                  </IconButton>
                </InputAdornment>
              )
            }}
            error={Boolean(touched.password && errors.password)}
            helperText={touched.password && errors.password}
          />
          <FormControl component="fieldset">
            <FormLabel component="legend">choose user type:</FormLabel>
            <RadioGroup
              {...getFieldProps("userType")}
              row
              aria-label="user-type"
              defaultValue="customer"
            >
              <FormControlLabel value={USER_TYPES.customer} control={<Radio />} label="Customer" />
              <FormControlLabel value={USER_TYPES.deliverer} control={<Radio />} label="Deliverer" />
              <FormControlLabel value={USER_TYPES.restaurant} control={<Radio />} label="Restaurant" />
            </RadioGroup>
          </FormControl>
        </Stack>

        <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ my: 2 }}>
          <FormControlLabel
            control={<Checkbox {...getFieldProps('remember')} checked={values.remember} />}
            label="Remember me"
          />

          <Link component={RouterLink} variant="subtitle2" to="#">
            Forgot password?
          </Link>
        </Stack>

        <LoadingButton
          fullWidth
          size="large"
          type="submit"
          variant="contained"
          loading={isSubmitting}
        >
          Login
        </LoadingButton>
      </Form>
    </FormikProvider>
  );
}
