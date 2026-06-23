
class OlympiadException(Exception):
    pass

class UserAlreadyExists(OlympiadException):
    pass

class UserNotExist(OlympiadException):
    pass

class InvalidCredentials(OlympiadException):
    pass

class InvalidToken(OlympiadException):
    pass

class TokenNotFound(OlympiadException):
    pass

class NotAuthorized(OlympiadException):
    pass


class InvalidDateConfiguration(OlympiadException):
   pass

class OlympiadNotExists(OlympiadException):
    pass

class OlympiadAlreadyInactive(OlympiadException):
    pass

class ApplicationAlreadyExists(OlympiadException):
    pass

class OlympiadInactive(OlympiadException):
    pass

class RegistrationClosed(OlympiadException):
    pass

class RegistrationNotStarted(OlympiadException):
    pass

class ApplicationNotExists(OlympiadException):
    pass

class ProfileNotCompleted(OlympiadException):
    pass

class ProfileAlreadyExists(OlympiadException):
    pass

class ProfileDataAlreadyExists(OlympiadException):
    pass

class ProfileNotExists(OlympiadException):
    pass

class ApplicationAlreadyReviewed(OlympiadException):
    pass

class OlympiadAlreadyActive(OlympiadException):
    pass

class TokenExpired(OlympiadException):
    pass

class OTPRequired(OlympiadException):
    pass

class InvalidOTP(OlympiadException):
    pass

class InvalidPassword(OlympiadException):
    pass

class UserAlreadyHasRole(OlympiadException):
    pass

class SuperAdminModificationNotAllowed(OlympiadException):
    pass

class UserStatusConflict(OlympiadException):
    pass

class InvalidSortField(OlympiadException):
    pass

class InvalidSortOrder(OlympiadException):
    pass