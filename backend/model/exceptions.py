class FIELD_REGEX_FAILED(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FILED_EMPTY(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DUPLICATE_ENTITY_EXCEPTION(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ENTITY_NOT_FOUND(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NOT_ALLOWED(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SYNTAX_ERROR(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class INTERNAL_SERVER_ERROR(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class INTERNAL_DATABASE_ERROR(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
