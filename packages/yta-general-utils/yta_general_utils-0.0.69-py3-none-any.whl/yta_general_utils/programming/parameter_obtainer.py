import inspect


class ParameterObtainer:
    """
    Class to interact with python methods and classes to obtain
    the parameters those method have. This is usefull for dynamic
    functionality that need to fill or check if the required
    parameters are passed or not.
    """
    @staticmethod
    def get_parameters_from_method(method):
        """
        This methods returns the existing parameters in the provided
        'method' that are not 'self' nor 'cls'. These parameters will
        be categorized in 'mandatory' and 'optional'. The 'optional'
        values are those that have None as default value.

        The 'method' parameter must be a real python method to be able
        to inspect it.
        """
        parameters = {
            'mandatory': [],
            'optional': []
        }

        params = inspect.signature(method).parameters.values()
        for parameter in params:
            if parameter.name in ['self', 'cls']:
                continue
            
            if parameter.default is parameter.empty:
                parameters['optional'].append(parameter.name)
            else:
                parameters['mandatory'].append(parameter.name)

        return parameters
