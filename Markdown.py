import re
from bs4 import BeautifulSoup


def read(path):
    with open(path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
    return [line for line in lines]  # Strip newline characters

def write(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

def convert_md_to_html(md_path, html_path):
    with open(html_path, 'w') as file:
        pass

    isCodeBlock = False
    write(html_path, "<html><body>\n")
    lines = read(md_path)

    for line in lines:
        # Handle escaping characters for HTML special characters
        line = re.sub(r'&', '&amp;', line)
        line = re.sub(r'<', '&lt;', line)
        line = re.sub(r'>', '&gt;', line)
        line = re.sub(r'"', '&quot;', line)
        line = re.sub(r"'", '&#39;', line)

        if line.startswith("```"):
            if isCodeBlock:  # If already inside a code block
                isCodeBlock = False  # End the current code block
                write(html_path, f"<pre><code>{code}</code></pre>")
            else:
                isCodeBlock = True
                language = re.match(r"```(\w+)", line).group(1)
                print(f"found: {language}")
                line = ''
                

        if isCodeBlock:
            code += line
            continue
        else:
            code = ''

        if line.startswith("```"):
                continue

        # 1. Convert headings (e.g., #heading -> <h1>heading</h1>)
        line = re.sub(r'^(#{1}) (.*)', r'<h1>\2</h1>', line, flags=re.MULTILINE)
        line = re.sub(r'^(#{2}) (.*)', r'<h2>\2</h2>', line, flags=re.MULTILINE)
        line = re.sub(r'^(#{3}) (.*)', r'<h3>\2</h3>', line, flags=re.MULTILINE)
        line = re.sub(r'^(#{4}) (.*)', r'<h4>\2</h4>', line, flags=re.MULTILINE)
        line = re.sub(r'^(#{5}) (.*)', r'<h5>\2</h5>', line, flags=re.MULTILINE)
        line = re.sub(r'^(#{6}) (.*)', r'<h6>\2</h6>', line, flags=re.MULTILINE)
        
        # 2. Convert bold (e.g., **bold** or __bold__ -> <strong>bold</strong>)
        line = re.sub(r'(\*\*|__)([^*_\n]+)\1', r'<strong>\2</strong>', line)

        # 3. Convert emphasis (e.g., *italic* or _italic_ -> <em>italic</em>)
        line = re.sub(r'(\*|_)([^*_\n]+)\1', r'<em>\2</em>', line)

        # 4. Convert inline code (e.g., `code` -> <code>code</code>)
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)

        # 5. Convert horizontal rule (e.g., --- -> <hr>)
        line = re.sub(r'---', r'<hr>', line)

        # 6. Convert images (e.g., ![alt](url) -> <img src="url" alt="alt">)
        line = re.sub(r'!\[([^\]]+)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', line)

        # 7. Convert links (e.g., [link](url) -> <a href="url">link</a>)
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)

        write(html_path, line)


    write(html_path, "\n</html></body>\n")



def beautify_html(file_path):
    try:
        # Read the HTML file
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Parse and beautify the HTML content
        soup = BeautifulSoup(content, "html.parser")
        beautified_html = soup.prettify()

        # Create a new file name for the output
        output_file = file_path

        # Save the beautified HTML
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(beautified_html)

        print(f"Beautified HTML saved to: {output_file}")
        return output_file

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
convert_md_to_html('readme.md', 'example.html')
beautify_html("example.html")
