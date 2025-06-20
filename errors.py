class GlpiAuthError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return "GLPI AUTH ERROR, {}".format(self.message)
        else:
            return "GLPI AUTH ERROR - NO ARGS"


class GlpiSessionError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return "GLPI API SESSION IS NOT ACTIVE, {}".format(self.message)
        else:
            return "GLPI API SESSION IS NOT ACTIVE - NO ARGS"