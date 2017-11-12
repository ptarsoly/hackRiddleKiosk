var express = require('express');
var bodyParser = require('body-parser');
//var cors = require('cors');
var app = express();

var SerialPort = require('serialport');
var port = new SerialPort('/dev/tty96B0', { autoOpen: false });

port.open(function (err) {
    if (err) {
      return console.log('Error opening port: ', err.message);
    }
});
//app.use(cors());

app.use(bodyParser.json());

var jsonData = {
    "user" : null
};

app.post('/', function(request, response){
  console.log(request.body);      // your JSON
  jsonData.user = request.body.user;
   response.send( ( verify() ) ? '1' : '0' );    // echo the result back
});


app.get('/data',function(request, response){
    response.send("Hello World");
});

app.listen(3001, "0.0.0.0");

function verify() {
    if(jsonData.user<4 && jsonData.user>-1) {
        //serial code
        var byteToSend = 0xc0;
        byteToSend = byteToSend | jsonData.user;
        port.write(byteToSend, function( error ) {
            if(error) {
                console.log(error);
            }
        });
        var verified = port.read();
        
        if(verified.find('1')) {
            return true;
        }
        else {
            return false;
        }
    }
};