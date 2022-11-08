import json, sys, requests

class CollectionDeletor():
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
        if self.isVerbose :  print(f"Deleting Collection {self.option('old_collection_workspace')}.{self.option('old_collection_name')}")

        qryResopnse = requests.delete(
            f"{self.option('baseURL')}ws/{self.option('old_collection_workspace')}/collections/{self.option('old_collection_name')}",
                 headers = self.option('headers')
        )


        if qryResopnse.status_code != 200:
           sys.exit(f"Collection Deleter had unexpected error deleting {self.option('old_collection_workspace')}.{self.option('old_collection_name')}: \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")

        response = {'status': 'Successful'}
        return response