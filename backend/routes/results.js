const router = require('express').Router();
let Results = require('../models/results.model');
// const utils = require('../utils/routes_utils');
// import appendToArray from '../utils/routes_utils'

function appendToArray(arr, toAppend){
    return arr.concat(toAppend)
}


router.route('/').get((req, res) => {
   Results.find()
       .then(result => res.json(result))
       .catch(err => res.status(400).json('Error: '+ err));
});

router.route('/:id').get((req, res) => {
   Results.findById(req.params.id)
       .then(result => res.json(result))
       .catch(err => res.status(400).json('Error' + err));
});

router.route('/update/:id').post((req,res) =>{
   Results.findById(req.params.id)
       .then(result => {
           result.card_prices = appendToArray(result.card_prices, req.body.card_prices);
           result.descriptions = appendToArray(result.descriptions, req.body.descriptions);
           result.regular_prices = appendToArray(result.regular_prices, req.body.regular_prices);
           result.online_prices = appendToArray(result.online_prices, req.body.online_prices);
           result.starss = appendToArray(result.starss, req.body.starss);
           result.stocks = appendToArray(result.stocks, req.body.stocks);
           result.urls = appendToArray(result.urls, req.body.urls);

           result.save()
               .then(() => res.json('Result Updated!'))
               .catch(err => res.status(400).json('Error ' + err))
       })
       .catch(err => res.status(400).json('Erroraso '+ err))
});

module.exports = router;