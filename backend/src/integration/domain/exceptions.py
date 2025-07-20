class IntegrationRequestException(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f'Request error: {self.message}'


class IntegrationInvalidResponseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f'Invalid response from API received'


class IntegrationUnauthorizedExeception(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self):
        return f'Unauthorized API request'
