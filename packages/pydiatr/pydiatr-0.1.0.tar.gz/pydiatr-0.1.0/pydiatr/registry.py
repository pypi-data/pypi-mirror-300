"""
from pydiatr.handler import AbstractHandler, AbstractRequest, AbstractResponse
from pydiatr.registry import Registry

registry = Registry()

# Example subclass of AbstractRequest
class CreateUserRequest(AbstractRequest):
    username: str
    email: str

# Example subclass of AbstractResponse
class CreateUserResponse(AbstractResponse):
    success: bool

# Example handler subclass
@registry.decorate_handler
class CreateUserHandler(AbstractHandler[CreateUserRequest, CreateUserResponse]):

    async def handle(self, request: CreateUserRequest) -> CreateUserResponse:
        print(f"Creating user: {request.username} with email: {request.email}")
        return CreateUserResponse(success=True)
"""
from typing import List, Optional, Type
from pydiatr.handler import AbstractHandler, THandler, TRequest, TResponse


class RegistryLookupError(ValueError):
    pass


class Registry:

    def __init__(self, handlers: List[AbstractHandler[TRequest, TResponse]] = []):
        self.handlers = {handler.get_request_type(): handler for handler in handlers}

    def get_handler(self, request_type: Type[TRequest]) -> Optional[AbstractHandler[TRequest, TResponse]]:
        return self.handlers.get(request_type)
    
    def register_handler(self, handler: THandler, *args, **kwargs):
        self.handlers[handler.get_request_type()] = handler(*args, **kwargs)

    def decorate_handler(self, handler: THandler):
        self.register_handler(handler)
        return handler
    
    async def dispatch(self, request: TRequest, *args, **kwargs) -> TResponse:
        handler = self.get_handler(type(request))
        if not handler:
            raise RegistryLookupError(f"No handler found for request: {request}")
        response = await handler.handle(request, *args, **kwargs)
        return response
