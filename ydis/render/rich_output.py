import dis
from typing import Generator, Iterable

from rich.console import Console
from rich.table import Table
from rich.text import Text

class RichRenderer:
    """Renders disassembled instructions using Rich."""

    def __init__(self, console: Console = None):
        self.console = console or Console()

    def render(self, instructions: Iterable[dis.Instruction], title: str = "Disassembly"):
        """
        Render instructions as a table.
        """
        instructions = list(instructions)
        table = Table(title=title, expand=True)
        table.add_column("Line", justify="right", style="cyan", no_wrap=True)
        table.add_column("Offset", justify="right", style="magenta", no_wrap=True)
        table.add_column("Opcode", style="green")
        table.add_column("Argument", style="yellow")
        table.add_column("Arg Value", style="blue")

        previous_line = None

        jump_targets = {}
        target_count = 1
        for instr in instructions:
            if instr.is_jump_target and instr.offset not in jump_targets:
                jump_targets[instr.offset] = f"L{target_count}"
                target_count += 1
                
        nested_code_objects = []

        for i, instr in enumerate(instructions):
            line_str = ""
            current_lineno = None

            if instr.positions and instr.positions.lineno is not None:
                current_lineno = instr.positions.lineno
            
            elif instr.starts_line is not None and not isinstance(instr.starts_line, bool):
                current_lineno = instr.starts_line

            if current_lineno == 0:
                current_lineno = None

            if current_lineno is not None:
                if current_lineno != previous_line:
                    line_str = str(current_lineno)
                    previous_line = current_lineno
            
            row_style = None
            
            offset_str = str(instr.offset)
            if instr.offset in jump_targets:
                label = jump_targets[instr.offset]
                offset_str = f"[bold yellow]{label} >>[/] {offset_str}"
                row_style = "on grey15"

            opcode_str = instr.opname
            arg_str = str(instr.arg) if instr.arg is not None else ""
            arg_val_str = str(instr.argval) if hasattr(instr, 'argrepr') and instr.argrepr else ""
            
            if instr.argrepr:
                 arg_val_str = instr.argrepr
            elif instr.argval is not instr.arg:
                 arg_val_str = str(instr.argval)

            if "JUMP" in instr.opname and isinstance(instr.argval, int):
                target_offset = instr.argval
                if target_offset in jump_targets:
                     arg_val_str = f"to {jump_targets[target_offset]}"
                     row_style = "on grey15"

            if instr.opname in ("LOAD_FAST_LOAD_FAST", "STORE_FAST_STORE_FAST", "STORE_FAST_LOAD_FAST"):
                arg_str = ""
                arg_val_str = f"{arg_val_str} (fused)"

            if hasattr(instr.argval, 'co_code'):
                name = getattr(instr.argval, 'co_name', '<code_block>')
                arg_val_str = f"<code: {name}>"
                nested_code_objects.append(instr.argval)

            if instr.opname == "NOT_TAKEN":
                arg_val_str = "(branch not taken — falls through)"

            if instr.opname == "CALL" and not arg_val_str:
                for j in range(i - 1, -1, -1):
                    prev = instructions[j]
                    if prev.opname in ("LOAD_GLOBAL", "LOAD_NAME", "LOAD_METHOD", "LOAD_ATTR", "LOAD_DEREF"):
                        call_name = str(prev.argval)
                        if call_name.startswith("NULL + "):
                            call_name = call_name[7:]
                        arg_val_str = f"calling {call_name}"
                        break
            
            table.add_row(line_str, offset_str, opcode_str, arg_str, arg_val_str, style=row_style)

        self.console.print(table)
        
        if nested_code_objects:
            from rich.rule import Rule
            self.console.print()

        for co in nested_code_objects:
            name = getattr(co, 'co_name', '<code_block>')
            self.console.print(Rule(f"[bold cyan]Disassembly of {name}[/]", style="cyan"))
            self.console.print()
            self.render(dis.get_instructions(co), title="")
