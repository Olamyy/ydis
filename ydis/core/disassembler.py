import dis
from typing import Generator, Any

class Disassembler:
    """Core disassembler class wrapping dis.get_instructions."""

    def get_instructions(self, x: Any) -> Generator[dis.Instruction, None, None]:
        """
        Get instructions for a given object (function, method, code object, etc.).
        
        Args:
            x: The object to disassemble. Can be a function, method, class, code object, or string of source code.
            
        Yields:
            dis.Instruction: The disassembled instructions.
        """
        return dis.get_instructions(x)
