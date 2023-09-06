from pprint import pformat

class CompareException(Exception):
    def __init(self, context):
        super().__init__("MESSAGE HERE: " + pformat(context))
        self.context = context

