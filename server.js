var express = require('express');
var app = express();

//set report
var powrt = process.env.PORT || 8080

app.use(express.static(__dirname + "/public"));

// routes

app.get("/", function(req, res){
  res.render("index");
})

app.listen(port, function() {
  console.log("app running");
})
