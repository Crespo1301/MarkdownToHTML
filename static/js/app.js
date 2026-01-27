/**
 * Markdown to HTML Converter - Web App
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
const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-input');
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

    if (!markdown.trim()) {
        updatePreview('<html><body><p style="color:#888;padding:20px;">Enter some Markdown to see the preview...</p></body></html>');
        return;
    }

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
    updatePreview('<html><body></body></html>');
    showToast('Editor cleared');
}

/**
 * Handle file upload
 */
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.md') && !file.name.endsWith('.markdown') && !file.name.endsWith('.txt')) {
        showToast('Please upload a .md, .markdown, or .txt file');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        markdownInput.value = e.target.result;
        // Set title from filename
        const baseName = file.name.replace(/\.(md|markdown|txt)$/, '');
        titleInput.value = baseName;
        convertMarkdown();
        showToast('File loaded: ' + file.name, 'success');
    };
    reader.onerror = function() {
        showToast('Error reading file');
    };
    reader.readAsText(file);
    
    // Reset input so same file can be uploaded again
    event.target.value = '';
}

/**
 * Trigger file input click
 */
function triggerUpload() {
    fileInput.click();
}

// Event Listeners
markdownInput.addEventListener('input', debouncedConvert);
themeSelect.addEventListener('change', convertMarkdown);
tocCheckbox.addEventListener('change', convertMarkdown);
titleInput.addEventListener('input', debouncedConvert);
clearBtn.addEventListener('click', clearEditor);
copyBtn.addEventListener('click', copyHtml);
downloadBtn.addEventListener('click', downloadHtml);
uploadBtn.addEventListener('click', triggerUpload);
fileInput.addEventListener('change', handleFileUpload);

// Initial conversion on page load
document.addEventListener('DOMContentLoaded', convertMarkdown);