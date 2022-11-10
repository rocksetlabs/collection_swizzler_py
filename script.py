import sys, os, argparse, yaml, requests
from uuid import uuid4
from dotenv import load_dotenv


class Script():

    def __init__(self):
        self.options = {}

    def getOptions(self):
        return self.options

    def default_options(self):
        # Return a set of the default options. These can be overriden from the config file and the command line
        def_options = {}
        def_options['api_server'] = 'api.rs2.usw2.rockset.com'
    
        return def_options

    def load_config(self, default_options, cli_options):

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

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Rockset Sequenctial Script')
        parser.add_argument('-v', '--verbose', help='print information to the screen', action="store_true")
        # parser.add_argument('--nolog', help='suppresses output log', action="store_true")
        parser.add_argument('-c', '--config', help='yaml configuration file with test parameters', default='./resources/config.yaml')
        # parser.add_argument('-o', '--output_dir', help='directory where output is writen', default='./history')

        args = parser.parse_args()
        arg_options = {}
        arg_options['config_file'] = args.config
        arg_options['verbose'] = args.verbose
        
        # arg_options['verbose'] = True # TODO Remove after dev

        return arg_options

    def loadOptions(self):
        cli_options = self.parse_args()
        default_options = self.default_options()
        all_options = self.load_config(default_options, cli_options)
        self.options.update(all_options)



 

