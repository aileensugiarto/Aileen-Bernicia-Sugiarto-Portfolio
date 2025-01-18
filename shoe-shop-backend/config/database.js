let mysql = require("mysql");

let connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "shoe_inventory",
});

connection.connect(function (error) {
  if (!error) {
    console.log(error);
  } else {
    console.log("Connection Successful");
  }
});

module.exports = connection;