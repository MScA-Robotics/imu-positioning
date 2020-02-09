const sleep = require('sleep');

module.exports = {
  logRequestPaths: (req, res, next) => {
    console.log(`${req.method} request made to: ${req.url}`);
    next();
  },
  
  /**
   * serveBuild: (req, res) => {
   *   res.sendFile(path.join(__dirname, 'build', 'index.html'));
   * },
   */
  
  homePostTest: (req, res) => {
    console.log(req);
    res.send("POST Received");
  },
  
  driveBoard: (req, res) => {
    let paramsName = req.params.route_name;
    res.render("drive/index", { 
      layout: 'layouts/emmet',
      title: 'Drive',
      name: paramsName
    });
  }
}
