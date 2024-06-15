from uuid import UUID

from litestar import Litestar, get
from litestar.openapi import OpenAPIConfig, ResponseSpec
from litestar.openapi.plugins import StoplightRenderPlugin
from litestar.openapi.spec import Example
from pydantic import BaseModel


class TestResponse(BaseModel):
    message: str
    code: int
    uuid: UUID

@get("/hello/", tags=["Hello World"], responses={
    305: ResponseSpec(
        data_container=TestResponse,
        examples=[
            Example(
                summary="Example 1",
                description="An example response",
                value={"message": "Hello, World!"}
            )
        ],
    )
})
async def hello_world(
        name: str
) -> str:
    return f"Hello, {name}!"


app = Litestar(
    debug=True,
    route_handlers=[
        hello_world,
    ],
    openapi_config=OpenAPIConfig(
        title="Litestar Example",
        description="Example of Litestar with Scalar OpenAPI docs",
        version="0.0.1",
        render_plugins=[StoplightRenderPlugin(
            path="/elements",
        )],
        path="/docs",
    ),
)
