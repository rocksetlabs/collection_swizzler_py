class BaseStep:
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