import React, { useState, useEffect } from 'react';
import axios from "axios";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  MenuItem,
  TextField,
  InputLabel,
  Select
} from '@mui/material';
import { styled } from '@mui/material/styles';
import MUIDataTable from 'mui-datatables';
// import Typography from '@mui/material/Typography';

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
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function ProductIn({ open }) {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({
    id_product_in: "",
    id_product: "",
    product_in_date: "",
    amount: "",
    // keterangan: "",
  });

  const [editing, setEditing] = useState(false);
  const [dialogOpen, setOpen] = useState(false);
  const [barangOption, setBarangOption] = useState([]);

  useEffect(() => {
    getData();
    getBarangOption();
  }, []);

  const getData = () => {
    // axios.get('https://aileen.kreatiftechno.com/barang_masuk.php')
    axios.get('http://localhost:5000/api/product_in')
      .then(response => {
        setItems(response.data.data_barang);
      })
      .catch(error => {
        console.log(error);
      });
  }

  const getBarangOption = () => {
    // axios.get('https://aileen.kreatiftechno.com/barang.php')
    axios.get('http://localhost:5000/api/product')
      .then(response => {
        setBarangOption(response.data.data_barang);
      })
      .catch(error => {
        console.log(error);
      });
  }

  const changeForm = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  const createData = async () => {
    if (editing) {
      // await axios.put("https://aileen.kreatiftechno.com/barang_masuk.php", form);
      await axios.put("http://localhost:5000/api/product_in/update", form);
    } else {
      await axios.post("http://localhost:5000/api/product_in/create", form);
    }
    setForm({
      id_product_in: "",
      id_product: "",
      product_in_date: "",
      amount: "",
    });
    setEditing(false);
    setOpen(false);
    getData();
  }

  const updateData = (event) => {
    setForm(event);
    setEditing(true);
    setOpen(true);
  }

  const deleteData = (id) => {
    axios.delete(`http://localhost:5000/api/product_in/delete/${id}`)
      .then(response => {
        getData();
      })
      .catch(error => {
        console.log(error);
      });
  }

  const handleClickOpen = () => {
    setForm({
      id_product_in: "",
      id_product: "",
      product_in_date: "",
      amount: "",
    });
    setEditing(false);
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  const columns = [
    { name: "name", label: "Name", options: { filter: true, sort: true } },
    { name: "product_in_date", label: "Product In Date", options: { filter: true, sort: true } },
    { name: "amount", label: "Amount", options: { filter: false, sort: false } },
    {
      name: "actions",
      label: "Actions",
      options: {
        filter: false,
        sort: false,
        customBodyRender: (value, tableMeta) => {
          const item = items[tableMeta.rowIndex];
          return (
            <div>
              <Button variant="contained" color="primary" onClick={() => updateData(item)}>
                Edit
              </Button>
              <Button variant="contained" color="secondary" onClick={() => deleteData(item.id_product)}>
                Delete
              </Button>
            </div>
          );
        },
      },
    },
  ];

  const options = {
    filterType: "checkbox",
  }

  return (
    <Main open={open}>
      <DrawerHeader />
      <Button variant='contained' color='primary' onClick={handleClickOpen} style={{ marginBottom: 10 }}>
        Add Product In
      </Button>

      <Dialog open={dialogOpen} onClose={handleClose}>
        <DialogTitle>{editing ? "Edit Product In" : "Add Product In"}</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin='dense' >
            <InputLabel id='id_product-label'>Name</InputLabel>
            <Select label='name' name='id_product' value={form.id_product} onChange={changeForm} required>
              {barangOption.map((barang) => (
                <MenuItem key={barang.id_product} value={barang.id_product}>{barang.name}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin='dense'
            name='product_in_date'
            type='date'
            label='Product In Date'
            fullWidth
            value={form.product_in_date}
            onChange={changeForm}
            InputLabelProps={{ shrink: true, }}
            required
          />
          <TextField
            margin='dense'
            name='amount'
            label='Amount'
            fullWidth
            value={form.amount}
            onChange={changeForm}
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color='secondary'>
            Cancel
          </Button>
          <Button onClick={createData} color='primary'>
            {editing ? "Update" : "Add"}
          </Button>
        </DialogActions>
      </Dialog>

      <MUIDataTable
        title={"Product In"}
        data={items}
        columns={columns}
        options={options} />
    </Main>
  );
}
