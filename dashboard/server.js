var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var session = require('express-session');
var fs = require("fs");
var multer = require("multer");
var moment = require('moment');
let grpc = require("grpc");
var protoLoader = require("@grpc/proto-loader")
var mongoose    = require('mongoose');


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


// mongoDB server connection
mongoose.connect('mongodb://192.168.54.133:27017/inference', {useNewUrlParser: true});

var db = mongoose.connection;
db.on('error', console.error);
db.once('open', function(){
    // CONNECTED TO MONGODB SERVER
    console.log("Connected to mongod server");
});


app.use(express.static('public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(session({
    secret: '@#@$MYSIGN#@$#$',
    resave: false,
    saveUninitialized: true
}));

var router = require('./router/main')(app, fs, upload, grpc, client, mongoose);
