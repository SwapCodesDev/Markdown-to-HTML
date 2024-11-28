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


def convert_to_html(path_md, path_html):

    # Initialize variables
    is_code_block = False
    is_list = False
    is_task_list = False
    is_blockquote = False
    html_content = []
    lines = read(path_md)
    write(path_html, f"<!-- Markdown to HTML -->\n<link rel='stylesheet' href='example.css'>\n")

    # Convert the markdown to HTML
    for line in lines:

        # Blockquote
        if line.startswith(">"):
            is_blockquote = True

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

        # Append the line
        html_content.append(line.strip())

    for content in html_content:
        write(path_html, content + '\n', mode='a')


# Example usage
convert_to_html('example.md', 'example.html')
