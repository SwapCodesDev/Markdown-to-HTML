import re
from bs4 import BeautifulSoup


def read(path):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            return file.readlines()  # Read all lines into a list
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied for file {path}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return None


def write(path, data, mode='w'):
    try:
        with open(path, mode, encoding="utf-8") as file:
            file.write(data)
    except PermissionError:
        print(f"Error: Permission denied for writing to file {path}.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while writing to the file: {e}")
        return False
    return True


def beautify_html(path, output_path=None):
    try:
        # Read the HTML file
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        # Parse and beautify the HTML content
        soup = BeautifulSoup(content, "html.parser")
        beautified_html = soup.prettify()

        # Save the beautified HTML to the specified output path or overwrite the original
        output_file = output_path if output_path else path
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(beautified_html)

        return output_file

    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied for file {path}.")
        return None
    except Exception as e:
        print(f"An error occurred while beautifying the HTML: {e}")
        return None


def Handle_escaping_characters(line):
    line = re.sub(r'&', '&amp;', line)
    line = re.sub(r'<', '&lt;', line)
    line = re.sub(r'>', '&gt;', line)
    line = re.sub(r'"', '&quot;', line)
    line = re.sub(r"'", '&#39;', line)
    return line


def convert_heading(line):
    level = len(re.match(r"^#+", line).group())
    return f"<h{level}>{line[level + 1:].strip()}</h{level}>"


def convert_bold(line):
    return re.sub(r"(\*\*|__)(.*)\1", r"<strong>\2</strong>", line)


def convert_italic(line):
    return re.sub(r"(\*|_)(.*?)\1", r"<em>\2</em>", line)


def convert_strikethrough(line):
    return re.sub(r"~~(.*?)~~", r"<del>\1</del>", line)


def convert_blockquote(line):
    return f"<blockquote><p>{line[1:].strip()}</p></blockquote>"


def convert_subscript(line):
    return re.sub(r"~(.*?)~", r"<sub>\1</sub>", line)


def convert_superscript(line):
    return re.sub(r"\^(.*?)\^", r"<sup>\1</sup>", line)


def convert_highlight(line):
    return re.sub(r"==(.*?)==", r"<mark>\1</mark>", line)


def convert_inline_code(line):
    return re.sub(r"`(.*?)`", r"<code>\1</code>", line)


def convert_url_text(line):
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', line)


def convert_url_image(line):
    return re.sub(r"!\[([^\]]+)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', line)


def convert_horizontal_rule(line):
    return re.sub(r'---', r'<hr>', line)


def handle_hybrid_list(line, current_indent, indent_stack, html_content, list_type):
    """
    Handles both ordered and unordered lists, including hybrid structures.
    Args:
        line (str): The current line being processed.
        current_indent (int): Current indentation level.
        indent_stack (list): Stack to track nesting levels.
        html_content (list): List of HTML strings to append to.
        list_type (str): Type of list ('ol' for ordered, 'ul' for unordered).

    Returns:
        (int, str): Updated current indentation and list type.
    """
    stripped_line = line.lstrip()
    indent_level = len(line) - len(stripped_line)
    new_list_type = None

    # Determine the list type (ordered or unordered)
    if re.match(r"^\d+\.\s", stripped_line):
        new_list_type = "ol"
    elif stripped_line.startswith(('-', '+', '*')):
        new_list_type = "ul"

    if new_list_type:
        # Handle switching between list types
        if list_type and new_list_type != list_type:
            while indent_stack:
                html_content.append(f'</{list_type}>')
                indent_stack.pop()
            list_type = None

        # Handle nested or continued list
        if indent_level > current_indent:
            html_content.append(f'<{new_list_type}>')
            indent_stack.append(indent_level)
        while indent_stack and indent_level < indent_stack[-1]:
            html_content.append(f'</{new_list_type}>')
            indent_stack.pop()

        # Add list item
        list_content = (
            stripped_line[stripped_line.index('.') + 1:].strip()
            if new_list_type == "ol"
            else stripped_line[1:].strip()
        )
        html_content.append(f"<li>{list_content}</li>")
        return indent_level, new_list_type

    # Close any open lists if not a list item
    while indent_stack:
        html_content.append(f'</{list_type}>')
        indent_stack.pop()
    return 0, None


def convert_to_html(path_md, path_html):

    # Initialize variables
    is_code_block = False
    is_def_list = False
    is_ordered_list = False
    is_unordered_list = False
    is_task_list = False
    is_blockquote = False
    indent_stack = []
    current_list_type = None  # Tracks the current list type ('ol' or 'ul')
    current_indent = 0
    html_content = []
    lines = read(path_md)

    html_initial_body = (
    "<!DOCTYPE html>\n"
    "<html lang=\"en\">\n"
    "<head>\n"
    "  <meta charset=\"UTF-8\">\n"
    "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
    "  <title>Markdown to HTML</title>\n"
    "  <!-- Highlight.js Styles -->\n"
    "  <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css\">\n"
    "  <link rel='stylesheet' href='example.css'>\n"
    "  <script src=\"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js\"></script>\n"
    "  <script src=\"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js\"></script>\n"
    )

    html_end_body = (
        "  <script>hljs.highlightAll();</script>\n"
        "</body>\n"
        "</html>"
    )


    write(path_html, html_initial_body)

    # Convert the markdown to HTML
    for line in lines:

        # Blockquote
        if line.startswith(">"):
            is_blockquote = True

        # Handle Fenced Code Block
        if line.startswith("```"):
            if not is_code_block:
                html_content.append("<pre><code>")
                is_code_block = True
            else:
                html_content.append("</code></pre>")
                is_code_block = False
            continue

        if is_code_block:
            html_content.append(line)
            continue

        # Handle escaping characters except blockquotes
        if not is_blockquote:
            line = Handle_escaping_characters(line)
        else:
            line = Handle_escaping_characters(line[1:])
            line = convert_blockquote(line)
            is_blockquote = False
        
        # Heading
        if line.startswith("#"):
            html_content.append(convert_heading(line))
            continue
        
        # Horizontal rule
        if line.strip() == "---":
            html_content.append(convert_horizontal_rule(line))
            continue

        # Bold
        if re.search(r"(\*\*|__)(.*?)\1", line):
            line = convert_bold(line)
        
        # Italic
        if re.search(r"(\*|_)(.*?)\1", line):
            line = convert_italic(line)

        # Strikethrough
        if re.search(r"~~(.*?)~~", line):
            line = convert_strikethrough(line)

        # Subscript
        if re.search(r"~(.*?)~", line):
            line = convert_subscript(line)

        # Superscript
        if re.search(r"\^(.*?)\^", line):
            line = convert_superscript(line)

        # Highlight
        if re.search(r"==(.*?)==", line):
            line = convert_highlight(line)
        
        # Inline Code
        if re.search(r"`(.*?)`", line):
            line = convert_inline_code(line)

        # Image
        if re.search(r"!\[([^\]]+)\]\(([^)]+)\)", line):
            line = convert_url_image(line)

        # Link
        if re.search(r"\[([^\]]+)\]\(([^)]+)\)", line):
            line = convert_url_text(line)

        # Ordered and unordered list
        if re.match(r"^\d+\.\s", line.lstrip()):  # Check for ordered list
            if not is_ordered_list:
                is_ordered_list = True
                html_content.append('<ol>')
            current_indent, current_list_type = handle_hybrid_list(
                line, current_indent, indent_stack, html_content, current_list_type
            )
            continue  # Skip to the next line after processing
        elif line.lstrip().startswith(('-', '+', '*')):  # Check for unordered list
            if not is_unordered_list:
                is_unordered_list = True
                html_content.append('<ul>')
            current_indent, current_list_type = handle_hybrid_list(
                line, current_indent, indent_stack, html_content, current_list_type
            )
            continue  # Skip to the next line after processing
        else:
            if is_ordered_list:
                is_ordered_list = False
                html_content.append('</ol>')
            if is_unordered_list:
                is_unordered_list = False
                html_content.append('</ul>')
        
        # Definition list
        if line.startswith(":"):
            if not is_def_list:
                if html_content[-2].strip().startswith("</dl>"):
                    html_content[-2] = f"<dt>{html_content[-1]}</dt>"
                    html_content.pop()
                    is_def_list = True
                else:
                    html_content[-1] = f"<dl>\n<dt>{html_content[-1]}</dt>"
                    is_def_list = True
            if is_def_list:
                line = f"<dd>{line[1:].strip()}</dd>"
        else:
            if is_def_list:
                html_content.append("</dl>")
                is_def_list = False

        # Append the line
        html_content.append(line.strip())

    if is_def_list:  # Ensure closing <dl> if still in definition list at the end
        html_content.append("</dl>")

    for content in html_content:
        write(path_html, content + '\n', mode='a')
    
    write(path_html, html_end_body, mode='a')


# Example usage
convert_to_html('example.md', 'example.html')
