import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
} from '@mui/material';

import { styled } from '@mui/material/styles';
import MUIDataTable from 'mui-datatables';

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

export default function Product({ open }) {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({
    id_product: "",
    name: "",
    description: "",
    category: "",
    unit_price: "",
    stock: ""
  });
  const [editing, setEditing] = useState(false);
  const [dialogOpen, setOpen] = useState(false);

  useEffect(() => {
    getData();
  }, []);

  const getData = () => {
    // axios.get('https://aileen.kreatiftechno.com/barang.php')
    axios.get('http://localhost:5000/api/product')
      .then(response => {
        setItems(response.data.data_barang);
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
      // await axios.put("https://aileen.kreatiftechno.com/barang.php", form)
      await axios.put("http://localhost:5000/api/product/update", form)
    } else {
      // await axios.post("https://aileen.kreatiftechno.com/barang.php", form);
      await axios.post("http://localhost:5000/api/product/create", form);
    }
    setForm({
      id_product: "",
      name: "",
      description: "",
      category: "",
      unit_price: "",
      stock: "",
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
    // axios.delete(`https://aileen.kreatiftechno.com/barang.php?id_barang=${id}`)
    axios.delete(`http://localhost:5000/api/product/delete/${id}`)
      .then(response => {
        getData();
      })
      .catch(error => {
        console.log(error);
      });
  }

  const handleClickOpen = () => {
    setForm({
      id_product: "",
      name: "",
      description: "",
      category: "",
      unit_price: "",
      stock: "",
    });
    setEditing(false);
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  const columns = [
    { name: "name", label: "Name", options: { filter: true, sort: true } },
    {
      name: "description",
      label: "Description",
      options: {
        filter: false,
        sort: false,
        customBodyRender: (value) => {
          return (
            <div style={{ width: '150px', maxHeight: '60px', overflowY: 'auto' }}>
              {value}
            </div>
          );
        },
      },
    },
    { name: "category", label: "Category", options: { filter: true, sort: true } },
    { name: "unit_price", label: "Price", options: { filter: false, sort: false } },
    { name: "stock", label: "Stock", options: { filter: false, sort: false } },
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
      <Button variant="contained" color="primary" onClick={handleClickOpen} style={{ marginBottom: 10 }}>
        Add Product
      </Button>

      <Dialog open={dialogOpen} onClose={handleClose}>
        <DialogTitle>{editing ? "Edit Product" : "Add Product"}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="name"
            label="Name"
            fullWidth
            value={form.name}
            onChange={changeForm}
            required
          />
          <TextField
            autoFocus
            margin="dense"
            name="description"
            label="Description"
            fullWidth
            value={form.description}
            onChange={changeForm}
            required
          />
          <TextField
            autoFocus
            margin="dense"
            name="category"
            label="Category"
            fullWidth
            value={form.category}
            onChange={changeForm}
            required
          />
          <TextField
            autoFocus
            margin="dense"
            name="unit_price"
            label="Price"
            type="number"
            fullWidth
            value={form.unit_price}
            onChange={changeForm}
            required
          />
          <TextField
            autoFocus
            margin="dense"
            name="stock"
            label="Stock"
            fullWidth
            value={form.stock}
            onChange={changeForm}
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="secondary">
            Cancel
          </Button>
          <Button onClick={createData} color="primary">
            {editing ? "Update" : "Add"}
          </Button>
        </DialogActions>
      </Dialog>

      <MUIDataTable
        title={"Products"}
        data={items}
        columns={columns}
        options={options}
      />
    </Main>
  );
}
