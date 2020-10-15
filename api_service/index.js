const express = require("express");
const app = express();
const port = 4000;

app.get("/", (req, res) => {
  res.json({ user: "sid200026" });
});

app.listen(port, () => {
  console.log(`Example app listening at Port ${port}`);
});
