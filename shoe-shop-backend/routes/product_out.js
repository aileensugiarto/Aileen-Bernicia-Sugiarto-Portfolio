const express = require('express');
const router = express.Router();
const cors = require('cors');
router.use(cors());

const { body, validationResult } = require(`express-validator`);

const connection = require('../config/database');

/**
 * INDEX PRODUCT OUT
 */

router.get('/', function (request, response) {
  connection.query('SELECT po.id_product_out, po.id_product, p.name, po.product_out_date, po.amount FROM product_out po JOIN product p ON po.id_product = p.id_product',
    function (err, rows) {
      if (err) {
        return response.status(500).json({
          status: false,
          message: "Internal Server Error",
        });
      } else {
        return response.status(200).json({
          status:true,
          message: 'Product Out List',
          data_barang: rows
        });
      }
    }
  );
});


/**
 * GET PRODUCT OUT BY ID
 */
router.get('/:id_product_out', function(req, res) {
  const id = req.params.id_product;

  connection.query('SELECT * FROM product_out WHERE id_product_out = ?', [id], function(err, rows) {
    if (err) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error',
      });
    }

    if (rows.length === 0) {
      return res.status(404).json({
        status: false,
        message: 'Data not found',
      });
    }

    return res.status(200).json({
      status: true,
      message: 'Data retrieved successfully',
      data_barang: rows[0],
    });
  });
});


/**
 * CREATE PRODUCT OUT
 */
router.post('/create', [
  body('id_product').notEmpty(),
  body('product_out_date').notEmpty(),
  body('amount').notEmpty(),
], (req, res) => {

  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    return res.status(422).json({
      errors: errors.array()
    });
  }

  let formData = {
    id_product: req.body.id_product,
    product_out_date: req.body.product_out_date,
    amount: req.body.amount
  }

  connection.query('INSERT INTO product_out SET ?', formData, function (err, result) {
    if (err) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error',
      });
    } else {
      return res.status(201).json({
        status: true,
        message: 'Data Inserted Successfully',
        data: result.insertId, // Return the inserted ID
      });
    }
  });
});


/**
 * UPDATE PRODUCT OUT
 */

router.put('/update', [
  body('id_product').notEmpty(),
  body('product_out_date').notEmpty(),
  body('amount').notEmpty(),
], (req, res) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    return res.status(422).json({
      errors: errors.array()
    });
  }

  let id = req.body.id_product;

  let formData = {
    id_product: req.body.id_product,
    product_out_date: req.body.product_out_date,
    amount: req.body.amount
  }

  connection.query(`UPDATE product_out SET ? WHERE id_product_out = ${id}`, formData, (err, rows) => {
    if (err) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error'
      });
    } else {
      return res.status(200).json({
        status: true,
        message: 'Data Updated Successfully!'
      });
    }
  });
});


/**
 * DELETE PRODUCT OUT
 */

router.delete('/delete/(:id_product_out)', function (req, res) {
  let id = req.params.id_product_out; // Change from id_barang to id_product_out

  connection.query(`DELETE FROM product_out WHERE id_product_out = ${id}`, function (error, rows) {
    if (error) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error',
      });
    } else {
      return res.status(200).json({
        status: true,
        message: 'Data Deleted Successfully'
      });
    }
  });
});



// Total Product Out
router.get('/total_product_out', function(request, response) {
  connection.query('SELECT count(id_product_out) as total_product FROM product_out',
    function (err, rows) {
      if (err) {
        return response.status(500).json({
          status: false,
          message: 'Internal Server Error',
        });
      } else {
        return response.status(200).json({
          status: true,
          data_total_barang: rows
        });
      }
    }
  );
});

module.exports = router;