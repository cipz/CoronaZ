"use strict";

const http = require('http');
const express = require('express');
const cors = require('cors');

const port = 9000;

// Create app
const aggregatedView = require("./routes/aggregated_view");

const app = express();
app.set('port', port);

app.use(cors())
app.use(aggregatedView)

// Create server
const server = http.createServer(app);

server.listen(port);

server.on('listening', () => {
    console.log(`API is running on port ${port}`);
});

server.on('error', (err) => {
    console.log('Error', err.message);
    process.exit(err.statusCode);
});