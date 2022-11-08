import sys, os, argparse, yaml, requests
from uuid import uuid4
from dotenv import load_dotenv
from CollectionCreator import CollectionCreator
from CollectionDeletor import CollectionDeletor
from ReadyWaiter import ReadyWaiter
from AliasSwizzler import AliasSwizzler

class Launcher():
    def __init__(self, options):
        self.options_dict = options
        self.pendingAggregationUpdates = dict()
     
    def option(self, key):
        if key in self.options_dict:
            return self.options_dict[key]
        else:
            sys.exit(f"Request for unavailable option: {key}") 
 
    def isVerbose(self):
        return self.option('verbose')


def default_options():
    # Return a set of the default options. These can be overriden from the config file and the command line
    options = {}
    options['api_server'] = 'api.rs2.usw2.rockset.com'
 
    return options

def load_config(default_options, cli_options):

    # Get the test configuration file
    with open(cli_options['config_file']) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(f"Could not process yaml config file {cli_options['config_file']}")

    # Merge the options with the correct precedence
    all_options = {}
    all_options.update(default_options)
    if 'options' in config:
        all_options.update(config['options'])
    all_options.update(cli_options) 


        # Get the API KEY(s)
    try:
        load_dotenv()
        apiKey = os.getenv('ROCKSET_APIKEY')
        all_options['api_key'] = apiKey
    except KeyError as e:
        print(e)
        # no need to do anything here now, API key may come from UI or CLI
        pass
        #exit("Did not find ROCKSET_APIKEY defined in .env or unix environment")

    # Ensure the api server as written in the config file doesn't inclue the protocol
    api_server = all_options['api_server']
    # Strip the protocl from the API server if it includes one
    if api_server[0:8] == 'https://':
        replacement = api_server[8:]
        all_options['api_server'] = replacement
    if api_server[0:7] == 'http://':
        replacement = api_server[7:]
        all_options['api_server'] = replacement

    all_options['baseURL'] = 'https://' + api_server + '/v1/orgs/self/'

    headers = {}
    headers['Authorization'] = 'ApiKey ' + all_options['api_key']
    headers['Content-Type'] = 'application/json' 
    all_options['headers'] = headers

    return all_options

def parse_args():
    parser = argparse.ArgumentParser(description='Rockset Script Step Launcher')
    parser.add_argument('-v', '--verbose', help='print information to the screen', action="store_true")
    # parser.add_argument('--nolog', help='suppresses output log', action="store_true")
    parser.add_argument('-c', '--config', help='yaml configuration file with test parameters', default='./resources/config.yaml')
    # parser.add_argument('-o', '--output_dir', help='directory where output is writen', default='./history')

    args = parser.parse_args()
    options = {}
    options['config_file'] = args.config
    options['verbose'] = args.verbose
    
    # options['verbose'] = True # TODO Remove after dev
    
    # options['output_dir'] = args.output_dir
    # options['log_output'] = not args.nolog
    return options

if __name__ == "__main__":
    # Get options from defaults, config file and cli. Merge options with preference of cli, then config file

    # Collect all options. The trick is that CLI options should override config and default options, but we
    # need to get the CLI options first because they may point to a specific config file
    cli_options = parse_args()
    default_options = default_options()
    all_options = load_config(default_options, cli_options)
    result = CollectionCreator(all_options).execute()
    all_options.update(result)
    result = ReadyWaiter(all_options).execute()
    all_options.update(result)
    result = AliasSwizzler(all_options).execute()
    all_options.update(result)
    if 'old_collection_name' in all_options:
        result = CollectionDeletor(all_options).execute()
        all_options.update(result)

