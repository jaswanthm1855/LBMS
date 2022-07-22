class UserNotAuthorizedException(Exception):
    pass


class InvalidBookIdException(Exception):
    pass


class BookNameAlreadyExistsException(Exception):
    pass


class InvalidMemberIdException(Exception):
    pass


class MemberUserNameAlreadyExistsException(Exception):
    pass


class AvailabilityStatusUpdationIsNotAllowedException(Exception):
    pass


class UserDoesNotBorrowedBookException(Exception):
    pass


class BookIsAlreadyBorrowedException(Exception):
    pass


class UserHasBorrowedBooksException(Exception):
    pass


class BookIsBorrowedException(Exception):
    pass


class InvalidAvailabilityStatusException(Exception):
    pass