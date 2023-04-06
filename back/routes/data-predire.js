var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser');
var consommationModel = require('../models/consommation.model.js');
const { route } = require('express/lib/application');
var moment = require('moment');

var jsonParser = bodyParser.json();

router.get('/push-data/:data_date', jsonParser, async function (req, res) {

  var data_date = "";
  if (req.params.data_date)
    data_date = req.params.data_date;

  console.log(data_date);

  const arrayDate = data_date.split("-");
  console.log(arrayDate);

  var newDate = arrayDate[3] + "-" + arrayDate[2] + "-" + arrayDate[1] + " GMT";
  var datePredict = new Date(newDate);

  console.log(datePredict)

  // for (i = 0; i++; i <= 15) {
  //   var formattedDate = moment(datePredict.addDays(i)).format('dd-MM-yyyy');
  //   console.log(formattedDate);
  // }

  const { spawn } = require('child_process');

  let yourscript = spawn('python3', ['/mnt/f/Data/TiengPhap/Keyce/KitGame2/Code/openit-stonehenge/python/getdata.py', data_date]); //exec(`python3 /mnt/f/Data/TiengPhap/Keyce/KitGame2/Code/openit-stonehenge/python/getdata.py "${data_date}" "" 1`,
  await yourscript.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  await yourscript.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  await yourscript.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
  // (error, stdout, stderr) => {
  //   if (error !== null) {
  //     console.log(`exec error: ${error}`);
  //   }
  // });
  // companyService.ExportEmployFromTheName(data);

  res.send("ok");
});


router.get('/get-data/:data_date', async function (req, res, next) {
  var data_date = "";
  if (req.params.data_date)
    data_date = req.params.data_date;

  console.log(data_date);

  const myMomentObject = moment(data_date, 'DD-MM-YYYY')
  var arrayDate = [];

  arrayDays = [];

  for (i = 1; i <= 12; i++) {
    var nextDay = moment(myMomentObject).add(i, 'days');
    arrayDate.push(moment(nextDay).format('DD-MM-YYYY'));
  }

  consommationModel.find({ 'data_date': { $in: arrayDate } },
    function (err, result) {
      if (err) {
        res.send(err);
      } else {
        res.send(JSON.stringify(result));
      }
    });
});

module.exports = router;
