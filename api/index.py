"""
Vercel Serverless Function for Markdown to HTML Converter
Author: Carlos Crespo
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from md2html.parser import MarkdownParser
from md2html.converter import HTMLConverter
from md2html.styles import Theme


class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Serve the homepage."""
        try:
            html_path = Path(__file__).parent.parent / 'templates' / 'index.html'
            with open(html_path, 'r') as f:
                html = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode())
    
    def do_POST(self):
        """Handle markdown conversion."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            markdown_text = data.get('markdown', '')
            theme_name = data.get('theme', 'light')
            include_toc = data.get('includeToc', True)
            title = data.get('title', 'Converted Document')
            fragment_only = data.get('fragmentOnly', False)
            
            theme = Theme.DARK if theme_name == 'dark' else Theme.LIGHT
            
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
            
            response = json.dumps({
                'html': html,
                'success': True,
                'stats': {
                    'headers': len(headers),
                    'tokens': len(tokens)
                }
            })
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())
            
        except Exception as e:
            response = json.dumps({'error': str(e), 'success': False})
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())