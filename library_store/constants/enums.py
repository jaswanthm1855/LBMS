import enum


class UserRoleEnum(enum.Enum):
    librarian = "LIBRARIAN"
    member = "MEMBER"

    @classmethod
    def choices(cls):
        return tuple(
            (choice.value, choice.value)
            for choice in cls
        )


class BookAvailabilityStatusEnum(enum.Enum):
    available = "AVAILABLE"
    borrowed = "BORROWED"
    not_available = "NOT_AVAILABLE"

    @classmethod
    def choices(cls):
        return tuple(
            (choice.value, choice.value)
            for choice in cls
        )
