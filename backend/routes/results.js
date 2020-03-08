const router = require('express').Router();
let Results = require('../models/results.model');


router.route('/').get((req, res) => {
   Results.find()
       .then(result => res.json(result))
       .catch(err => res.status(400).json('Error: '+ err));
});

module.exports = router;