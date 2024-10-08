class MediacatchError(Exception):
    """
    Base class for all Mediacatch exceptions.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MediacatchAPIError(Exception):
    """
    Raised when the API returns an error status code.
    """

    def __init__(self, status_code, response_json):
        self.status_code = status_code
        self.response_json = response_json
        super().__init__(f'API returned error status code: {status_code}')


class MediacatchTimeoutError(Exception):
    """
    Raised when a timeout occurs during API requests.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MediacatchUploadError(Exception):
    """
    Raised when an error occurs during file upload.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
