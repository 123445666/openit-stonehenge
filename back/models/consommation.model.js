const mongoose = require("mongoose");
var _ = require('lodash');
const Schema = mongoose.Schema;

// Define the meal schema
const consommationSchema = new Schema({
  consommation:
  {
    type: Number,
  },
  data_date:
  {
    type: String,
    required: true
  }
});

const consommationModel = mongoose.model("consommations", consommationSchema);

module.exports = consommationModel;
