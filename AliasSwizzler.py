import json, sys, requests, time

class AliasSwizzler():
    def __init__(self, options):
        self.options_dict = options

    def isVerbose(self):
        return self.option('verbose')

    def option(self, key):
        if key in self.options_dict:
            return self.options_dict[key]
        else:
            raise KeyError(f"Request for unavailable option: {key}") 

    def hasOption(self, key):
        return key in self.options_dict

    def execute(self):
        if self.isVerbose :  print(f"Creating Alias {self.option('target_alias_workspace')}.{self.option('target_alias_name')}")
        
        #Look to see if the alias already exists
        payload = dict()
        collections = list()
        collections.append(f"{self.option('new_collection_workspace')}.{self.option('new_collection_name')}")
        payload['collections'] = collections
        qryResopnse = requests.get(
            f"{self.option('baseURL')}ws/{self.option('target_alias_workspace')}/aliases/{self.option('target_alias_name')}",
            json = payload,
            headers = self.option('headers')
        )

        # Construct the payload for create/update alias call
        if self.isVerbose :  print(f"Creating new Alias {self.option('target_alias_workspace')}.{self.option('target_alias_name')}")
        payload = dict()
        collections = list()
        collections.append(f"{self.option('new_collection_workspace')}.{self.option('new_collection_name')}")
        payload['collections'] = collections

        if qryResopnse.status_code == 404:
            # The alias doesn't exist, so create it
            payload['name'] = self.option('target_alias_name')
            qryResopnse = requests.post(
                f"{self.option('baseURL')}ws/{self.option('target_alias_workspace')}/aliases",
                json = payload,
                headers = self.option('headers')
            )
            if qryResopnse.status_code != 200:
                sys.exit(f"AliasSwizzler had unexpected error creating a new alias: \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")

            response = {'status': 'Successful'}
            return response

        elif qryResopnse.status_code != 200:
            sys.exit(f"AliasSwizzler had unexpected error checking alias existence for {self.option('target_alias_workspace')}.{self.option('target_alias_name')}: \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")

        # Alias exists, so update it
        if self.isVerbose :  print(f"Updating Alias {self.option('target_alias_workspace')}.{self.option('target_alias_name')}")
        qryResopnse = requests.post(
            f"{self.option('baseURL')}ws/{self.option('target_alias_workspace')}/aliases/{self.option('target_alias_name')}",
            json = payload,
            headers = self.option('headers')
        )

        if qryResopnse.status_code != 200:
            sys.exit(f"AliasSwizzler had unexpected error updating alias {self.option('target_alias_workspace')}.{self.option('target_alias_name')}:  \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")
            
        response = {'status': 'Successful'}
        return response