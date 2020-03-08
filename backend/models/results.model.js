const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const resultsSchema = new Schema({
    name: String,
    card_prices: Array,
    descriptions: Array,
    regular_prices: Array,
    online_prices: Array,
    starrs: Array,
    stocks: Array,
    urls: Object,
});

const Result = mongoose.model('results', resultsSchema);

module.exports = Result;
