var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser');
var ConsommationModel = require('../models/consommation.model.js');
const { route } = require('express/lib/application');

var jsonParser = bodyParser.json();

router.post('/', jsonParser, async function (req, res) {

  var data_date = req.body.date;
  
  const { exec } = require('child_process');

  let yourscript = exec(`python3 /mnt/f/Data/TiengPhap/Keyce/KitGame2/Code/openit-stonehenge/python/getdata.py "${data_date}" "" 1`,
    (error, stdout, stderr) => {
      if (error !== null) {
        console.log(`exec error: ${error}`);
      }
    });
  // companyService.ExportEmployFromTheName(data);

  res.send(JSON.stringify(req.body));
});


router.get('/get-data/:date', jsonParser, async function (req, res) {
  var data_date = "";
  if (req.body.date)
    data_date = req.body.date_date;

  ConsommationModel.find(
    { $or: [{ date: data_date }] },
    function (err, result) {
      if (err) {
        res.send(err);
      } else {
        res.send(JSON.stringify(result));
      }
    })

});

module.exports = router;
