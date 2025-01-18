const express = require('express');
const router = express.Router();
const cors = require('cors');
router.use(cors());

const { body, validationResult } = require(`express-validator`);

const connection = require('../config/database');

/**
 * INDEX PRODUCT IN
 */

router.get('/', function (request, response) {
  connection.query('SELECT pi.id_product_in, pi.id_product, p.name, pi.product_in_date, pi.amount FROM product_in pi JOIN product p ON pi.id_product = p.id_product',
    function (err, rows) {
      if (err) {
        return response.status(500).json({
          status: false,
          message: "Internal Server Error",
        });
      } else {
        return response.status(200).json({
          status:true,
          message: 'Product In List',
          data_barang: rows
        });
      }
    }
  );
});


/**
 * GET PRODUCT BY ID
 */
router.get('/:id_product_in', function(req, res) {
  const id = req.params.id_barang;

  connection.query('SELECT * FROM product_in WHERE id_product_in = ?', [id], function(err, rows) {
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
 * CREATE PRODUCT IN
 */
router.post('/create', [
  body('id_product').notEmpty(),
  body('product_in_date').notEmpty(),
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
    product_in_date: req.body.product_in_date,
    amount: req.body.amount
  }

  connection.query('INSERT INTO product_in SET ?', formData, function (err, rows) {
    if (err) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error',
      });
    } else {
      return res.status(201).json({
        status: true,
        message: 'Data Inserted Successfully',
        data: rows[0]
      });
    }
  });
});


/**
 * UPDATE PRODUCT IN
 */

router.put('/update', [
  body('id_product').notEmpty(),
  body('product_in_date').notEmpty(),
  body('amount').notEmpty(),
], (req, res) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    return res.status(422).json({
      errors: errors.array()
    });
  }

  let id = req.body.id_product_in;

  let formData = {
    id_product: req.body.id_product,
    product_in_date: req.body.product_in_date,
    amount: req.body.amount
  }

  connection.query(`UPDATE product_in SET ? WHERE id_product_in = ${id}`, formData, (err, rows) => {
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
 * DELETE PRODUCT IN
 */

router.delete('/delete/(:id_product_in)', function (req, res) {
  let id = req.params.id_product_in;

  connection.query(`DELETE FROM product_in WHERE id_product_in = ${id}`, function (error, rows) {
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


// Total Product In
router.get('/total_product_in', function(request, response) {
  connection.query('SELECT count(id_product_in) as total_product FROM product_in',
    function (err, rows) {
      if (err) {
        return response.status(500).json({
          status: false,
          message: 'Internal Server Error',
        });
      } else {
        return response.status(200).json({
          status: true,
          data_total_product: rows
        });
      }
    }
  );
});

module.exports = router;