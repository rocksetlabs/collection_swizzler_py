from script import Script
from CollectionCreator import CollectionCreator
from CollectionDeletor import CollectionDeletor
from ReadyWaiter import ReadyWaiter
from AliasSwizzler import AliasSwizzler

class BulkLoadAndAlias(Script):
    def __init__(self):
        super().__init__()

    def execute(self):
        run_options = {}
        run_options.update(self.getOptions())
        result = CollectionCreator(run_options).execute()
        run_options.update(result)
        result = ReadyWaiter(run_options).execute()
        run_options.update(result)
        result = AliasSwizzler(run_options).execute()
        run_options.update(result)
        if 'old_collection_name' in run_options:
            result = CollectionDeletor(run_options).execute()
            run_options.update(result)

if __name__ == "__main__":
    script = BulkLoadAndAlias()
    script.loadOptions()
    script.execute()