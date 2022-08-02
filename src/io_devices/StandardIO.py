from sys import stdin, stdout

from .IODevice import IODevice
from .io_exceptions import IOReadOnEOF, IncompleteOutput


bytes_encoding = 'raw_unicode_escape'


class StandardIO(IODevice):
    """
    read from stdin, write to stdout
    """
    def __init__(self, output_verbose: bool):
        """
        @param output_verbose: if true print program's output
        """
        self.output_verbose = output_verbose
        self._output = b''

        self.current_input_byte = 0
        self.bits_to_read_in_input_byte = 0

        self.current_output_byte = 0
        self.bits_to_write_in_output_byte = 0

    def read_bit(self) -> bool:
        if 0 == self.bits_to_read_in_input_byte:
            read_bytes = stdin.read(1).encode(encoding=bytes_encoding)
            if 0 == len(read_bytes):
                raise IOReadOnEOF("Read an empty input on standard IO (EOF)")

            self.current_input_byte = read_bytes[0]
            self.bits_to_read_in_input_byte = 8

        bit = (self.current_input_byte & 1) == 1
        self.current_input_byte >>= 1
        self.bits_to_read_in_input_byte -= 1
        return bit

    def write_bit(self, bit: bool) -> None:
        self.current_output_byte |= bit << self.bits_to_write_in_output_byte
        self.bits_to_write_in_output_byte += 1

        if 8 == self.bits_to_write_in_output_byte:
            curr_output: bytes = self.current_output_byte.to_bytes(1, 'little')
            if self.output_verbose:
                stdout.write(curr_output.decode(encoding=bytes_encoding))
                stdout.flush()
            self._output += curr_output
            self.current_output_byte = 0
            self.bits_to_write_in_output_byte = 0

    def get_output(self) -> bytes:
        if 0 != self.bits_to_write_in_output_byte:
            raise IncompleteOutput("tries to get output when an unaligned number of bits was outputted "
                                   "(doesn't divide 8)")

        return self._output
