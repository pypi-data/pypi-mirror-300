from vvclasses.utils import ColorPrinter
import os
import re
import sys 
import argparse

def colors():
    blue = ColorPrinter.COLORS['blue']
    green = ColorPrinter.COLORS['green']
    red = ColorPrinter.COLORS['red']
    bold = ColorPrinter.COLORS['bold']
    bright_magenta = ColorPrinter.COLORS['bright_magenta']
    bright_red = ColorPrinter.COLORS['bright_red']
    cyan = ColorPrinter.COLORS['cyan']
    bright_blue = ColorPrinter.COLORS['bright_blue']
    bright_yellow = ColorPrinter.COLORS['bright_yellow']
    bright_cyan = ColorPrinter.COLORS['bright_cyan']
    return blue, green, red, bold, bright_magenta, bright_red, cyan, bright_blue, bright_yellow, bright_cyan



def print_md(text, style="monokai"):
    blue, green, red, bold, bright_magenta, bright_red, cyan, bright_blue, bright_yellow, bright_cyan = colors()
    printer_markdown = ColorPrinter(
        print_pattern="markdown",
        color_list=[
            bright_magenta,  # Headers
            bright_red,      # Bold
            green,           # Italics
            cyan,            # Inline code
            bright_blue,     # Links
            bright_yellow,   # Lists
            bright_cyan      # Blockquotes
        ],
        text_list=text
    )
    printer_markdown.execute_print(text=text, style=style)

def print_random(text):
    blue, green, red, bold, bright_magenta, bright_red, cyan, bright_blue, bright_yellow, bright_cyan = colors()
    printer_random = ColorPrinter(
        print_pattern="random",
        color_list=[blue, green, red, bold],
        text_list=text
    )
    printer_random.execute_print()

def print_alternating(text):
    blue, green, red, bold, bright_magenta, bright_red, cyan, bright_blue, bright_yellow, bright_cyan = colors()
    printer_alternating = ColorPrinter(
        print_pattern="new-line-alternating",
        color_list=[blue, green, red],
        text_list=text
    )
    printer_alternating.execute_print()

def print_grouped(text, group_size=4):
    blue, green, red, bold, bright_magenta, bright_red, cyan, bright_blue, bright_yellow, bright_cyan = colors()
    printer_grouped = ColorPrinter(
        group_size=group_size,
        print_pattern="grouped",
        color_list=[blue, green, red],
        text_list=text,
    )
    printer_grouped.execute_print(group_size=group_size)
    

#
# long_text_list_random = [
#     "This", "is", "a", "long", "text", "list", "that", "will", "be", "printed",
#     "in", "a", "random", "color", "pattern", "with", "a", "total", "of", "4",
#     "colors", "and", "a", "total", "of", "24", "words"
# ]
#
# long_text_list_alternating = [
#     "This", "is", "a", "long", "text", "list", "that", "will", "be", "printed",
#     "in", "a", "new-line-alternating", "color", "pattern", "with", "a", "total",
#     "of", "4", "colors", "and", "a", "total", "of", "24", "words"
# ]
#
# long_text_list_grouped = [
#     "This", "is", "a", "long", "text", "list", "that", "will", "be", "printed",
#     "in", "a", "grouped", "color", "pattern", "with", "a", "total", "of", "4",
#     "colors", "and", "a", "total", "of", "24", "words"
# ]
#
#
# if os.path.exists("EXAMPLEREADME.md"):
#     with open("EXAMPLEREADME.md", "r") as f:
#         markdown_text_list = f.read()
#
# if not markdown_text_list:
#     markdown_text_list = [
#         "# This is a markdown file",
#         "## This is a markdown file",
#         "### This is a markdown file",
#         "#### This is a markdown file",
#         "##### This is a markdown file",
#         "###### This is a markdown file",
#         "This is a markdown file",
#         "This is a markdown file", ]
#
# printer_random = ColorPrinter(
#     print_pattern="random",
#     color_list=[blue, green, red, bold],
#     text_list=long_text_list_random
# )
#
#
# printer_alternating = ColorPrinter(
#     print_pattern="new-line-alternating",
#     color_list=[blue, green, red],
#     text_list=long_text_list_alternating
# )
#
#
# printer_grouped = ColorPrinter(
#     print_pattern="grouped",
#     color_list=[blue, green, red],
#     text_list=long_text_list_grouped
# )
#
#
#
# printer_markdown = ColorPrinter(
#     print_pattern="markdown",
#     color_list=[
#         bright_magenta,  # Headers
#         bright_red,      # Bold
#         green,           # Italics
#         cyan,            # Inline code
#         bright_blue,     # Links
#         bright_yellow,   # Lists
#         bright_cyan      # Blockquotes
#     ],
#     text_list=markdown_text_list
# )
#
# # printer_markdown.execute_print(text=markdown_text_list, style=style)
# # print("\n\n")
# # printer_random.execute_print()
# # print("\n\n")
# # printer_alternating.execute_print()
# # print("\n\n")
# # printer_grouped.execute_print(group_size=3)
#
# parser = argparse.ArgumentParser(description='Print markdown text with syntax highlighting')
# parser.add_argument('--style', type=str, help='The pygments style to use for syntax highlighting')
# args = parser.parse_args()
#
# if args.style:
#     printer_markdown.execute_print(text=markdown_text_list, style=args.style)
# else:
#     printer_markdown.execute_print(text=markdown_text_list)
#
