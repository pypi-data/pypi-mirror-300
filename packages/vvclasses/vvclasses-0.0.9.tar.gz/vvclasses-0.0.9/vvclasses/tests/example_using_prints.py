from vvclasses import ColorPrinter, print_md, print_random, print_alternating, print_grouped
import os


def print_random_text():
    long_text_list_random = [
        "This", "is", "a", "long", "text", "list", "that", "will", "be", "printed",
        "in", "a", "random", "color", "pattern", "with", "a", "total", "of", "4",
        "colors", "and", "a", "total", "of", "24", "words"
    ]
    print_random(long_text_list_random)

def print_alternating_text():
    long_text_list_alternating = [
        "This", "is", "a", "long", "text", "list", "that", "will", "be", "printed",
        "in", "a", "new-line-alternating", "color", "pattern", "with", "a", "total",
        "of", "4", "colors", "and", "a", "total", "of", "24", "words"
    ]
    print_alternating(long_text_list_alternating)

def print_grouped_text():
    long_text_list_grouped = [
        "This", "is", "a", "long", "text", "list", "that", "will", "be", "printed",
        "in", "a", "grouped", "color", "pattern", "with", "a", "total", "of", "4",
        "colors", "and", "a", "total", "of", "24", "words"
    ]
    print_grouped(long_text_list_grouped, group_size=2)


def my_text():
    # You can also read a file and return the text as the string
    # with open("path/to/file.md", "r") as f:
    #     text = f.read()
    text = """# toml-cfg-tool  

## Table of Contents

- [Prerequisites](#prerequisites)

## Prerequisites

- [Python](https://www.python.org/downloads/)

## Arguments 

The tool accepts the following arguments:
- `--show`: Show the current configuration. (only shows the options that can be updated)

# Testing block code reading

```python
import os
import sys
import requests
import json
from datetime import datetime

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        sys.exit(1)

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

def main():
    url = "https://api.example.com/data"
    data = fetch_data(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_{timestamp}.json"
    save_data(data, filename)

if __name__ == "__main__":
    main()
```"""
    return text

def main():
    text = my_text()
    print("Printing MD:")
    print_md(text, style="github-dark")
    print("Printing Random:")
    print_random_text()
    print("Printing Alternating:")
    print_alternating_text()
    print("Printing Grouped:")
    print_grouped_text()

if __name__ == "__main__":
    main()
