"""Core Interface."""

from collections import defaultdict
from contextlib import suppress

from aiohttp import ClientSession
from aiohttp.http_exceptions import BadHttpMessage

from .util import parse_response


class MatrixState:
    """
    Store the state of the matrix.

    An input can be connected to multiple outputs. An output can be connected to one input.
    """

    def __init__(self) -> None:
        self._matrix_input: dict[int, list[int]] = defaultdict(list)
        self._matrix_output: dict[int, int] = {}

    def set_output_input(self, output: int, input: int) -> None:
        """
        Set an output to a specific input.

        Parameters:
            `output`: the output number to set as int.
            `input`: the input number to set as int.
        """
        self._matrix_output[output] = input
        self._matrix_input[input].append(output)

    def get_input(self, input: int) -> list[int]:
        """
        Get the outputs connected to an input.

        Parameters:
            `input`: the input number to get as int.
        """
        return self._matrix_input[input]

    def get_output(self, output: int) -> int:
        """
        Get the input connected to an output.

        Parameters:
            `output`: the output number to get as int.
        """
        return self._matrix_output[output]


class Blackbird24180:
    """Blackbird24180."""

    def __init__(self, host: str, session: ClientSession | None = None) -> None:
        """
        Initialize the Blackbird24180 instance.

        Parameters:
            `host`: the hostname or IP-address of the blackbird matrix as string.
            `session`: Optional ClientSession instance to use for requests.
        """
        self.host = host
        if not session:
            session = ClientSession()
        self.session = session

    async def __post(self, path: str, data: str) -> str:
        async with self.session.request(
            "post", f"{self.host}/{path}", data=data.encode("utf-8")
        ) as response:
            return await response.text()  # type: ignore[no-any-return]

    async def close(self) -> None:
        """Close the session."""
        await self.session.close()

    async def get_matrix(self) -> MatrixState:
        """Get the current matrix configuration."""
        # It seems like sending any data to this endpoint will work, but it cannot be empty
        # "lcc" is used because the web ui uses this
        response = await self.__post("cgi-bin/MUH44TP_getsetparams.cgi", "lcc")
        parsed_response = parse_response(response)
        state = MatrixState()
        for output in range(1, 9):
            state.set_output_input(output, int(parsed_response[f"CH{output}Output"]))
        return state

    async def set_output(self, output: int, input: int) -> None:
        """
        Set an input to a specific output.

        Parameters:
            `output`: the output number to modify as an int.
            `input`: the input number to set as int.
        """
        # Expect a BadHttpMessage because the server replies with an invalid http response
        with suppress(BadHttpMessage):
            await self.__post(
                "cgi-bin/MMX32_Keyvalue.cgi", f"{{CMD=OUT{output:02}:{input:02}."
            )
