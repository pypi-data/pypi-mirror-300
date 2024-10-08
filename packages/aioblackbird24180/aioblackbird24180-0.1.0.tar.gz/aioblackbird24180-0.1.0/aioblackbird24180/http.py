"""Custom HTTP implementation for the Blackbird API."""

# The blackbird 24180 HTTP server responds with malformed HTTP responses
# that are not compliant with the HTTP standard. This causes errors in
# both the httpx and aiohttp libraries. This very rudimentary custom
# implementation serves to manually make and parse HTTP requests and
# responses to workaround this.

import asyncio

BASE_HTTP_REQUEST = """{method} {path} HTTP/1.1
Host: {host}
Accept: */*
Content-Length: {content_length}

{body}"""


class HTTPExceptionError(Exception):
    """Raised when the HTTP request fails."""

    def __init__(self, status: int) -> None:
        """Initialize the exception."""
        super().__init__(f"HTTP request failed with status code {status}")


def __process_response(response: bytes) -> tuple[int, str]:
    """Return status code and strip out the HTTP headers from the response."""
    status_code = int(response.split(b"\r\n")[0].split(b" ")[1].decode("utf-8"))
    response_data = response.split(b"\n\n")[1].decode("utf-8")
    return status_code, response_data


def __generate_request(method: str, path: str, host: str, body: str) -> bytes:
    """Generate an HTTP request."""
    return BASE_HTTP_REQUEST.format(
        method=method,
        path=path,
        host=host,
        content_length=len(body),
        body=body,
    ).encode()


async def post_request(host: str, port: int, path: str, data: str) -> str:
    """Make a POST request to the HTTP server."""
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(
        __generate_request(
            method="POST",
            path=path,
            host=host,
            body=data,
        )
    )
    await writer.drain()
    response = await reader.read()
    writer.close()
    await writer.wait_closed()
    status, decoded_response = __process_response(response)
    if status != 200:
        raise HTTPExceptionError(status)
    return decoded_response
