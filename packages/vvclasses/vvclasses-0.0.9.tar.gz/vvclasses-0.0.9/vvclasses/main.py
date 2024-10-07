# Path: ./vvclasses_project/vvclasses.py 

from vvclasses.utils import ColorPrinter

def main():
    blue = ColorPrinter.COLORS['blue']
    bold = ColorPrinter.COLORS['bold']
    red = ColorPrinter.COLORS['red']
    green = ColorPrinter.COLORS['green']
    yellow = ColorPrinter.COLORS['yellow']
    magenta = ColorPrinter.COLORS['magenta']
    cyan = ColorPrinter.COLORS['cyan']
    bright_white = ColorPrinter.COLORS['bright_white']

    hi = "Hello"
    hello = "World"
    text_list = ["Blue Text", "Bold Text", "Red Text", hi, hello]

    color_list = [blue, bold, red, green, yellow, magenta, cyan, bright_white]

    printer = ColorPrinter(
        print_pattern="new-line-alternating",
        color_list=color_list,
        text_list=text_list
    )

    printer.execute_print()
