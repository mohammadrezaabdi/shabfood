import React from 'react'
import { Icon } from '@iconify/react';
import { useRef, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import moreVerticalFill from '@iconify/icons-eva/more-vertical-fill';
import messageCircleFill from '@iconify/icons-eva/message-circle-fill';
import alertCircleFill from '@iconify/icons-eva/alert-circle-fill';
// material
import { Menu, MenuItem, IconButton, ListItemIcon, ListItemText } from '@mui/material';
import { orderStateToStr, restaurantStateTransition } from 'src/utils/values';
import { updateOrderRestaurant} from "../../../utils/requests"
import { useAuth } from 'src/utils/useAuth';

// ----------------------------------------------------------------------

export default function RestaurantDashboardMoreMenu({
  currentStatus,
  orderID,
  handleRefresh
}) {
  const ref = useRef(null);
  const [isOpen, setIsOpen] = useState(false);

  const { authed, logout } = useAuth({});
  const handleChangeStatus = (new_status) => {
    updateOrderRestaurant(authed?.access_token, new_status, orderID).then(
      () => handleRefresh()
    ).catch(() => {})
  }

  return (
    <>
      <IconButton ref={ref} onClick={() => setIsOpen(true)}>
        <Icon icon={moreVerticalFill} width={20} height={20} />
      </IconButton>

      <Menu
        open={isOpen}
        anchorEl={ref.current}
        onClose={() => setIsOpen(false)}
        PaperProps={{
          sx: { width: 200, maxWidth: '100%' }
        }}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        {restaurantStateTransition?.[currentStatus] &&
          restaurantStateTransition[currentStatus].map(
            nextStatus => (
              <MenuItem sx={{ color: 'text.secondary' }} onClick={() => handleChangeStatus(nextStatus)}>
                <ListItemText primary={orderStateToStr[nextStatus]} primaryTypographyProps={{ variant: 'body2' }} />
              </MenuItem>
            )
          )}
      </Menu>
    </>
  );
}
