import React from 'react'
import { Navigate, useRoutes } from 'react-router-dom';
// layouts
import DashboardLayout from './layouts/DashboardLayout'
//
import Login from './pages/Login';
import Register from './pages/Register';
import NotFound from './pages/Page404';
import RestaurantsList from './pages/RestaurantsList';
import RestaurantMenu from './pages/RestaurantMenu';
import DashboardRouter from './pages/dashboard/DashboardRouter';
import DelivererDashboard from './pages/dashboard/DelivererDashboard';
import RestaurantDashboard from './pages/dashboard/RestaurantDashboard';
import CustomerDashboard from './pages/dashboard/CustomerDashboard';

// ----------------------------------------------------------------------

export default function Router() {
  return useRoutes([
    {
      path: '/',
      element: <DashboardLayout />,
      children: [
        { path: '/', element: <Navigate to="/restaurant/all" /> },
        // public restaurant
        { path: 'restaurant/all', element: <RestaurantsList />},
        { path: 'restaurant/:id', element: <RestaurantMenu />},
        // private dashboard for each user
        { path: 'dashboard', element: <DashboardRouter />},
        { path: 'restaurant/dashboard', element: <RestaurantDashboard />},
        { path: 'customer/dashboard', element: <CustomerDashboard />},
        { path: 'deliverer/dashboard', element: <DelivererDashboard />},
        // sign pages
        { path: 'register', element: <Register /> },
        { path: 'login', element: <Login /> },
        // other pages
        { path: '404', element: <NotFound /> },
        { path: '*', element: <NotFound /> }
      ]
    },
  ]);
}
