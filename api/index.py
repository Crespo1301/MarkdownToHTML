"""
Vercel Serverless Function for Markdown to HTML Converter
Author: Carlos Crespo
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import parse_qs

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from md2html.parser import MarkdownParser
from md2html.converter import HTMLConverter
from md2html.styles import Theme


def handler(request):
    """Handle incoming requests."""
    
    # Serve the homepage
    if request.method == 'GET':
        html_path = Path(__file__).parent.parent / 'templates' / 'index.html'
        with open(html_path, 'r') as f:
            html = f.read()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html
        }
    
    # Handle POST requests for conversion
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            
            markdown_text = body.get('markdown', '')
            theme_name = body.get('theme', 'light')
            include_toc = body.get('includeToc', True)
            title = body.get('title', 'Converted Document')
            fragment_only = body.get('fragmentOnly', False)
            
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
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'html': html,
                    'success': True,
                    'stats': {
                        'headers': len(headers),
                        'tokens': len(tokens)
                    }
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e), 'success': False})
            }
    
    return {
        'statusCode': 405,
        'body': 'Method not allowed'
    }