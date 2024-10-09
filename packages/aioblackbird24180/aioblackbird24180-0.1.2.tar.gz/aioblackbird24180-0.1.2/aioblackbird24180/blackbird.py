"""Core Interface."""

from collections import defaultdict

from .http import post_request
from .util import parse_response


class MatrixState:
    """
    Store the state of the matrix.

    An input can be connected to multiple outputs. An output can be connected to one
    input.
    """

    def __init__(self) -> None:
        """Initialize the MatrixState instance."""
        self.matrix_input: dict[int, list[int]] = defaultdict(list)
        self.matrix_output: dict[int, int] = {}

    def set_output_input(self, output: int, input: int) -> None:
        """
        Set an output to a specific input.

        Parameters:
            `output`: the output number to set as int.
            `input`: the input number to set as int.
        """
        self.matrix_output[output] = input
        self.matrix_input[input].append(output)

    def get_input(self, input: int) -> list[int]:
        """
        Get the outputs connected to an input.

        Parameters:
            `input`: the input number to get as int.
        """
        return self.matrix_input[input]

    def get_output(self, output: int) -> int:
        """
        Get the input connected to an output.

        Parameters:
            `output`: the output number to get as int.
        """
        return self.matrix_output[output]


class Blackbird24180:
    """Blackbird24180."""

    def __init__(self, host: str, port: int) -> None:
        """
        Initialize the Blackbird24180 instance.

        Parameters:
            `host`: the hostname or IP-address of the blackbird matrix as string.
            `port`: the port of the blackbird matrix as int.
        """
        self.host = host
        self.port = port

    async def __post(self, path: str, data: str) -> str:
        return await post_request(self.host, self.port, path, data)

    async def get_matrix(self) -> MatrixState:
        """Get the current matrix configuration."""
        # It seems like sending any data to this endpoint will work, but it cannot be
        # empty "lcc" is used because the web ui uses this
        response = await self.__post("/cgi-bin/MUH44TP_getsetparams.cgi", "lcc")
        parsed_response = parse_response(response)
        state = MatrixState()
        for output, input in enumerate(parsed_response["Outputbuttom"]):
            # Add 1 to output to skip 0-indexing
            state.set_output_input(output + 1, int(input))
        return state

    async def set_output(self, output: int, input: int) -> None:
        """
        Set an input to a specific output.

        Parameters:
            `output`: the output number to modify as an int.
            `input`: the input number to set as int.
        """
        await self.__post(
            "/cgi-bin/MMX32_Keyvalue.cgi", f"{{CMD=OUT{output:02}:{input:02}."
        )
