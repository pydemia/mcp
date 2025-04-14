from typing import Any
from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from mcp import ClientSession, types
from mcp.client.sse import sse_client
from contextlib import asynccontextmanager, AbstractAsyncContextManager


class AsyncMCPSession(AbstractAsyncContextManager):
    def __init__(
        self,
        server_url: str,
        headers: dict[str, Any] | None = None,
        timeout: float = 5.0,
        read_timeout: float = 60 * 5.0,
    ):
        self.server_url = server_url
        self.sse_client = sse_client(
            url=self.server_url,
            headers=headers,
            timeout=timeout,
            sse_read_timeout=read_timeout,
        )
        self.streams = None
        self.sessionmaker = None
        self.session = None

    async def __aenter__(self):
        await super().__aenter__()
        self.streams = await self.sse_client.__aenter__()
        self.sessionmaker = ClientSession(*self.streams)
        self.session = await self.sessionmaker.__aenter__()
        await self.session.initialize()
        return self.session

    async def __aexit__(self, exc_typ, exc_val, exc_tb):
        await self.session.__aexit__(exc_typ, exc_val, exc_tb)
        await self.sse_client.__aexit__(exc_typ, exc_val, exc_tb)
        await super().__aexit__(exc_typ, exc_val, exc_tb)


# class AsyncMCPSession(_AsyncGeneratorContextManager):

#     def __init__(self):
#         self.server_url = "http://localhost:8080/sse"
#         self.sse_client = sse_client(url=self.server_url)
#         # self.session = ClientSession()

#     async def get_async_session(self):

#         async with self.sse_client as streams:
#             async with ClientSession(*streams) as session:

#         # async with AsyncSession(
#         #     bind=self.engine,
#         #     autocommit=False,
#         #     autoflush=True,
#         #     expire_on_commit=False,
#         # ) as session:
#         session: sqlmodel_AsyncSession = self.async_session()
#         try:
#             yield session
#         except HandledException as known_e:
#             session: async_scoped_session
#             await session.rollback()
#             raise known_e
#         except Exception as e:
#             session: async_scoped_session
#             await session.rollback()
#             raise HandledException(ResponseCode.ENTITY_CANNOT_UPDATED, e=e) from e
#         else:
#             await session.commit()
#         finally:
#             await self.session.remove()
#             # await self.engine.dispose()

#     @staticmethod
#     @asynccontextmanager
#     async def async_session_context_manager(async_session: sqlmodel_AsyncSession):
#         try:
#             yield async_session
#         except HandledException as known_e:
#             await async_session.rollback()
#             raise known_e
#         except Exception as e:
#             await async_session.rollback()
#             raise HandledException(ResponseCode.DATABASE_COMMIT_ERROR, e=e) from e
#         else:
#             await async_session.commit()
#         finally:
#             await async_session.remove()


app = FastAPI(title="mcp sse client app")


@app.get("/tools", tags=["tools"])
# async def list_tools(mcp_session: AsyncMCPSession = Depends()):
async def list_tools():
    async with AsyncMCPSession("http://localhost:8080/sse") as session:
        response: types.ListToolsResult = await session.list_tools()
        return JSONResponse(
            content=response.model_dump(),
            status_code=200,
        )
