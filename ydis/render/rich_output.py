import dis
from typing import Generator, Iterable

from rich.console import Console
from rich.table import Table
from rich.text import Text

class RichRenderer:
    """Renders disassembled instructions using Rich."""

    def __init__(self, console: Console = None):
        self.console = console or Console()

    def render(self, instructions: Iterable[dis.Instruction]):
        """
        Render instructions as a table.
        """
        table = Table(title="Disassembly", expand=True)
        table.add_column("Line", justify="right", style="cyan", no_wrap=True)
        table.add_column("Offset", justify="right", style="magenta", no_wrap=True)
        table.add_column("Opcode", style="green")
        table.add_column("Argument", style="yellow")
        table.add_column("Arg Value", style="blue")

        previous_line = None

        for instr in instructions:
            line_str = ""
            current_lineno = None

            # 1. Prefer extraction from positions (Python 3.11+)
            if instr.positions and instr.positions.lineno is not None:
                current_lineno = instr.positions.lineno
            
            # 2. Fallback to starts_line (Python < 3.11 or fallback)
            # Ensure we don't treat boolean True as a line number
            elif instr.starts_line is not None and not isinstance(instr.starts_line, bool):
                current_lineno = instr.starts_line

            # 3. Filter out line 0 (often used for internal RESUME ops or module start)
            if current_lineno == 0:
                current_lineno = None

            # 4. Determine if we should print it (only if changed from previous)
            if current_lineno is not None:
                if current_lineno != previous_line:
                    line_str = str(current_lineno)
                    previous_line = current_lineno
            
            # Note: if current_lineno is None, line_str remains ""


            offset_str = str(instr.offset)
            opcode_str = instr.opname
            arg_str = str(instr.arg) if instr.arg is not None else ""
            arg_val_str = str(instr.argval) if instr.argrepr else "" # Use argrepr if available, or argval
            
            # Use argrepr which is pre-formatted by dis
            if instr.argrepr:
                 arg_val_str = instr.argrepr
            elif instr.argval is not instr.arg:
                 # If argval is interesting (different from integer arg)
                 arg_val_str = str(instr.argval)


            table.add_row(line_str, offset_str, opcode_str, arg_str, arg_val_str)

        self.console.print(table)
