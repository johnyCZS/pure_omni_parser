"""Global custom exceptions"""


class OmniParserError(Exception):
    """Base exception for OmniParser"""
    pass


class InvalidAPIKeyError(OmniParserError):
    """Raised when API key is invalid or missing"""
    pass


class InvalidImageError(OmniParserError):
    """Raised when image data is invalid"""
    pass


class ModelLoadError(OmniParserError):
    """Raised when model fails to load"""
    pass


class ParsingError(OmniParserError):
    """Raised when parsing fails"""
    pass