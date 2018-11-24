""" Class that validates and parses queries """

class InputParser():

    def __init__(self):
        self.logger = self.__log_setup()

    def __log_setup(self):
        return None

    def validate_input(self, input):
        """ Validates user input
            Returns true if valid.
            Returns false otherwise
        """
        return False

    def parse_input(self, input):
        """ Parses the user input and returns a
            dictionary of the requested searches.
        """
        return None
