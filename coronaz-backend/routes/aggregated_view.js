  
var express = require('express');
var router = express.Router();

const aggregatedController = require('../controllers/aggregated_controller');

router.get('/data', aggregatedController.getData);

module.exports = router;