from rest_framework import status


class CustomBaseExecption(Exception):
    is_custom_execption = True


class NotFoundError(CustomBaseExecption):
    def __init__(self, msg="Data Not Found. Please Check ID", *args, **kwargs):
        self.status = status.HTTP_400_BAD_REQUEST
        super().__init__(msg, *args, **kwargs)


class NotFoundUserError(CustomBaseExecption):
    def __init__(
        self, msg="User Not Found. Please Check ID or Password", *args, **kwargs
    ):
        self.status = status.HTTP_400_BAD_REQUEST
        super().__init__(msg, *args, **kwargs)


class NotAuthorizedError(CustomBaseExecption):
    def __init__(self, msg="Login Required", *args, **kwargs):
        self.status = status.HTTP_403_FORBIDDEN
        super().__init__(msg, *args, **kwargs)


class TokenExpiredError(CustomBaseExecption):
    def __init__(self, msg="Login time expired. Please login again", *args, **kwargs):
        self.status = status.HTTP_403_FORBIDDEN
        super().__init__(msg, *args, **kwargs)


class NoPermissionError(CustomBaseExecption):
    def __init__(self, msg="You are not granted for this request", *args, **kwargs):
        self.status = status.HTTP_403_FORBIDDEN
        super().__init__(msg, *args, **kwargs)
