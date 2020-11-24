"use strict";

const http = require('http');
const mongoose = require('mongoose');
const express = require('express');

const port = 9000;

// Create app
const aggregatedView = require("./routes/aggregated_view");

const app = express();
app.set('port', port);
app.use(aggregatedView)

// Create server
const server = http.createServer(app);

// Connect to MongoDB database
mongoose.connect("mongodb://telerik:123@host.docker.internal/coronaz", { useNewUrlParser: true })
    .then(() => server.listen(port))
    .catch(err => {
        console.log('Error connecting to the database', err.message);
        process.exit(err.statusCode);
    })

server.on('listening', () => {
    console.log(`API is running on port ${port}`);
});

server.on('error', (err) => {
    console.log('Error', err.message);
    process.exit(err.statusCode);
});