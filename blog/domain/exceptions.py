class InvalidStatusException(Exception):
    pass


class NotFoundException(Exception):
    pass


class UserNotFoundException(NotFoundException):
    pass


class ArticleNotFoundException(NotFoundException):
    pass


class PermissionDeniedException(Exception):
    pass
