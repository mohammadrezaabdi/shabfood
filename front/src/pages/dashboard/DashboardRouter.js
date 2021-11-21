// material
import React from 'react'
import { useNavigate } from 'react-router';
import { useAuth } from 'src/utils/useAuth';
import { USER_TYPES } from 'src/utils/values';

// ----------------------------------------------------------------------

export default function DashboardRouter() {
  let navigate = useNavigate()
  const {authed} = useAuth()
  switch ((authed?.object_type + "").toLowerCase()) {
    case USER_TYPES.customer:
        navigate(`/customer/dashboard`)
        break
    case USER_TYPES.deliverer:
        navigate(`/deliverer/dashboard`)
        break
    case USER_TYPES.restaurant:
        navigate(`/restaurant/dashboard`)
        break
    default:
        navigate("/login")
  }
  return (<></>);
}
