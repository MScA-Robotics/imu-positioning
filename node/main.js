"use strict;"

const express = require('express'),
  path = require('path'),
  layouts = require('express-ejs-layouts'),
  app = express();

const driveController = require("./controllers/driveController"),
  errorController = require("./controllers/errorController");

app.set("port", process.env.PORT || 3000);
app.set("view engine", "ejs");

// Pre Route Middleware
app.use(layouts);
app.use(driveController.logRequestPaths);
app.use(express.urlencoded({extended: false}) );
app.use(express.static("public"));
app.use(express.json());

// Listen
app.listen(app.get("port"), () => {
  console.log(`Server running at http://localhost:${ app.get("port") }`)
});

// Main Routes
// app.get("/home", driveController.serveIndex);
app.get("/drive", driveController.drive);
app.get("/", driveController.drive);

// app.post("/ctl", driveController.ctl)

// Post Route Middleware
app.use(errorController.respondNoResourceFound);
app.use(errorController.respondInternalError);
app.use(errorController.logErrors);
