var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var session = require('express-session');
var fs = require("fs");
var multer = require("multer");
var moment = require('moment');
let grpc = require("grpc");
var protoLoader = require("@grpc/proto-loader");
var request = require("request");
var mongoose = require('mongoose');
//var Mongoose = require('mongoose').Mongoose;

// express server setting
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

var hostname = '143.248.148.131'
var port = 55560
var server = app.listen(port, hostname, function(){
    server.setTimeout( 3 * 60 * 1000 )
    console.log("Express server has started on port %d", port)
});


// input_model_form -> file 포함한 데이터 submit 시, file 저장 방법
const upload = multer({
  storage: multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, './data/model_upload/');
    },
    filename: function (req, file, cb) {
      cb(null, req.body.model_name + "." + (file.originalname).split(".")[1]);
    }
  }),
});


// grpc server setting
const PROTO_PATH = './router/protos/streamDL.proto'
const streamDLbroker = grpc.load(PROTO_PATH).streamDL.streamDLbroker
const client = new streamDLbroker('143.248.148.131:50091', grpc.credentials.createInsecure())


//var instanceTrain = new Mongoose();
//var instanceInfer = new Mongoose();

//instanceTrain.connect('mongodb://192.168.54.145:27017/onlinedl', {useNewUrlParser: true});
//instanceInfer.connect('mongodb://192.168.54.145:27017/inference', {useNewUrlParser: true});

var instanceTrain = mongoose.createConnection('mongodb://192.168.153.193:27017/onlinedl', {useNewUrlParser: true});
var instanceInfer = mongoose.createConnection('mongodb://192.168.153.193:27017/inference', {useNewUrlParser: true});

//var db1 = instanceTrain.connection;
//db1.on('error', console.error);
//db1.once('open', function(){
    // CONNECTED TO MONGODB SERVER
//    console.log("Connected to instanceTrain DB server");
//});

//var db2 = instanceInfer.connection;
//db2.on('error', console.error);
//db2.once('open', function(){
    // CONNECTED TO MONGODB SERVER
//    console.log("Connected to instanceInfer DB server");
//});

// mongoDB server connection
//mongoose.connect('mongodb://192.168.54.133:27017/inference', {useNewUrlParser: true});

//var db = mongoose.connection;
//db.on('error', console.error);
//db.once('open', function(){
    // CONNECTED TO MONGODB SERVER
//    console.log("Connected to mongod server");
//});


app.use(express.static('public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(session({
    secret: '@#@$MYSIGN#@$#$',
    resave: false,
    saveUninitialized: true
}));

//var router = require('./router/main')(app, fs, upload, grpc, client, request, mongoose);
var router = require('./router/main')(app, fs, upload, grpc, client, request, mongoose, instanceTrain, instanceInfer);
