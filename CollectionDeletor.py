import sys, requests
from BaseStep import BaseStep

class CollectionDeletor(BaseStep):
    def __init__(self, options):
        super().__init__(options)

    def execute(self):
        if self.isVerbose() :  print(f"Deleting Collection {self.option('old_collection_workspace')}.{self.option('old_collection_name')}")

        qryResopnse = requests.delete(
            f"{self.option('baseURL')}ws/{self.option('old_collection_workspace')}/collections/{self.option('old_collection_name')}",
                 headers = self.option('headers')
        )


        if qryResopnse.status_code != 200:
           sys.exit(f"Collection Deleter had unexpected error deleting {self.option('old_collection_workspace')}.{self.option('old_collection_name')}: \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")

        response = {'last_status': 'Successful', 'last_step': 'Delete Old Collection'}
        return response