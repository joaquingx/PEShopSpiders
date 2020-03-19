const router = require('express').Router();

router.route('/').get((req, res) => {
    res.send('<h1 style="color: blue; margin-left: 45%">Healthy server!<h1>')
});

module.exports = router;
