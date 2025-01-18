const express = require("express");
const router = express.Router();
const { body, validationResult } = require(`express-validator`);
const bcrypt = require("bcryptjs");
const connection = require("../config/database");

/**
 * REGISTER
 */

router.post(
  "/register",
  [
    body("username").notEmpty().withMessage("Invalid username"),
    body("password")
      .isLength({ min: 6 })
      .withMessage("Password min 6 characters")
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }

    const { username, password } = req.body;

    connection.query(
      "SELECT * FROM user WHERE username = ?",
      [username],
      (err, result) => {
        if (err) {
          return res.status(500).json({ message: "Internal Server Error" });
        }

        if (result.length > 0) {
          return res.status(400).json({ message: "Username already registered" });
        }

        bcrypt.hash(password, 10, (err, hashedPassword) => {
          if (err) {
            return res.status(500).json({ message: "Error hashing password" });
          }

          const formData = { username, password: hashedPassword }
          connection.query("INSERT INTO user SET ?", formData, (err, rows) => {
            if (err) {
              return res.status(500).json({ message: "Internal Server Error" });
            }
            return res
              .status(201)
              .json({ message: "User registered successfully" });
          });
        });
      }
    );

  }
);


/**
 * LOGIN
 */

router.post(
  "/login",
  [
    body("username").notEmpty().withMessage("Invalid username"),
    body("password").notEmpty().withMessage("Password is required"),
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }

    const { username, password } = req.body;

    connection.query(
      "SELECT * FROM user WHERE username = ?",
      [username],
      (err, result) => {
        if (err) {
          return res.status(500).json({ message: "Internal Server Error" });
        }

        if (result.length === 0) {
          return res.status(404).json({ message: "User not found" });
        }

        const user = result[0];

        bcrypt.compare(password, user.password, (err, isMatch) => {
          if (err || !isMatch) {
            return res
              .status(400)
              .json({ message: "Invalid username or password" });
          }

          // Jika password cocok, buat token JWT
          return res.status(200).json({
            message: "Login successful",
            user: {
              id: user.id,
              username: user.username,
            }
          });
        });
      }
    );
  }
);

module.exports = router;
