import React from 'react'
import { Icon } from '@iconify/react';
import { useRef, useState } from 'react';
import homeFill from '@iconify/icons-eva/home-fill';
import loginOutlined from '@iconify/icons-ant-design/login-outlined';
import roundAppRegistration from '@iconify/icons-ic/round-app-registration';
import { Link as RouterLink, useNavigate} from 'react-router-dom';
// material
import { alpha } from '@mui/material/styles';
import { Button, Box, Divider, MenuItem, Typography, Avatar, IconButton } from '@mui/material';
// components
import MenuPopover from '../../components/helpers/MenuPopover';
//
import { useAuth } from 'src/utils/useAuth';

// ----------------------------------------------------------------------

const account = {
  displayName: 'Shab food',
  photoURL: '/static/avatar_default.jpg'
};

const MENU_OPTIONS = [
  {
    label: 'Dashbard',
    icon: homeFill,
    linkTo: '/dashboard',
    sign: true
  },
  {
    label: 'LogIn',
    icon: loginOutlined,
    linkTo: '/login',
    sign: false
  },
  {
    label: 'register',
    icon: roundAppRegistration,
    linkTo: '/register',
    sign: false
  }
];

// ----------------------------------------------------------------------

export default function AccountPopover() {
  const anchorRef = useRef(null);
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  const navigate = useNavigate();
  const HandlelogOut = () => {
    logout().then( () =>
      navigate('/', { replace: true })
    )
  }

  const { authed, logout } = useAuth()
  const loggedIn = !!authed?.object_type
  return (
    <>
      <IconButton
        ref={anchorRef}
        onClick={handleOpen}
        sx={{
          padding: 0,
          width: 44,
          height: 44,
          ...(open && {
            '&:before': {
              zIndex: 1,
              content: "''",
              width: '100%',
              height: '100%',
              borderRadius: '50%',
              position: 'absolute',
              bgcolor: (theme) => alpha(theme.palette.grey[900], 0.72)
            }
          })
        }}
      >
        <Avatar src={account.photoURL} alt="photoURL" />
      </IconButton>

      <MenuPopover
        open={open}
        onClose={handleClose}
        anchorEl={anchorRef.current}
        sx={{ width: 220 }}
      >
        <Box sx={{ my: 1.5, px: 2.5 }}>
          <Typography variant="subtitle1" noWrap>
            {account.displayName}
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
            {authed?.object_type}
          </Typography>
        </Box>

        <Divider sx={{ my: 1 }} />

        {MENU_OPTIONS.map((option) => (
          (option?.sign === (loggedIn)) && (<MenuItem
            key={option.label}
            to={option.linkTo}
            component={RouterLink}
            onClick={handleClose}
            sx={{ typography: 'body2', py: 1, px: 2.5 }}
          >
            <Box
              component={Icon}
              icon={option.icon}
              sx={{
                mr: 2,
                width: 24,
                height: 24
              }}
            />

            {option.label}
          </MenuItem>)
        ))}

        {(loggedIn) && (<Box sx={{ p: 2, pt: 1.5 }}>
          <Button fullWidth color="inherit" variant="outlined" onClick={HandlelogOut}>
            Logout
          </Button>
        </Box>)}
      </MenuPopover>
    </>
  );
}
