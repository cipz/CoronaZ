const getData = (req, res) => {

    var MongoClient = require('mongodb').MongoClient;
    // Linux
    var url = "mongodb://telerik:123@mongo/coronaz";
    // Windows
    // var url = "mongodb://telerik:123@host.docker.internal/coronaz";

    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("coronaz");
        dbo.collection("coronaz").find({}).toArray((err, result) => {
            if (err) throw err;
            res.status(200).send({ result });
            db.close();
        });
    });
};

module.exports = {
    getData
};