class SvError(Exception):
    def __init__(self, message, ex: Exception | None):
        self.message = message
        self.ex = ex
        super().__init__(self.message)

    def __str__(self):
        return self.message + " " + str(self.ex) if self.ex is not None else self.message