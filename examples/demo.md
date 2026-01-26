# Markdown to HTML Converter Demo

This document demonstrates all the Markdown features supported by the md2html converter.

## Text Formatting

You can make text **bold** using double asterisks or __underscores__.

Text can be *italicized* with single asterisks or _underscores_.

For ***bold and italic*** together, use triple asterisks or ___underscores___.

## Links and Images

Here's a [link to GitHub](https://github.com) for more information.

You can also add a title: [Visit Google](https://google.com "Google Search Engine")

Images work similarly:

![Placeholder Image](https://via.placeholder.com/400x200 "Example Image")

## Headers

### This is an H3

#### This is an H4

##### This is an H5

###### This is an H6

## Code

Inline code looks like `const greeting = "Hello World";` in your text.

### Code Blocks

Here's a JavaScript example:

```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(10)); // Output: 55
```

And a Python example:

```python
def quicksort(arr):
    """Implement quicksort algorithm."""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)
```

Indented code blocks also work:

    This is a code block
    created with 4 spaces
    of indentation

## Lists

### Unordered Lists

- First item
- Second item
- Third item with nested items:
  - Nested item A
  - Nested item B
    - Even deeper nesting
- Fourth item

### Ordered Lists

1. First step
2. Second step
3. Third step
4. Fourth step

## Blockquotes

> This is a blockquote. It can span multiple lines
> and is great for highlighting important information
> or quoting external sources.

## Horizontal Rules

Here's a horizontal rule:

---

And another style:

***

## Putting It All Together

Here's a practical example combining multiple elements:

> **Pro Tip:** When learning a new programming language, try building small projects like a **markdown converter**! It teaches you:
> 
> 1. File I/O operations
> 2. String manipulation
> 3. Regular expressions
> 4. Object-oriented design

Check out the [project repository](https://github.com/Crespo1301/MarkdownToHTML) for the full source code.

---

*Generated with md2html by Carlos Crespo*
