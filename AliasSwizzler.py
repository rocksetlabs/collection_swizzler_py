import sys, requests
from BaseStep import BaseStep

class AliasSwizzler(BaseStep):
    def __init__(self, options):
        super().__init__(options)

    def execute(self):
        
        # Construct the payload for create/update alias call
        payload = dict()
        collections = list()
        collections.append(f"{self.option('new_collection_workspace')}.{self.option('new_collection_name')}")
        payload['collections'] = collections

        #Look to see if the alias already exists
        qryResopnse = requests.get(
            f"{self.option('baseURL')}ws/{self.option('target_alias_workspace')}/aliases/{self.option('target_alias_name')}",
            headers = self.option('headers')
        )

        if qryResopnse.status_code == 404:
            # The alias doesn't exist, so create it
            if self.isVerbose :  print(f"Creating new Alias {self.option('target_alias_workspace')}.{self.option('target_alias_name')}")
            payload['name'] = self.option('target_alias_name')
            qryResopnse = requests.post(
                f"{self.option('baseURL')}ws/{self.option('target_alias_workspace')}/aliases",
                json = payload,
                headers = self.option('headers')
            )
            if qryResopnse.status_code != 200:
                sys.exit(f"AliasSwizzler had unexpected error creating a new alias: \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")

            response = {'last_status': 'Successful', 'last_step': 'Swizzle Alias'}
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
            
        response = {'last_status': 'Successful', 'last_step': 'Swizzle Alias'}
        return response