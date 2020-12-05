const getData = (req, res) => {

    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://telerik:123@mongo/coronaz";

    MongoClient.connect(url, function(err, db) {
        if (err) {
            console.log(`Could not connect to database: ${err}`)
            res.status(500).send({});
        } else {
            var dbo = db.db("coronaz");
            dbo.collection("coronaz").find({}).toArray((err, result) => {
                if (err) {
                    console.log(`Could not connect to database: ${err}`)
                    res.status(500).send({});
                } else {
                    res.status(200).send({ result });
                    db.close();
                }
            });
        }
    })
};

module.exports = {
    getData
};