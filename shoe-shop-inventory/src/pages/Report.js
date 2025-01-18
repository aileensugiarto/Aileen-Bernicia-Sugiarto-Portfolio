import React, { useState, useEffect } from "react";
import axios from "axios";
import { DataGrid } from "@mui/x-data-grid";
import {
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  Box,
} from '@mui/material';
import { styled } from '@mui/material/styles';

const drawerWidth = 240;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function Report({ open }) {
  const [productIn, setProductIn] = useState([]);
  const [productOut, setProductOut] = useState([]);
  const [selectedReport, setSelectedReport] = useState('productIn');

  useEffect(() => {
    // Fetch product in data
    axios.get('http://localhost:5000/api/product_in')
      .then(response => {
        setProductIn(response.data.data_barang); // Make sure the data contains unique ids
      })
      .catch(error => {
        console.log(error);
      });

    // Fetch product out data
    axios.get('http://localhost:5000/api/product_out')
      .then(response => {
        setProductOut(response.data.data_barang); // Make sure the data contains unique ids
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  // Define columns for Product In report
  const columnsIn = [
    { field: "name", headerName: "Name", width: 200 },
    { field: "product_in_date", headerName: "Product In Date", width: 200 },
    { field: "amount", headerName: "Amount", width: 100 },
  ];

  // Define columns for Product Out report
  const columnsOut = [
    { field: "name", headerName: "Name", width: 200 },
    { field: "product_out_date", headerName: "Product Out Date", width: 200 },
    { field: "amount", headerName: "Amount", width: 100 },
  ];

  // Helper to calculate total items
  const getTotalBarang = data => {
    return data.reduce((total, item) => total + item.amount, 0); // Use correct field name
  };

  // Handle report type change
  const handleReportChange = (event) => {
    setSelectedReport(event.target.value);
  };

  return (
    <Main open={open}>
      <DrawerHeader />

      <Container>
        <Typography variant="h4" gutterBottom>
          Report
        </Typography>

        <FormControl fullWidth variant="outlined" style={{ marginBottom: '2rem' }}>
          <Select value={selectedReport} onChange={handleReportChange}>
            <MenuItem value="productIn">Product In</MenuItem>
            <MenuItem value="productOut">Product Out</MenuItem>
          </Select>
        </FormControl>

        {/* Display Product In Data */}
        {selectedReport === 'productIn' ? (
          <>
            <Typography variant="h6" gutterBottom>
              Product In Report
            </Typography>
            <div style={{ height: 400, width: '100%' }}>
              <DataGrid
                rows={productIn}
                columns={columnsIn}
                pageSize={5}
                rowsPerPageOptions={[5]}
                getRowId={(row) => row.id_barang_masuk || row.id_product_in} // Fallback ID
              />
            </div>

            {/* Display total products in */}
            <Box mt={2}>
              <Typography variant="h6">
                Product In Total: {getTotalBarang(productIn)}
              </Typography>
            </Box>
          </>
        ) : (
          <>
            <Typography variant="h6" gutterBottom>
              Product Out Report
            </Typography>
            <div style={{ height: 400, width: '100%' }}>
              <DataGrid
                rows={productOut}
                columns={columnsOut}
                pageSize={5}
                rowsPerPageOptions={[5]}
                getRowId={(row) => row.id_barang_keluar || row.id_product_out} // Fallback ID
              />
            </div>

            {/* Display total products out */}
            <Box mt={2}>
              <Typography variant="h6">
                Product Out Total: {getTotalBarang(productOut)}
              </Typography>
            </Box>
          </>
        )}
      </Container>
    </Main>
  );
}
