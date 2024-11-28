import re

def markdown_to_html_line_by_line(file_path):
    # Open the Markdown file and read it line by line
    with open(file_path, 'r') as markdown_file:
        lines = markdown_file.readlines()

    html_output = []

    # Variables to handle multi-line elements
    in_code_block = False
    in_list = False
    in_task_list = False

    for line in lines:
        line = line.rstrip()

        # Handle Fenced Code Block
        if line.startswith("```"):
            if not in_code_block:
                html_output.append("<pre><code>")
                in_code_block = True
            else:
                html_output.append("</code></pre>")
                in_code_block = False
            continue

        if in_code_block:
            html_output.append(line)
            continue

        # Headings
        if line.startswith("#"):
            heading_level = len(re.match(r"^#+", line).group())
            content = line[heading_level + 1:]
            html_output.append(f"<h{heading_level}>{content}</h{heading_level}>")
            continue

        # Bold
        line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)

        # Italic
        line = re.sub(r"\*(.*?)\*", r"<em>\1</em>", line)

        # Strikethrough
        line = re.sub(r"~~(.*?)~~", r"<del>\1</del>", line)

        # Highlight
        line = re.sub(r"==(.*?)==", r"<mark>\1</mark>", line)

        # Subscript
        line = re.sub(r"~(.*?)~", r"<sub>\1</sub>", line)

        # Superscript
        line = re.sub(r"\^(.*?)\^", r"<sup>\1</sup>", line)

        # Blockquote
        if line.startswith(">"):
            html_output.append(f"<blockquote>{line[1:].strip()}</blockquote>")
            continue

        # Ordered List
        if re.match(r"^\d+\.\s", line):
            if not in_list:
                html_output.append("<ol>")
                in_list = True
            html_output.append(f"<li>{line[3:]}</li>")
            continue

        # Unordered List
        if re.match(r"^[-*]\s", line):
            if not in_list:
                html_output.append("<ul>")
                in_list = True
            html_output.append(f"<li>{line[2:]}</li>")
            continue

        # Task List
        if re.match(r"^-\s[ xX]\s", line):
            if not in_task_list:
                html_output.append("<ul>")
                in_task_list = True
            checked = "checked" if "[x]" in line or "[X]" in line else ""
            content = re.sub(r"-\s[ xX]\s", "", line)
            html_output.append(f'<li><input type="checkbox" {checked} disabled> {content}</li>')
            continue

        # Close Lists
        if in_list and not re.match(r"^\d+\.\s|^[-*]\s", line):
            html_output.append("</ol>" if line.startswith("1.") else "</ul>")
            in_list = False

        if in_task_list and not re.match(r"^-\s[ xX]\s", line):
            html_output.append("</ul>")
            in_task_list = False

        # Horizontal Rule
        if line == "---":
            html_output.append("<hr>")
            continue

        # Inline Code
        line = re.sub(r"`(.*?)`", r"<code>\1</code>", line)

        # Links
        line = re.sub(r"(.*?)(.*?)", r'<a href="\2">\1</a>', line)

        # Images
        line = re.sub(r"!(.*?)(.*?)", r'<img src="\2" alt="\1">', line)

        # Tables
        if "|" in line:
            if line.strip().startswith("|"):
                html_output.append("<table>")
                rows = line.split("|")[1:-1]
                html_output.append("<tr>" + "".join(f"<th>{cell.strip()}</th>" for cell in rows) + "</tr>")
                continue
            elif line.strip().startswith("-"):
                continue
            else:
                rows = line.split("|")[1:-1]
                html_output.append("<tr>" + "".join(f"<td>{cell.strip()}</td>" for cell in rows) + "</tr>")
                continue
        if line == "":
            if html_output and html_output[-1] == "</table>":
                html_output.append("</table>")

        # Paragraphs
        if line.strip():
            html_output.append(f"<p>{line}</p>")

    # Handle any open lists or code blocks
    if in_list:
        html_output.append("</ul>" if line.startswith("-") else "</ol>")
    if in_code_block:
        html_output.append("</code></pre>")

    return "\n".join(html_output)

# Usage
input_file = "m.md"  # Replace with your markdown file path
output = markdown_to_html_line_by_line(input_file)

# Save the output to an HTML file
with open("output.html", "w") as html_file:
    html_file.write(output)
