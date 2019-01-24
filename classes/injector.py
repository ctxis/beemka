class Injector:
    def __init__(self, utils):
        self.utils = utils

    def inject(self, asar_file, asar_working_path, module, module_data, output_file, worker_class):
        # Extract.
        if not self.utils.extract_asar(asar_file, asar_working_path):
            return False

        worker_data = {
            'asar_working_path': asar_working_path,
            'module': module,
            'module_data': module_data
        }

        # Process.
        if worker_class.run(worker_data) is False:
            return False

        # Compress.
        self.utils.compress_asar(asar_working_path, output_file)

        # Cleanup.
        self.utils.remove_directory(asar_working_path)

        return True