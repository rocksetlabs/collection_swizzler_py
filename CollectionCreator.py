import json, sys, requests
from BaseStep import BaseStep

class CollectionCreator(BaseStep):
    def __init__(self, options):
        super().__init__(options)

    def execute(self):
        if self.isVerbose() :  print(f"Creating Collection {self.option('new_collection_workspace')}.{self.option('new_collection_name')}")
        payload = dict()
        payload['name'] = self.option('new_collection_name')
        sources = list()
        source = dict()
        source['integration_name'] = self.option('source_integration')
        s3 = dict()
        s3['region'] = self.option('source_s3_region')
        s3['bucket'] = self.option('source_s3_bucket')
        s3['pattern'] = self.option('source_s3_pattern')
        source['s3'] = s3
        sources.append(source)
        payload['sources'] = sources

        if self.hasOption('sqlTransform'):
            payload['field_mapping_query'] = self.option('sqlTransform')

        if self.hasOption('retention_seconds'):
            payload['retention_secs'] = self.option('retention_secs')

        qryResopnse = requests.post(
            f"{self.option('baseURL')}ws/{self.option('new_collection_workspace')}/collections",
            json = payload,
            headers = self.option('headers')
        )


        if qryResopnse.status_code != 200:
           sys.exit(f"Collection Creator had unexpected error creating {self.option('new_collection_workspace')}.{self.option('new_collection_name')}: \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")

        response = {'last_status': 'Successful', 'last_step': 'Create New Collection'}
        return response