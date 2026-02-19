import click
import sys
import os
from ydis.core.disassembler import Disassembler
from ydis.render.rich_output import RichRenderer

@click.command()
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    """
    Disassemble a Python file.
    """
    try:
        with open(path, 'r') as f:
            source = f.read()
        
        # Compile the source to a code object
        code_obj = compile(source, path, 'exec')
        
        disassembler = Disassembler()
        instructions = disassembler.get_instructions(code_obj)
        
        renderer = RichRenderer()
        renderer.render(instructions)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
