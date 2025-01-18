import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DrawerComponent from './components/DrawerComponent';
import URLRoute from './pages/URLRoute'; // Assuming this contains the other routes
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Dashboard from './pages/Dashboard';

export default function App() {
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <DrawerComponent
          open={open}
          handleDrawerOpen={handleDrawerOpen}
          handleDrawerClose={handleDrawerClose}
        />

        <Routes>
          {/* Default route to render Dashboard when first opening */}
          <Route path="/" element={<Navigate to="/dashboard" />} />
          {/* Dashboard Route */}
          <Route path="/dashboard" element={<Dashboard open={open} />} />
          {/* Other Routes */}
          <Route path="/*" element={<URLRoute open={open} />} />
        </Routes>
      </Box>
    </Router>
  );
}
