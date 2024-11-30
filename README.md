# Markdown to HTML Converter using Python

This repository contains a Python script that converts Markdown files into HTML with advanced features, supporting a wide range of Markdown elements and extensions.

## Features

- [x] Heading
- [x] Bold
- [x] Italic
- [x] Blockquote
- [x] Ordered List
- [x] Unordered List
- [x] Code
- [x] Horizontal Rule
- [x] Link
- [x] Image
- [x] Table
- [x] Code Block
- [x] Footnote
- [x] Definition List
- [x] Strikethrough
- [x] Task List
- [x] Emoji
- [x] Highlight
- [x] Subscript
- [x] Superscript

## Requirements

- Python 3.7 or higher
- Dependencies:
  - `beautifulsoup4`
  - `emoji`

Install the dependencies using:

```bash
pip install beautifulsoup4 emoji
```

## How to Use

1. Place your Markdown file in the project directory (e.g., `example.md`).
2. Run the script with the following command:

```bash
python Markdown.py
```

3. The converted HTML file (e.g., `example.html`) will be generated in the same directory.

## Example

### Input (`example.md`)

```markdown
# Welcome

This is **bold** text and *italic* text.

- Item 1
- Item 2

[Visit Google](https://google.com)
```

### Output (`example.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Markdown to HTML</title>
</head>
<body>
  <h1>Welcome</h1>
  <p>This is <strong>bold</strong> text and <em>italic</em> text.</p>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
  <p><a href="https://google.com">Visit Google</a></p>
</body>
</html>
```

## Additional Features

### Footnotes

```markdown
Here is a sentence with a footnote.[^1]

[^1]: This is the footnote content.
```

### Tables

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |
```

### Task Lists

```markdown
- [x] Completed Task
- [ ] Incomplete Task
```

### Emoji Support

Use emojis like `:smile:` or `:rocket:`.

## Error Handling

The script handles common errors such as missing files or incorrect formats and provides detailed error messages for troubleshooting.

## Contribution

Feel free to submit issues or pull requests to improve the script.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.