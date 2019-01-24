import os, pprint

class ModuleManager:
    def __init__(self, module_path, utils):
        self.utils = utils
        self.module_path = module_path
        self.modules = self.load_modules(self.module_path)

    def get_loaded_modules(self):
        return self.modules

    def load_modules(self, module_path):
        modules = {}
        for folder in os.listdir(module_path):
            path = os.path.join(module_path, folder)
            module = self.parse_module(path)
            if module:
                module['folder'] = folder
                modules[module['module']] = module

        return modules

    def parse_module(self, folder):
        module_file = os.path.join(folder, 'module.beemka')
        if not os.path.isfile(module_file):
            return False

        data = self.utils.load_file(module_file)
        signature = self.parse_signature(data)
        signature['path'] = folder

        return signature

    def parse_signature(self, data):
        signature = {}
        lines = data.split("\n")
        feature = ''
        for line in lines:
            info = self.parse_signature_line(line)
            if not info:
                continue

            if info['type'] == 'feature':
                # This should be the first element.
                if not 'features' in signature:
                    signature['features'] = {}

                feature = info['name']
                signature['features'][feature] = {}
            elif info['type'] == 'required' or info['type'] == 'option':
                if not 'params' in signature['features'][feature]:
                    signature['features'][feature]['params'] = {}

                if not info['type'] in signature['features'][feature]['params']:
                    signature['features'][feature]['params'][info['type']] = {}

                signature['features'][feature]['params'][info['type']][info['name']] = {
                    'name': info['name'],
                    'default': info['default'],
                    'description': info['description']
                }
            elif info['type'] == 'module' or info['type'] == 'author' or info['type'] == 'module_description' or info['type'] == 'event':
                signature[info['type']] = info['name']
            elif info['type'] == 'description':
                signature['features'][feature]['description'] = info['name']

        return signature

    def parse_signature_line(self, line):
        line = line.strip()
        if line[:1] != '@':
            return False

        # Get the first part.
        space = line.find(' ')
        if space == -1:
            return False

        type = line[:space].strip().lstrip('@')
        name = ''
        default = ''
        description = ''
        data = line[space:].strip()

        if type == 'module' or type == 'author' or type == 'feature' or type == 'description' or type == 'module_description' or type == 'event':
            name = data
        elif type == 'required' or type == 'option':
            comma = data.find(',')
            if comma == -1:
                return False

            name = data[:comma].strip()
            data = data[comma + 1:].strip()

            if type == 'required':
                description = data
            else:
                comma = data.find(',')
                if comma == -1:
                    default = data
                else:
                    default = data[:comma].strip()
                    description = data[comma + 1:].strip()

        return {
            'type': type,
            'name': name,
            'default': default,
            'description': description
        }

    def collect_data(self, module):
        data = self.make_data_object(module)

        for name, feature in module['features'].items():
            print("Gathering data for feature: " + feature['description'])

            if 'required' in feature['params'] and 'enabled' in feature['params']['required']:
                response = self.utils.prompt_for(feature['params']['required']['enabled']['description'], valid_responses=['true', 'false'], default_response='true').lower()
                data[name]['enabled'] = response

                if response == 'false':
                    continue

            for param_type in ['required', 'option']:
                if not param_type in feature['params']:
                    continue

                for param_name, param in feature['params'][param_type].items():
                    if param_name == 'enabled':
                        # We already did this.
                        continue

                    response = self.utils.prompt_for(param['description'],default_response=param['default'])
                    data[name][param_name] = response

        return data

    def make_data_object(self, module):
        data = {}

        for name, feature in module['features'].items():
            if not name in data:
                data[name] = {}

            for param_type in ['required', 'option']:
                if not param_type in feature['params']:
                    continue

                for param_name, param in feature['params'][param_type].items():
                    if not param_name in data[name]:
                        data[name][param_name] = param['default']

        return data

