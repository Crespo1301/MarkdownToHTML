"""
Flask API for Markdown to HTML Converter

Provides web interface and API endpoint for converting
Markdown to styled HTML.

Author: Carlos Crespo
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from flask import Flask, request, jsonify, render_template, send_from_directory
from md2html.parser import MarkdownParser
from md2html.converter import HTMLConverter
from md2html.styles import Theme

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)


@app.route('/')
def home():
    """Render the main web interface."""
    return render_template('index.html')


@app.route('/api/convert', methods=['POST'])
def convert():
    """
    API endpoint to convert Markdown to HTML.
    
    Expects JSON: {"markdown": "...", "theme": "light|dark", "includeToc": true|false}
    Returns JSON: {"html": "...", "success": true} or {"error": "...", "success": false}
    """
    try:
        data = request.get_json()
        
        if not data or 'markdown' not in data:
            return jsonify({'error': 'No markdown provided', 'success': False}), 400
        
        markdown_text = data.get('markdown', '')
        theme_name = data.get('theme', 'light')
        include_toc = data.get('includeToc', True)
        title = data.get('title', 'Converted Document')
        fragment_only = data.get('fragmentOnly', False)
        
        # Select theme
        theme = Theme.DARK if theme_name == 'dark' else Theme.LIGHT
        
        # Parse and convert
        parser = MarkdownParser()
        tokens = parser.parse(markdown_text)
        headers = parser.get_headers()
        
        converter = HTMLConverter(
            theme=theme,
            include_toc=include_toc,
            include_styles=True
        )
        
        if fragment_only:
            html = converter.convert_fragment(tokens)
        else:
            html = converter.convert(tokens, title=title, headers=headers)
        
        return jsonify({
            'html': html,
            'success': True,
            'stats': {
                'headers': len(headers),
                'tokens': len(tokens)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(app.static_folder, filename)


# Vercel requires this
if __name__ == '__main__':
    app.run(debug=True, port=5000)
