# Path: ./vvclasses_project/printclass.py

from colorama import init, Fore, Style
import random
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.styles import get_style_by_name, get_all_styles
from pygments.formatters import TerminalTrueColorFormatter
from pygments.util import ClassNotFound

# Initialize colorama
init(autoreset=True)

class ColorPrinter:
    """
    A class to print colored text in the terminal based on specified patterns.
    """

    # ANSI escape codes for colors using colorama's Fore and Style
    COLORS = {
        'black': Fore.BLACK,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'bright_black': Style.DIM + Fore.BLACK,
        'bright_red': Style.BRIGHT + Fore.RED,
        'bright_green': Style.BRIGHT + Fore.GREEN,
        'bright_yellow': Style.BRIGHT + Fore.YELLOW,
        'bright_blue': Style.BRIGHT + Fore.BLUE,
        'bright_magenta': Style.BRIGHT + Fore.MAGENTA,
        'bright_cyan': Style.BRIGHT + Fore.CYAN,
        'bright_white': Style.BRIGHT + Fore.WHITE,
        'bold': Style.BRIGHT  # Using Style.BRIGHT as a substitute for bold
    }

    END = Style.RESET_ALL  # Reset to default

    # some popular style options are: 'monokai', 'dracula', 'vs', 'paraiso-dark', 'paraiso-light', 'github'
    def __init__(self, print_pattern="new-line-alternating", color_list=None, text_list=None, style='paraiso-dark'):
        """
        Initializes the ColorPrinter with specified parameters.

        Args:
            print_pattern (str): The pattern to use for printing (e.g., 'new-line-alternating', 'random', 'grouped').
            color_list (list): List of ANSI color codes.
            text_list (list): List of texts to print.
        """
        # Input validation
        if not isinstance(print_pattern, str):
            raise ValueError("print_pattern must be a string.")
        if color_list is not None and not isinstance(color_list, list):
            raise ValueError("color_list must be a list or None.")
        if not print_pattern == "markdown" and text_list is not None and not isinstance(text_list, list):
            raise ValueError("text_list must be a list or None.")

        self.style = style
        self.print_pattern = print_pattern
        self.color_list = color_list if color_list is not None else [
            self.COLORS['blue'], self.COLORS['bold']
        ]
        self.text_list = text_list if text_list is not None else []

        # Number of colors determined by the length of color_list
        self.color_count = len(self.color_list)

        # Ensure color_list has at least one color
        if self.color_count == 0:
            raise ValueError("color_list must contain at least one color.")

    def new_line_alternating(self):
        """
        Prints each text in text_list with a corresponding color from color_list in an alternating pattern.
        """
        for index, text in enumerate(self.text_list):
            color = self.color_list[index % self.color_count]
            print(f"{color}{text}{self.END}")

    def markdown_pattern(self, text, style):
        """
        Prints a single block of Markdown-formatted text with colors based on Markdown specifiers.
        Supports the following Markdown elements:
            - Headers (#, ##, ###, etc.)
            - Bold (**text** or __text__)
            - Italics (*text* or _text_)
            - Inline Code (`code`)
            - Links ([text](url))
            - Lists (- item, * item, + item)
            - Blockquotes (> quote)
            - Code Blocks (```language ... ```)
    
        Args:
            text (str): The Markdown-formatted text to print.
        """
        # Split the text into lines
        lines = text.split('\n')
    
        # Define regex patterns for block-level and inline-level markdown
        block_patterns = [
            (r'^(#{1,6})(\s+)(.*)', self.COLORS['bright_magenta']),          # Headers
            (r'^(\s*[-*+])(\s+)(.*)', self.COLORS['bright_yellow']),        # Lists
            (r'^(>)(\s+)(.*)', self.COLORS['bright_cyan']),                 # Blockquotes
        ]
    
        inline_patterns = [
            # Order matters: longer patterns should be first
            (r'(\*\*|__)(.*?)\1', self.COLORS['bright_red']),              # Bold with ** or __
            (r'(\*|_)(.*?)\1', self.COLORS['green']),                      # Italics with * or _
            (r'(`)(.*?)\1', self.COLORS['cyan']),                           # Inline code
            (r'(\[)(.*?)(\])(\()(.*?)(\))', self.COLORS['bright_blue']),   # Links [text](url)
        ]
    
        code_block_start_pattern = re.compile(r'^```(\w+)?')
        code_block_end_pattern = re.compile(r'^```')
    
        inside_code_block = False
        code_block_language = ''
        code_block_lines = []
    
        for line in lines:
            stripped_line = line.strip()
    
            if not inside_code_block:
                # Check for code block start
                start_match = code_block_start_pattern.match(stripped_line)
                if start_match:
                    inside_code_block = True
                    code_block_language = start_match.group(1) if start_match.group(1) else ''
                    print(f"{self.COLORS['bright_cyan']}{stripped_line}{self.END}")
                    continue  # Move to the next line
    
                # Check block-level patterns first
                color_assigned = False
                for pattern, color in block_patterns:
                    match = re.match(pattern, line)
                    if match:
                        prefix, space, content = match.groups()
                        # Now process the content for inline patterns
                        colored_content = self.apply_inline_patterns(content, inline_patterns)
                        # Apply color to the entire line
                        print(f"{color}{prefix}{space}{colored_content}{self.END}")
                        color_assigned = True
                        break
                if color_assigned:
                    continue  # Move to the next line
    
                # Handle inline patterns
                colored_line = self.apply_inline_patterns(line, inline_patterns)
                # Print the colored line with default white color
                print(f"{self.COLORS['white']}{colored_line}{self.END}")
            else:
                # Inside a code block
                end_match = code_block_end_pattern.match(stripped_line)
                if end_match:
                    # Apply syntax highlighting to the accumulated code block
                    highlighted_code = self.syntax_highlight('\n'.join(code_block_lines), code_block_language, style)
                    print(highlighted_code)
                    # Print the code block end
                    print(f"{self.COLORS['bright_cyan']}{stripped_line}{self.END}")
                    # Reset code block state
                    inside_code_block = False
                    code_block_language = ''
                    code_block_lines = []
                else:
                    # Accumulate code lines
                    code_block_lines.append(line)

    def syntax_highlight(self, code, language, style):
        """
        Applies syntax highlighting to a block of code using Pygments.
    
        Args:
            code (str): The code block to highlight.
            language (str): The programming language of the code.
    
        Returns:
            str: The syntax-highlighted code block with ANSI color codes.
        """
        try:
            if language:
                lexer = get_lexer_by_name(language, stripall=True)
            else:
                lexer = TextLexer()
        except ClassNotFound:
            lexer = TextLexer()

        try:
            style = get_style_by_name(style)
        except ClassNotFound:
            style = get_style_by_name(self.style)

        try:
            # Always ensure a valid formatter is set
            formatter = TerminalTrueColorFormatter(style=style)
            highlighted_code = highlight(code, lexer, formatter)
        except Exception as e:
            print(f"Error creating formatter with style '{style}': {e}")
            # Return an empty string or the raw code in case of error
            highlighted_code = code

        return highlighted_code  # Always return a valid string

    def apply_inline_patterns(self, text, patterns):
        """
        Applies inline markdown patterns to the given text and returns the colored text.

        Args:
            text (str): The text to apply patterns on.
            patterns (list): List of tuples containing regex patterns and their corresponding colors.

        Returns:
            str: The text with ANSI color codes applied.
        """
        for pattern, color in patterns:
            def replacer(match):
                if pattern == r'(\[)(.*?)(\])(\()(.*?)(\))':
                    # Links: [text](url)
                    replacement = f"{self.COLORS['bright_blue']}{match.group(1)}{self.COLORS['white']}{match.group(2)}{self.COLORS['bright_blue']}{match.group(3)}{self.COLORS['white']}{match.group(4)}{self.COLORS['bright_blue']}{match.group(5)}{self.COLORS['bright_blue']}{match.group(6)}{self.END}"
                    return replacement 
                else:
                    # Other inline elements
                    replacement = f"{color}{match.group(0)}{self.END}"
                    return replacement

            text = re.sub(pattern, replacer, text)
        return text

    def random_pattern(self):
        """
        Prints each text in text_list with a randomly selected color from color_list.
        """
        for text in self.text_list:
            color = random.choice(self.color_list)
            print(f"{color}{text}{self.END}")

    def grouped_pattern(self, group_size=2):
        """
        Prints texts in groups, applying the same color to each group.

        Args:
            group_size (int): Number of texts per group to share the same color.
        """
        if not isinstance(group_size, int) or group_size <= 0:
            raise ValueError("group_size must be a positive integer.")

        for i in range(0, len(self.text_list), group_size):
            group = self.text_list[i:i + group_size]
            color = self.color_list[(i // group_size) % self.color_count]
            for text in group:
                print(f"{color}{text}{self.END}")

    def execute_print(self, **kwargs):
        """
        Executes the print method based on the specified print_pattern.

        Args:
            **kwargs: Additional keyword arguments for specific patterns (e.g., group_size for 'grouped').
        """
        if self.print_pattern == "new-line-alternating":
            self.new_line_alternating()
        elif self.print_pattern == "random":
            self.random_pattern()
        elif self.print_pattern == "markdown":
            text = kwargs.get('text', '')
            style = kwargs.get('style', self.style)
            if not isinstance(text, str):
                # convert from a list to a string 
                text = ' '.join(text)
                if not isinstance(text, str):
                    raise ValueError("text must be a string.")
            self.markdown_pattern(text, style)
        elif self.print_pattern == "grouped":
            group_size = kwargs.get('group_size', 2)
            self.grouped_pattern(group_size=group_size)
        else:
            print(f"Unrecognized print pattern: {self.print_pattern}. Defaulting to 'new-line-alternating'.")
            self.new_line_alternating()

