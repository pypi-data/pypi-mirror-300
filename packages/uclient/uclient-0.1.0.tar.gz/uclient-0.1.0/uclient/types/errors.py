import json


class STATUS_CODE:
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    MODEL_NOT_FOUND = 404
    BAD_PARAMS = 422
    API_RATE_LIMIT = 503
    BILL_LIMIT = 429
    INTERNAL_ERROR = 500
    API_TIMEOUT = 423
    API_CONNECTION_ERROR = 424
    MODEL_NOT_STARTED = 501
    BAD_RESPONSE = 502


class APIException(Exception):
    def __init__(self, code: int = 0, msg: str = "", context: dict = {}):
        self.code = code
        self.msg = msg
        self.context = context

    def __str__(self):
        return json.dumps({"code": self.code, "msg": self.msg, "context": self.context})

    __repr__ = __str__


class BadResponseError(APIException):
    """BadResponseError: Exception for bad response error"""

    def __init__(
        self,
        code: int = STATUS_CODE.BAD_RESPONSE,
        msg: str = "Bad Response Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class AuthenticationError(APIException):
    """AuthError: Exception for authentication error"""

    def __init__(
        self,
        code: int = STATUS_CODE.UNAUTHORIZED,
        msg: str = "Authentication Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class ModelNotFoundError(APIException):
    """ModelNotFoundError: Exception for model not found"""

    def __init__(
        self,
        code: int = STATUS_CODE.MODEL_NOT_FOUND,
        msg: str = "Model Not Found",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class ModelLoadError(APIException):
    """ModelLoadError: Exception for model load error"""

    def __init__(
        self,
        code: int = STATUS_CODE.INTERNAL_ERROR,
        msg: str = "Model Load Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class IncorrectAPIKeyError(APIException):
    """IncorrectAPIKeyError: Exception for incorrect API key error"""

    def __init__(
        self,
        code: int = STATUS_CODE.UNAUTHORIZED,
        msg: str = "Incorrect API Key",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class InternalServerError(APIException):
    """InternalServerError: Exception for internal server error"""

    def __init__(
        self,
        code: int = STATUS_CODE.INTERNAL_ERROR,
        msg: str = "Internal Server Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class RateLimitError(APIException):
    """APIRateLimitError: Exception for API rate limit error"""

    def __init__(
        self,
        code: int = STATUS_CODE.API_RATE_LIMIT,
        msg: str = "API Rate Limit Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class BillLimitError(APIException):
    """BillLimitError: Exception for bill limit error"""

    def __init__(
        self,
        code: int = STATUS_CODE.BILL_LIMIT,
        msg: str = "Bill Limit Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class BadParamsError(APIException):
    """BadParamsError: Exception for bad parameters error"""

    def __init__(
        self,
        code: int = STATUS_CODE.BAD_PARAMS,
        msg: str = "Bad Parameters Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class ModelGenerateError(APIException):
    """LocalModelGenerateError: Exception for local model generation error"""

    def __init__(
        self,
        code: int = STATUS_CODE.INTERNAL_ERROR,
        msg: str = "Model Generate Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class APITimeoutError(APIException):
    def __init__(
        self,
        code: int = STATUS_CODE.API_TIMEOUT,
        msg: str = "API Timeout",
        context: dict = {},
    ):
        super().__init__(code, msg, context)


class APIConnectionError(APIException):
    def __init__(
        self,
        code: int = STATUS_CODE.API_CONNECTION_ERROR,
        msg: str = "API Connnection Error",
        context: dict = {},
    ):
        super().__init__(code, msg, context)
