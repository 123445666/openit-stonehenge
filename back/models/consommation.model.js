const mongoose = require("mongoose");
var _ = require('lodash');
const Schema = mongoose.Schema;

// Define the meal schema
const consommationSchema = new Schema({
  consommation:
  {
    type: String,
    required: true
  },
  date:
  {
    type: String,
    required: true
  },
  hour:
  {
    type: String,
  }
});

const consommationModel = mongoose.model("consommations", consommationSchema);

module.exports = consommationModel;
