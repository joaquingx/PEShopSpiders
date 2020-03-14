const router = require('express').Router();
let Results = require('../models/results.model');
// const utils = require('../utils/routes_utils');
// import appendToArray from '../utils/routes_utils'

function appendToArray(arr, toAppend){
    return arr.concat(toAppend)
}
function comparePrices(a,b ){
    if (b[1] === 'Not Found'){
        return -1;
    } else if(a[1] === 'Not Found'){
        return 1;
    }
    if (a[1] < b[1]){
        return -1;
    } else{
        return 1;
    }
}

function beautifyDescription(desc){
    console.dir(desc);
    if(desc === 'card_prices'){
        return 'Con Tarjeta' ;
    } else if(desc === 'regular_prices'){
        return 'Fisico';
    } else{
        return 'Online';
    }
}

function normalizePrice(market,  price, key){
    let price_number = price;
    if (!isNaN(price)){
        price_number = Number(price_number);
    }
    if (price_number === 0){
        price_number = 'Not Found';
    }
    return [market + '(' + beautifyDescription(key) + ')', price_number]
}

function sortInformation(result){
    keys = [
        'card_prices',
        'online_prices',
        'regular_prices',
    ];
    prices = [];
    for (const [key, value] of Object.entries(result._doc)) {
        if (keys.includes(key)){
            for (var price_dict of Array.from(value)){
                for (const [market, price] of Object.entries(price_dict)){
                    prices.push(normalizePrice(market, price, key));
                }
            }

        }
    }
    prices.sort(comparePrices);
    return prices;
}



router.route('/').get((req, res) => {
   Results.find()
       .then(result => res.json(result))
       .catch(err => res.status(400).json('Error: '+ err));
});

router.route('/:id').get((req, res) => {
   Results.findById(req.params.id)
       .then(result => {
           result._doc.sorted_prices = sortInformation(result);
           return res.json(result);
       })
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
