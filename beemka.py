__version__ = '0.1'

import argparse, os, tempfile, pprint, time, shutil, sys, base64, jsmin
from classes.utils import BaseUtils
from classes.modules import ModuleManager
from classes.injector import Injector

parser = argparse.ArgumentParser(prog="Beemka Electron Exploitation")

parser.add_argument("-v", "--version", action="version", version="%(prog)s " + __version__)
parser.add_argument("-l", "--list-modules", dest="list_modules", action="store_true", default=False, help="List all available modules.")
parser.add_argument("-i", "--inject", dest="inject", action="store_true", default=False, help="Inject code into Electron.")
parser.add_argument("-f", "--asar", dest="asar_file", default="", help="Path to electron.asar file.")
parser.add_argument("-p", "--asar-working-path", dest="asar_working_path", default="", help="Temporary working path to use for extracting asar archives.")
parser.add_argument("-o", "--output", dest="output_file", default="", help="Path to the file that will be generated.")
parser.add_argument("-m", "--module", dest="module", default="", help="Module to inject. Use --list-modules to list available modules.")
parser.add_argument("-u", "--unpack", dest="unpack", action="store_true", default=False, help="Unpack asar file.")
parser.add_argument("-z", "--pack", dest="pack", action="store_true", default=False, help="Pack asar file.")
args = parser.parse_args()

if not len(sys.argv) > 1:
    parser.print_help()
    exit(1)

current_path = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_path, 'templates')

utils = BaseUtils()
module_manager = ModuleManager(os.path.join(current_path, 'modules'), utils)
injector = Injector(utils)

modules = module_manager.get_loaded_modules()

if args.list_modules:
    if len(modules) == 0:
        print("No modules found.")
    else:
        print("Available modules\n")
        for name, module in modules.items():
            print("[ " + name + " ]\t" + module['module_description'])

    exit(0)
elif args.pack or args.unpack:
    if args.pack:
        asar_directory = args.asar_working_path
        output_file = args.output_file

        if not os.path.isdir(asar_directory):
            print("Directory does not exist: " + asar_directory)
            exit(1)
        elif os.path.isfile(output_file):
            response = utils.prompt_for("Output file already exists (" + output_file + ") Overwrite?", valid_responses=["Y", "N"], default_response="N")
            if response.lower() == 'n':
                exit(1)

        if not utils.compress_asar(asar_directory, output_file):
            print("Could not pack asar file.")
            exit(1)

        print("asar file successfully packed to: " + output_file)
        exit(0)

    elif args.unpack:
        asar_file = args.asar_file
        output_dir = args.output_file

        if not asar_file or not os.path.isfile(asar_file):
            print("--asar file not specified or does not exist")
            exit(1)
        elif os.path.isdir(output_dir):
            response = utils.prompt_for("Output directory already exists (" + output_dir + ") Overwrite?", valid_responses=["Y", "N"], default_response="N")
            if response.lower() == 'n':
                exit(1)

        if not utils.extract_asar(asar_file, output_dir):
            print("Could not extract asar file.")
            exit(1)

        print("asar file successfully extracted to: " + output_dir)
        exit(0)
elif args.inject:
    if not args.asar_file or not os.path.isfile(args.asar_file):
        print("--asar file not specified or does not exist")
        exit(1)

    asar_file = args.asar_file

    if args.asar_working_path == '':
        asar_working_path = tempfile.mkdtemp(prefix='beemka_')
    else:
        asar_working_path = args.asar_working_path

        if os.path.isdir(asar_working_path):
            response = utils.prompt_for("Working path already exists (" + asar_working_path + ") Overwrite?", valid_responses=["Y", "N"], default_response="N")
            if response.lower() == 'n':
                exit(1)

    if args.output_file == '':
        output_file = asar_file + '_' + str(time.time()) + '.asar'
    else:
        output_file = args.output_file

        if os.path.isfile(output_file):
            response = utils.prompt_for("Output file already exists (" + output_file + ") Overwrite?", valid_responses=["Y", "N"], default_response="N")
            if response.lower() == 'n':
                exit(1)

    if args.module == '':
        print("Module not specified.")
        exit(1)
    elif args.module not in modules:
        print("Invalid module: " + args.module)
        exit(1)

    module = modules[args.module]
    module_data = module_manager.collect_data(module)

    mod = __import__('modules.' + module['folder'] + '.worker', fromlist=['worker'])
    worker_class = getattr(mod, 'worker')
    worker = worker_class(utils)

    if not injector.inject(asar_file, asar_working_path, module, module_data, output_file, worker):
        print("Could not inject payload.")
        exit(1)

    print("Payload injected. Output file is: " + output_file)
    exit(0)