import sys, requests, time
from BaseStep import BaseStep

class ReadyWaiter(BaseStep):
    def __init__(self, options):
        super().__init__(options)

    def execute(self):
        #Loop until the collection is in a READY state
        status = 'REQUESTED'
        for attempt in range(1, self.option('collection_wait_time_sec') // self.option('collection_wait_poll_sec') + 1 ):
            if self.isVerbose() : print(f"Attempt {attempt} waiting for READY state for collection {self.option('new_collection_workspace')}.{self.option('new_collection_name')}. Current status: {status}")
            qryResopnse = requests.get(
                    f"{self.option('baseURL')}ws/{self.option('new_collection_workspace')}/collections/{self.option('new_collection_name')}",
                    headers = self.option('headers')
                )

            if qryResopnse.status_code != 200:
                sys.exit(f"ReadyWaiter had unexpected error waiting for {self.option('new_collection_workspace')}/collections/{self.option('new_collection_name')} \n\t {qryResopnse.reason} \n\t {qryResopnse.text}")

            response_data = qryResopnse.json()
            data = response_data['data']
            status = data['status']

            if status == 'READY' : break
            time.sleep(self.option('collection_wait_poll_sec'))

        if status != 'READY':
                sys.exit(f"ReadyWaiter timed out waiting for READY status on {self.option('new_collection_workspace')}.{self.option('new_collection_name')}")

        response = {'last_status': 'Successful', 'last_step': 'Wait for Collection Ready'}
        return response