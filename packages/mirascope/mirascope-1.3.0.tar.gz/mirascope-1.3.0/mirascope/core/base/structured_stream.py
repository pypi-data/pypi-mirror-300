"""This module defines the base class for structured streams."""

from collections.abc import (
    AsyncGenerator,
    AsyncIterable,
    Awaitable,
    Callable,
    Generator,
    Iterable,
)
from functools import wraps
from typing import (
    Generic,
    ParamSpec,
    TypeVar,
    cast,
    overload,
)

from pydantic import BaseModel

from ._utils import (
    BaseType,
    GetJsonOutput,
    SetupCall,
    extract_tool_return,
    fn_is_async,
    setup_extract_tool,
)
from .call_params import BaseCallParams
from .call_response import BaseCallResponse
from .call_response_chunk import BaseCallResponseChunk
from .dynamic_config import BaseDynamicConfig
from .stream import BaseStream, stream_factory
from .tool import BaseTool

_BaseCallResponseT = TypeVar("_BaseCallResponseT", bound=BaseCallResponse)
_BaseCallResponseChunkT = TypeVar(
    "_BaseCallResponseChunkT", bound=BaseCallResponseChunk
)
_BaseToolT = TypeVar("_BaseToolT", bound=BaseTool)
_BaseCallParamsT = TypeVar("_BaseCallParamsT", bound=BaseCallParams)
_BaseDynamicConfigT = TypeVar("_BaseDynamicConfigT", bound=BaseDynamicConfig)
_ResponseModelT = TypeVar("_ResponseModelT", bound=BaseModel | BaseType)


class BaseStructuredStream(Generic[_ResponseModelT]):
    """A base class for streaming structured outputs from LLMs."""

    stream: BaseStream
    response_model: type[_ResponseModelT]
    constructed_response_model: _ResponseModelT

    def __init__(
        self,
        *,
        stream: BaseStream,
        response_model: type[_ResponseModelT],
    ) -> None:
        """Initializes an instance of `BaseStructuredStream`."""
        self.stream = stream
        self.response_model = response_model

    def __iter__(self) -> Generator[_ResponseModelT, None, None]:
        """Iterates over the stream and extracts structured outputs."""
        json_output = ""
        for chunk, _ in self.stream:
            json_output += chunk.content
            if json_output and json_output[0] != "{":
                try:
                    json_start = json_output.index("{")
                    json_output = json_output[json_start:]
                except ValueError:
                    json_output = ""
            if chunk.model is not None:
                self.stream.model = chunk.model
            if json_output:
                yield extract_tool_return(self.response_model, json_output, True)
        if json_output:
            json_output = json_output[: json_output.rfind("}") + 1]
        self.constructed_response_model = extract_tool_return(
            self.response_model, json_output, False
        )
        yield self.constructed_response_model

    def __aiter__(self) -> AsyncGenerator[_ResponseModelT, None]:
        """Iterates over the stream and extracts structured outputs."""

        async def generator() -> AsyncGenerator[_ResponseModelT, None]:
            json_output = ""
            async for chunk, _ in self.stream:
                json_output += chunk.content
                if json_output and json_output[0] != "{":
                    try:
                        json_start = json_output.index("{")
                        json_output = json_output[json_start:]
                    except ValueError:
                        json_output = ""
                if chunk.model is not None:
                    self.stream.model = chunk.model
                if json_output:
                    yield extract_tool_return(self.response_model, json_output, True)
            if json_output:
                json_output = json_output[: json_output.rfind("}") + 1]
            self.constructed_response_model = extract_tool_return(
                self.response_model, json_output, False
            )
            yield self.constructed_response_model

        return generator()


_BaseDynamicConfigT = TypeVar("_BaseDynamicConfigT", bound=BaseDynamicConfig)
_BaseClientT = TypeVar("_BaseClientT", bound=object)
_ResponseT = TypeVar("_ResponseT")
_ResponseChunkT = TypeVar("_ResponseChunkT")
_P = ParamSpec("_P")


def structured_stream_factory(  # noqa: ANN201
    *,
    TCallResponse: type[_BaseCallResponseT],
    TCallResponseChunk: type[_BaseCallResponseChunkT],
    TStream: type[BaseStream],
    TToolType: type[_BaseToolT],
    setup_call: SetupCall[
        _BaseClientT,
        _BaseDynamicConfigT,
        _BaseCallParamsT,
        _ResponseT,
        _ResponseChunkT,
        _BaseToolT,
    ],
    get_json_output: GetJsonOutput[_BaseCallResponseChunkT],
):
    class CustomContentChunk(TCallResponseChunk):
        json_output: str

        @property
        def content(self) -> str:
            return self.json_output

    @overload
    def decorator(
        fn: Callable[_P, _BaseDynamicConfigT],
        model: str,
        response_model: type[_ResponseModelT],
        json_mode: bool,
        client: _BaseClientT | None,
        call_params: _BaseCallParamsT,
    ) -> Callable[
        _P,
        Iterable[_ResponseModelT],
    ]: ...

    @overload
    def decorator(
        fn: Callable[_P, Awaitable[_BaseDynamicConfigT]],
        model: str,
        response_model: type[_ResponseModelT],
        json_mode: bool,
        client: _BaseClientT | None,
        call_params: _BaseCallParamsT,
    ) -> Callable[
        _P,
        Awaitable[AsyncIterable[_ResponseModelT]],
    ]: ...

    def decorator(
        fn: Callable[_P, _BaseDynamicConfigT]
        | Callable[_P, Awaitable[_BaseDynamicConfigT]],
        model: str,
        response_model: type[_ResponseModelT],
        json_mode: bool,
        client: _BaseClientT | None,
        call_params: _BaseCallParamsT,
    ) -> Callable[
        _P,
        Iterable[_ResponseModelT] | Awaitable[AsyncIterable[_ResponseModelT]],
    ]:
        def handle_chunk(
            chunk: _ResponseChunkT,
        ) -> tuple[_BaseCallResponseChunkT, None]:
            call_response_chunk = TCallResponseChunk(chunk=chunk)
            json_output = get_json_output(call_response_chunk, json_mode)

            call_response_chunk = cast(
                _BaseCallResponseChunkT,
                CustomContentChunk(chunk=chunk, json_output=json_output),  # pyright: ignore [reportAbstractUsage]
            )
            return call_response_chunk, None

        def handle_stream(
            stream: Generator[_ResponseChunkT, None, None],
            tool_types: list[type[_BaseToolT]] | None,
        ) -> Generator[tuple[_BaseCallResponseChunkT, None], None, None]:
            for chunk in stream:
                yield handle_chunk(chunk)

        async def handle_stream_async(
            stream: AsyncGenerator[_ResponseChunkT, None],
            tool_types: list[type[_BaseToolT]] | None,
        ) -> AsyncGenerator[tuple[_BaseCallResponseChunkT, None], None]:
            async for chunk in stream:
                yield handle_chunk(chunk)

        stream_decorator = stream_factory(
            TCallResponse=TCallResponse,
            TStream=TStream,
            setup_call=setup_call,
            handle_stream=handle_stream,
            handle_stream_async=handle_stream_async,
        )

        tool = setup_extract_tool(response_model, TToolType)
        stream_decorator_kwargs = {
            "model": model,
            "tools": [tool],
            "json_mode": json_mode,
            "client": client,
            "call_params": call_params,
        }
        fn._model = model  # pyright: ignore [reportFunctionMemberAccess]
        if fn_is_async(fn):

            @wraps(fn)
            async def inner_async(
                *args: _P.args, **kwargs: _P.kwargs
            ) -> AsyncIterable[_ResponseModelT]:
                return BaseStructuredStream[_ResponseModelT](
                    stream=await stream_decorator(fn=fn, **stream_decorator_kwargs)(
                        *args, **kwargs
                    ),
                    response_model=response_model,
                )

            return inner_async
        else:

            @wraps(fn)
            def inner(*args: _P.args, **kwargs: _P.kwargs) -> Iterable[_ResponseModelT]:
                return BaseStructuredStream[_ResponseModelT](
                    stream=stream_decorator(fn=fn, **stream_decorator_kwargs)(
                        *args, **kwargs
                    ),
                    response_model=response_model,
                )

            return inner

    return decorator
