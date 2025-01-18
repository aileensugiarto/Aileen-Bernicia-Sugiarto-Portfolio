import * as React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './Dashboard';
import Product from './Product';
import ProductIn from './ProductIn';
import ProductOut from './ProductOut';
import Report from './Report';

export default function URLRoute ({ open }) {
  return (
    <div style={{
      flexGrow: 1,
      padding: "16px",
      marginLeft: open ? "240px" : "0",
      transition: "margin 0.3s",
    }}>
      <Routes>
        <Route path='/dashboard' element={<Dashboard />} />
        <Route path='/product' element={<Product />} />
        <Route path='/productIn' element={<ProductIn />} />
        <Route path='/productOut' element={<ProductOut />} />
        <Route path='/report' element={<Report />} />
      </Routes>
    </div>
  );
}