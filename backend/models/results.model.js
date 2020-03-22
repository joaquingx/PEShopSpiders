const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const resultsSchema = new Schema({
    name: String,
    card_prices: Array,
    descriptions: Array,
    regular_prices: Array,
    online_prices: Array,
    starss: Array,
    stocks: Array,
    urls: Array,
});

const Result = mongoose.model('results', resultsSchema);

module.exports = Result;
