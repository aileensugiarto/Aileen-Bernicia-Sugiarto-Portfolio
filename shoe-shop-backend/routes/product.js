const express = require('express');
const router = express.Router();
const cors = require('cors');
router.use(cors());

const {body, validationResult} = require(`express-validator`);

const connection = require('../config/database');

/**
 * INDEX PRODUCT: menampilkan semua data
 */
router.get('/', function(request, response) {
  connection.query('SELECT * FROM product ORDER BY id_product desc',
    function (err, rows) {
    if (err) {
      return response.status(500).json({
        status: false,
        message: 'Internal Server Error',
      })
    } else {
      return response.status(200).json({
        status: true,
        message: 'Data Product List',
        data_barang: rows // data barang
      })
    }
  })
})


/**
 * GET PRODUCT BY ID
 */
router.get('/:id_product', function(req, res) {
  const id = req.params.id_product;

  connection.query('SELECT * FROM product WHERE id_product = ?', [id], function(err, rows) {
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
 * CREATE PRODUCT
 */

router.post('/create', [
  body('name').notEmpty(),
  body('description').notEmpty(),
  body('category').notEmpty(),
  body('unit_price').notEmpty(),
  body('stock').notEmpty()
], (req, res) => {

  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    return res.status(422).json({
      errors: errors.array()
    })
  }

  let formData = {
    name: req.body.name,
    description: req.body.description,
    category: req.body.category,
    unit_price: req.body.unit_price,
    stock: req.body.stock
  };

  connection.query('INSERT INTO product SET ?', formData, function (err, rows) {
    if (err) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error',
      })
    } else {
      return res.status(201).json ({
        status: true,
        message: 'Data Inserted Successfully',
        data: rows[0]
      })
    }
  })
});


/**
 * UPDATE PRODUCT
 */

router.put('/update', [

  body('id_product').notEmpty(),
  body('name').notEmpty(),
  body('description').notEmpty(),
  body('category').notEmpty(),
  body('unit_price').notEmpty(),
  body('stock').notEmpty()

], (req, res) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    return res.status(422).json({
      errors: errors.array()
    })
  }

  let id = req.body.id_product;

  let formData = {
    name: req.body.name,
    description: req.body.description,
    category: req.body.category,
    unit_price: req.body.unit_price,
    stock: req.body.stock
  }

  connection.query(`UPDATE product SET ? WHERE id_product = ${id}`, formData, (err, rows) => {
    if (err) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error'
      })
    } else {
      return res.status(200).json({
        status: true,
        message: 'Data Updated Successfully!'
      })
    }
  })
});


/**
 * DELETE BARANG
 */

router.delete('/delete/(:id_product)', function(req, res) {

  let id = req.params.id_product;

  connection.query(`DELETE FROM product WHERE id_product = ${id}`, function (error, rows) {
    if (error) {
      return res.status(500).json({
        status: false,
        message: 'Internal Server Error',
      })
    } else {
      return res.status(200).json({
        status: true,
        message: 'Data Deleted Successfully!'
      })
    }
  })

});


// Total Product
router.get('/total_product', function(request, response) {
  connection.query('SELECT count(id_product) as total_product FROM product',
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

