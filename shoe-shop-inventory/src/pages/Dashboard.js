import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { CardActionArea } from '@mui/material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBox, faPencilSquare, faAngleDoubleDown, faAngleDoubleUp } from '@fortawesome/free-solid-svg-icons';
import axios from "axios";
import React, { useState, useEffect } from "react";

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

const CardContainer = styled('div')({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  gap: '20px',
});

export default function Dashboard({ open }) {
  const [totalProduct, setTotalProduct] = useState(0);
  const [totalProductIn, setTotalProductIn] = useState(0);
  const [totalProductOut, setTotalProductOut] = useState(0);

  useEffect(() => {
    fetchTotalProduct();
    fetchTotalProductIn();
    fetchTotalProductOut();
  }, []);

  const fetchTotalProduct = () => {
    axios.get('http://localhost:5000/api/product/total_product')
      .then(response => {
        setTotalProduct(response.data.data_total_product[0].total_product);
      })
      .catch(error => {
        console.log(error);
      });
  };

  const fetchTotalProductIn = () => {
    axios.get('http://localhost:5000/api/product_in/total_product_in')
      .then(response => {
        setTotalProductIn(response.data.data_total_product_in[0].total_product_in);
      })
      .catch(error => {
        console.log(error);
      });
  };

  const fetchTotalProductOut = () => {
    axios.get('http://localhost:5000/api/product_out/total_product_out')
    .then(response => {
      setTotalProductOut(response.data.data_total_product_out[0].total_product_out);
    })
    .catch(error => {
      console.log(error);
    });
  };

  return (
    <Main open={open}>
      <DrawerHeader />
      <CardContainer>
        <Card style={{ width: '300px', backgroundColor: 'white' }}>
          <CardActionArea>
            <div style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
              <FontAwesomeIcon icon={faBox} style={{ fontSize: 100, color: '#1976D2' }} />
            </div>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Product
              </Typography>
              {/* Removed total */}
            </CardContent>
          </CardActionArea>
        </Card>

        <Card style={{ width: '300px' }}>
          <CardActionArea>
            <div style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
              <FontAwesomeIcon icon={faAngleDoubleDown} style={{ fontSize: 100, color: '#1976D2' }} />
            </div>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Product In
              </Typography>
              {/* Removed total */}
            </CardContent>
          </CardActionArea>
        </Card>

        <Card style={{ width: '300px' }}>
          <CardActionArea>
            <div style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
              <FontAwesomeIcon icon={faAngleDoubleUp} style={{ fontSize: 100, color: '#1976D2' }} />
            </div>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Product Out
              </Typography>
              {/* Removed total */}
            </CardContent>
          </CardActionArea>
        </Card>

        <Card style={{ width: '300px' }}>
          <CardActionArea>
            <div style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
              <FontAwesomeIcon icon={faPencilSquare} style={{ fontSize: 100, color: '#1976D2' }} />
            </div>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Report
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </CardContainer>
    </Main>
  );
}
