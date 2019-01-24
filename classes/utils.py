import os, shutil
from classes.asar import Asar

class BaseUtils:
    def prompt_for(self, message, valid_responses=None, default_response='', response_case_sensitive=False):
        if valid_responses is None:
            valid_responses = []

        message = self.process_input_message(message, valid_responses, default_response)

        is_valid_response = False
        response = ''
        while not is_valid_response:
            response = input(message).strip()
            if response == '' and default_response != '':
                response = default_response

            is_valid_response = self.validate_response(response, valid_responses, response_case_sensitive)

        return response

    def process_input_message(self, message, valid_responses, default_response):
        if len(valid_responses) > 0:
            message += ' (' + '/'.join(valid_responses) + ')'

        if len(default_response) > 0:
            message += ' - default is ' + default_response

        message += ': '

        return message

    def validate_response(self, response, valid_responses, response_case_sensitive):
        is_valid = False

        if len(valid_responses) == 0:
            is_valid = True
        else:
            for valid_response in valid_responses:
                if not response_case_sensitive:
                    if valid_response.strip().lower() == response.lower():
                        is_valid = True
                        break
                else:
                    if valid_response.strip() == response:
                        is_valid = True
                        break

        return is_valid

    def load_file(self, file):
        if not os.path.isfile(file):
            return ''

        with open(file, 'r') as content_file:
            content = content_file.read()
        return content

    def generate_js_variable(self, data):
        lines = []

        for feature_name, feature in data.items():
            for name, value in feature.items():
                lines.append("let beemka_" + feature_name + "_" + name + " = \"" + value.replace('"', '\\"') + "\";")

        return lines

    def event_exists(self, file_contents, event_type, event_name):
        return self.event_position(file_contents, event_type, event_name) != -1

    def event_position(self, file_contents, event_type, event_name):
        # app.once + ready becomes app.once('ready'
        event = event_type + "('" + event_name + "'"
        return file_contents.find(event)

    def inject_code(self, file_contents, event_type, event_name, payload, function_definition):
        if self.event_exists(file_contents, event_type, event_name):
            file_contents = self.inject_code_when_event_exists(file_contents, event_type, event_name, payload)
        else:
            file_contents = self.inject_code_when_event_does_not_exist(file_contents, payload, function_definition)

        return file_contents

    def inject_code_when_event_exists(self, file_contents, event_type, event_name, payload):
        instance_start = self.event_position(file_contents, event_type, event_name)
        if instance_start == -1:
            return False

        function_starts_at = file_contents.find('{', instance_start)
        if function_starts_at == -1:
            return False

        part_left = file_contents[:function_starts_at + 1]
        part_right = file_contents[function_starts_at + 1:]

        file_contents = part_left + "\n\n" + payload + "\n\n" + part_right

        return file_contents

    def inject_code_when_event_does_not_exist(self, file_contents, payload, function_definition):
        function = function_definition.replace('%FUNCTION_CODE%', payload)
        file_contents += "\n\n" + function + "\n\n"

        return file_contents

    def get_function_definition(self, file_contents, event_type, event_name):
        instance_start = self.event_position(file_contents, event_type, event_name)
        if instance_start == -1:
            return False

        function_starts_at = file_contents.find('{', instance_start)
        if function_starts_at == -1:
            return False

        # Now we need to find out what the BrowserWindow variable is called.
        function_definition_starts_at = file_contents.find('function', instance_start)
        if function_definition_starts_at == -1:
            return False

        function_definition_ends_at = file_contents.find(')', function_definition_starts_at)
        if function_definition_ends_at == -1:
            return False

        function_definition_text = file_contents[function_definition_starts_at + len(
            'function'):function_definition_ends_at + 1].strip().strip('()').replace(' ', '')
        return function_definition_text

    def get_function_positional_argument(self, function_definition, argument_position):
        function_params = function_definition.split(',')

        argument_position -= 1

        if argument_position >= len(function_params):
            return False

        return function_params[argument_position].strip()

    def compress_asar(self, path, output_file):
        try:
            with Asar.from_path(path) as a:
                with open(output_file, 'wb') as f:
                    a.fp.seek(0)
                    f.write(a.fp.read())
        except Exception as e:
            return False

        return True

    def extract_asar(self, input_file, output_folder):
        try:
            with Asar.open(input_file) as archive:
                archive.extract(output_folder)
        except Exception as e:
            return False

        return True

    def remove_directory(self, directory):
        shutil.rmtree(directory)