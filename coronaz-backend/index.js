"use strict";

const http = require('http');
const mongoose = require('mongoose');

const port = 9000;

// No app and config yet
//const app = require('./src/app');
//const config = require('./src/config');

// Set API port
//app.set('port', port);

// Create server
const server = http.createServer();

// Connect to MongoDB database
mongoose.connect("mongodb://telerik:123@host.docker.internal/coronaz", { useNewUrlParser: true })
    .then(() => server.listen(config.port))
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