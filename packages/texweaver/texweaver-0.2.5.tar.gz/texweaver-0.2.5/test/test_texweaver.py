from texweaver import TexParser
from texweaver import DefaultConfig
def test_parser():
    src = """
# Heading 1

## Heading 2

### Heading 3

This is a **bold** text.

This is an *italic* text.

### Heading 3

This is an inline code `print('Hello, World!')`.

## Heading 2

This is a code block:

```python
def hello_world():
    print('Hello, World!')
```

This is an inline LaTeX formula: $E = mc^2$.

This is a LaTeX formula block:

$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

![GitHub Logo](/path/to/image.png)

This is an unordered list:

- Item 1
- Item 2
- Item 3

This is an ordered list:

1. Item 1
2. Item 2
3. Item 3
    """
    
    parser = TexParser()
    parser.parse(src)
    mdoc = parser.doc
    latex = mdoc.to_latex(DefaultConfig)
    print(latex)
    
if __name__ == '__main__':
    test_parser()