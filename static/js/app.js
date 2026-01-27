/**
 * Markdown to HTML Converter - Web App
 * 
 * Handles real-time conversion, theme switching, and file operations.
 * 
 * Author: Carlos Crespo
 */

// DOM Elements
const markdownInput = document.getElementById('markdown-input');
const previewFrame = document.getElementById('preview-frame');
const themeSelect = document.getElementById('theme-select');
const tocCheckbox = document.getElementById('toc-checkbox');
const titleInput = document.getElementById('title-input');
const clearBtn = document.getElementById('clear-btn');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');
const toast = document.getElementById('toast');

// State
let currentHtml = '';
let debounceTimer = null;

/**
 * Show a toast notification
 */
function showToast(message, type = 'default') {
    toast.textContent = message;
    toast.className = 'toast show' + (type === 'success' ? ' success' : '');
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

/**
 * Convert markdown via API
 */
async function convertMarkdown() {
    const markdown = markdownInput.value;
    const theme = themeSelect.value;
    const includeToc = tocCheckbox.checked;
    const title = titleInput.value || 'Converted Document';

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                markdown,
                theme,
                includeToc,
                title
            }),
        });

        const data = await response.json();

        if (data.success) {
            currentHtml = data.html;
            updatePreview(data.html);
        } else {
            console.error('Conversion error:', data.error);
            showToast('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Request error:', error);
        showToast('Connection error. Please try again.');
    }
}

/**
 * Update the preview iframe
 */
function updatePreview(html) {
    const doc = previewFrame.contentDocument || previewFrame.contentWindow.document;
    doc.open();
    doc.write(html);
    doc.close();
}

/**
 * Debounced conversion (wait for typing to stop)
 */
function debouncedConvert() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(convertMarkdown, 300);
}

/**
 * Copy HTML to clipboard
 */
async function copyHtml() {
    if (!currentHtml) {
        showToast('Nothing to copy');
        return;
    }

    try {
        await navigator.clipboard.writeText(currentHtml);
        showToast('HTML copied to clipboard!', 'success');
    } catch (error) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = currentHtml;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('HTML copied to clipboard!', 'success');
    }
}

/**
 * Download HTML file
 */
function downloadHtml() {
    if (!currentHtml) {
        showToast('Nothing to download');
        return;
    }

    const title = titleInput.value || 'converted';
    const filename = title.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '.html';
    
    const blob = new Blob([currentHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('Downloaded ' + filename, 'success');
}

/**
 * Clear the editor
 */
function clearEditor() {
    markdownInput.value = '';
    currentHtml = '';
    updatePreview('');
    showToast('Editor cleared');
}

// Event Listeners
markdownInput.addEventListener('input', debouncedConvert);
themeSelect.addEventListener('change', convertMarkdown);
tocCheckbox.addEventListener('change', convertMarkdown);
titleInput.addEventListener('input', debouncedConvert);
clearBtn.addEventListener('click', clearEditor);
copyBtn.addEventListener('click', copyHtml);
downloadBtn.addEventListener('click', downloadHtml);

// Initial conversion on page load
document.addEventListener('DOMContentLoaded', convertMarkdown);
```

---

## ✅ Phase 3 Checkpoint

Your project structure should now look like this:
```
MarkdownToHTML/
├── api/
│   └── index.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
├── src/
│   └── md2html/
│       └── ... (existing files)
├── requirements.txt
├── vercel.json
└── ... (other existing files)
