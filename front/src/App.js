// routes
import React from 'react'
import Router from './routes';
// theme
import ThemeConfig from './theme';
import GlobalStyles from './theme/globalStyles';
// components
import ScrollToTop from './components/helpers/ScrollToTop';
import { BaseOptionChartStyle } from './components/charts/BaseOptionChart';
import { AuthProvider } from './utils/useAuth';
import { ConfirmProvider } from 'material-ui-confirm'

// ----------------------------------------------------------------------

export default function App() {
  return (
    <ThemeConfig>
      <ScrollToTop />
      <GlobalStyles />
      <BaseOptionChartStyle />
      <ConfirmProvider>
        <AuthProvider>
          <Router />
        </ AuthProvider>
      </ConfirmProvider>
    </ThemeConfig>
  );
}
