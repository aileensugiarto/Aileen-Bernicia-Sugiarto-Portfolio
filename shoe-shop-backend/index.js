const express = require("express");
const app = express();
const port = 5000;
const cors = require("cors");
const bodyParser = require("body-parser");

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Import routers
const authRouter = require("./routes/auth");
const productRouter = require("./routes/product");
const productInRouter = require("./routes/product_in");
const productOutRouter = require("./routes/product_out");

// Use routers
app.use("/api/auth", authRouter);
app.use("/api/product", productRouter);
app.use("/api/product_in", productInRouter);
app.use("/api/product_out", productOutRouter);

app.listen(port, () => {
  console.log(`App running at http://localhost:${port}`);
});
