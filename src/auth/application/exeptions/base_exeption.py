class BaseApplicationException(Exception):
    default_message: str = "Application error"

    def __init__(self, message: str = None, *args):  # type: ignore[assignment]
        self.message = message or self.default_message
        super().__init__(self.message, *args)
