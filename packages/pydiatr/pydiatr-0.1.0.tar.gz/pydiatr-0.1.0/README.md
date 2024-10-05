# PydiatR
The python MediatR.

## Example Usage
```python
from pydiatr.handler import AbstractHandler, AbstractRequest, AbstractResponse
from pydiatr.registry import Registry

registry = Registry()

class CreateUserRequest(AbstractRequest):
    username: str
    email: str

class CreateUserResponse(AbstractResponse):
    success: bool

@registry.decorate_handler
class CreateUserHandler(AbstractHandler[CreateUserRequest, CreateUserResponse]):

    async def handle(self, request: CreateUserRequest) -> CreateUserResponse:
        print(f"Creating user: {request.username} with email: {request.email}")
        return CreateUserResponse(success=True)

response = await registry.dispatch(CreateUserRequest)
```
# TODO:
* Abstract/DRY CI/CD
* Auto version bumping in CI/CD based on commit message using `poetry version <option>`
* Tests
* Test coverage and coverage comment on PR
* Coverage badge
* build badge
* license badge
* pypi badge
* README
* FastAPI example
* FastAPI cookiecutter?