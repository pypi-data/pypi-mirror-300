"""
Tool to create a new tool.

Outputs instructions for gptme to follow.
"""

from .base import ToolSpec

instructions = """
Call the tool to get started.
"""


def create_tool():
    print(
        "To create a new tool, first learn the steps by reading gptme/tools/__init__.py and a couple existing tools."
        "Choose some by listing the tools in the gptme/tools/ directory, dont pick a large one."
        "Then, create a new file in the tools directory and follow the instructions in the __init__.py file."
        "Finally, add the new tool to the tools/__init__.py file."
    )


tool = ToolSpec(
    name="create_tool",
    desc="Create a new tool for gptme",
    instructions=instructions,
    functions=[create_tool],
)
__doc__ += tool.get_doc(__doc__)
