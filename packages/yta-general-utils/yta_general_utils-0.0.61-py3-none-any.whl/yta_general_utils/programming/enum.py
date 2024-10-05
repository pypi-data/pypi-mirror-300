from yta_general_utils.programming.parameter_validator import ParameterValidator
from enum import Enum


class YTAEnum(Enum):
    @classmethod
    def is_valid(cls, value):
        """
        This method returns True if the provided 'value' is a valid
        value for the also provided Enum class 'cls', or False if
        not.
        """
        return is_valid(value, cls)

    @classmethod
    def is_name_or_value(cls, name_or_value):
        """
        This method validates if the provided 'name_or_value' is a
        name or a value of some of this YTAEnum items, raising an 
        exception if not.

        This method will return the YTAEnum item (containing .name
        and .value) if it is valid.
        """
        return is_name_or_value(name_or_value, cls)
    
    @classmethod
    def get_all(cls):
        """
        This method returns all the existing items in this 'cls' Enum
        class.
        """
        return get_all(cls)
    
    @classmethod
    def get_all_names(cls):
        """
        This method returns all the names of the existing items in
        this 'cls' Enum class.
        """
        return get_all_names(cls)

    @classmethod
    def get_all_values(cls):
        """
        This method returns all the values of the existing items in 
        this 'cls' Enum class.
        """
        return get_all_values(cls)
    
    @classmethod
    def get_all_values_as_str(cls):
        """
        This method returns all the values of the existing items as
        strings separated by commas. This is useful to show the 
        accepted values of an Enum.
        """
        return get_values_as_str(cls.get_all())

def is_enum(cls: Enum):
    """
    This method returns True if the provided 'cls' parameter is
    an enum class or subclass.
    """
    return isinstance(cls, Enum) or issubclass(cls, (Enum, YTAEnum))

def is_valid(value: any, enum: Enum):
    """
    This method returns True if the provided 'value' is a valid value for
    the also provided 'enum' Enum object, or False if not.
    """
    if not value:
        raise Exception('No "value" provided.')
    
    if not issubclass(enum, Enum):
        raise Exception('The "enum" parameter is not an Enum.')

    try:
        enum(value)
        return True
    except Exception:
        return False
    
def is_name_or_value(value: any, enum: YTAEnum):
    """
    This method validates if the provided 'value' is a name
    or a value of the also provided 'enum' YTAEnum, raising
    an Exception if not.

    This method returns the enum item (containing .name and
    .value) if it is valid.
    """
    ParameterValidator.validate_mandatory_parameter('value', value)
    ParameterValidator.validate_mandatory_parameter('enum', enum)
    ParameterValidator.validate_is_enum(value)

    if value in enum.get_all_names():
        return enum[value]
    elif value in enum.get_all_values():
        return enum(value)
    
    raise Exception(f'The provided Enum value "{value}" is not a valid {enum.__class__.__name__} enum name or value.')
    
def get_all(enum: Enum):
    """
    This method returns all the items defined in a Enum subtype that
    is provided as the 'enum' parameter.
    """
    if not enum:
        raise Exception('No "enum" provided.')
    
    if not isinstance(enum, Enum) and not issubclass(enum, Enum):
        raise Exception('The "enum" parameter provided is not an Enum.')
    
    return [item for item in enum]

def get_all_names(cls):
    """
    Returns a list containing all the registered enum names.
    """
    return [item.name for item in get_all(cls)]

def get_all_values(cls):
    """
    Returns a list containing all the registered enum values.
    """
    return [item.value for item in get_all(cls)]

def get_names(enums: list[Enum]):
    """
    Returns a list containing all the names of the provided
    'enums' Enum elements.
    """
    if any(not is_enum(enum) for enum in enums):
        raise TypeError('At least one of the given "enums" is not an Enum class or subclass.')    
    
    return [item.name for item in enums]

def get_values(enums: list[Enum]):
    """
    Returns a list containing all the values of the provided
    'enums' Enum elements.
    """
    if any(not is_enum(enum) for enum in enums):
        raise TypeError('At least one of the given "enums" is not an Enum class or subclass.')    
     
    return [item.value for item in enums]

def get_values_as_str(enums: Enum):
    """
    Returns a string containing the provided 'enums' values separated
    by commas.
    """
    if any(not is_enum(enum) for enum in enums):
        raise TypeError('At least one of the given "enums" is not an Enum class or subclass.')    
     
    return ', '.join(get_values(enums))