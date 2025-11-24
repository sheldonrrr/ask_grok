#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tutorial Viewer Module

Converts markdown tutorial to HTML and displays it in a local web browser.
Simple, lightweight, no external dependencies beyond PyQt5.
"""

import os
import re
import tempfile
import webbrowser
from pathlib import Path


class MarkdownToHTMLConverter:
    """Simple markdown to HTML converter for tutorial display"""
    
    def __init__(self):
        self.html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 2.5em;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 15px;
            font-size: 2em;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        
        h3 {{
            color: #555;
            margin-top: 30px;
            margin-bottom: 12px;
            font-size: 1.5em;
        }}
        
        h4 {{
            color: #666;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", Courier, monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin-bottom: 15px;
        }}
        
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 20px 0;
            color: #555;
            font-style: italic;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        
        em {{
            font-style: italic;
            color: #555;
        }}
        
        .toc {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        
        .toc h2 {{
            margin-top: 0;
            font-size: 1.5em;
            border: none;
        }}
        
        .toc ul {{
            list-style: none;
            margin-left: 0;
        }}
        
        .toc li {{
            margin-bottom: 5px;
        }}
        
        .back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #3498db;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            text-decoration: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: background 0.3s;
        }}
        
        .back-to-top:hover {{
            background: #2980b9;
            text-decoration: none;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            h2 {{
                font-size: 1.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    <a href="#" class="back-to-top">↑ Top</a>
</body>
</html>
"""
    
    def convert(self, markdown_text):
        """Convert markdown to HTML"""
        html = markdown_text
        
        # Escape HTML entities first
        # html = html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        
        # Horizontal rules
        html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Inline code
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)
        
        # Lists - unordered
        lines = html.split('\n')
        in_ul = False
        result = []
        
        for i, line in enumerate(lines):
            # Check for unordered list
            if re.match(r'^- (.+)$', line):
                if not in_ul:
                    result.append('<ul>')
                    in_ul = True
                content = re.sub(r'^- (.+)$', r'\1', line)
                result.append(f'<li>{content}</li>')
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                result.append(line)
        
        if in_ul:
            result.append('</ul>')
        
        html = '\n'.join(result)
        
        # Ordered lists
        lines = html.split('\n')
        in_ol = False
        result = []
        
        for line in lines:
            if re.match(r'^\d+\. (.+)$', line):
                if not in_ol:
                    result.append('<ol>')
                    in_ol = True
                content = re.sub(r'^\d+\. (.+)$', r'\1', line)
                result.append(f'<li>{content}</li>')
            else:
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)
        
        if in_ol:
            result.append('</ol>')
        
        html = '\n'.join(result)
        
        # Paragraphs
        lines = html.split('\n')
        result = []
        in_p = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip if it's already an HTML tag
            if stripped.startswith('<') or stripped == '':
                if in_p:
                    result.append('</p>')
                    in_p = False
                result.append(line)
            else:
                if not in_p:
                    result.append('<p>')
                    in_p = True
                result.append(line)
        
        if in_p:
            result.append('</p>')
        
        html = '\n'.join(result)
        
        return html
    
    def create_html_file(self, markdown_file_path):
        """Create HTML file from markdown file"""
        try:
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Extract title from first line
            title_match = re.match(r'^# (.+)$', markdown_content, re.MULTILINE)
            title = title_match.group(1) if title_match else "Ask AI Plugin Tutorial"
            
            # Convert markdown to HTML
            html_content = self.convert(markdown_content)
            
            # Create full HTML
            full_html = self.html_template.format(
                title=title,
                content=html_content
            )
            
            # Create temporary HTML file
            temp_dir = tempfile.gettempdir()
            html_file_path = os.path.join(temp_dir, 'ask_ai_plugin_tutorial.html')
            
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            return html_file_path
            
        except Exception as e:
            raise Exception(f"Failed to create HTML file: {str(e)}")


def open_tutorial_in_browser():
    """Open the tutorial in the default web browser"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # When running as a calibre plugin, files are in a zip
        # We need to read the file content directly
        tutorial_content = None
        
        # Try to get the tutorial content using calibre's get_resources
        try:
            from calibre.utils.zipfile import ZipFile
            import sys
            
            # Find the plugin zip file
            plugin_path = None
            for path in sys.path:
                if 'Ask AI Plugin.zip' in path or 'ask_grok' in path:
                    if os.path.exists(path) and path.endswith('.zip'):
                        plugin_path = path
                        break
            
            if plugin_path:
                logger.info(f"Found plugin zip: {plugin_path}")
                with ZipFile(plugin_path, 'r') as zf:
                    # Try to read the tutorial file from zip
                    tutorial_name = 'tutorial/tutorial_v0.3_for_Ask_AI_Plugin_v1.3.3.md'
                    if tutorial_name in zf.namelist():
                        tutorial_content = zf.read(tutorial_name).decode('utf-8')
                        logger.info(f"Read tutorial from zip: {len(tutorial_content)} bytes")
                    else:
                        logger.error(f"Tutorial not found in zip. Available files: {zf.namelist()[:10]}")
        except Exception as e:
            logger.warning(f"Could not read from zip: {e}")
        
        # Fallback: try direct file access (for development)
        if not tutorial_content:
            plugin_dir = Path(__file__).parent
            tutorial_file = plugin_dir / 'tutorial' / 'tutorial_v0.3_for_Ask_AI_Plugin_v1.3.3.md'
            
            if tutorial_file.exists():
                with open(tutorial_file, 'r', encoding='utf-8') as f:
                    tutorial_content = f.read()
                logger.info(f"Read tutorial from file: {tutorial_file}")
            else:
                raise FileNotFoundError(f"Tutorial file not found: {tutorial_file}")
        
        if not tutorial_content:
            raise Exception("Could not load tutorial content")
        
        # Convert to HTML
        converter = MarkdownToHTMLConverter()
        
        # Extract title from first line
        import re
        title_match = re.match(r'^# (.+)$', tutorial_content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Ask AI Plugin Tutorial"
        
        # Convert markdown to HTML
        html_content = converter.convert(tutorial_content)
        
        # Create full HTML
        full_html = converter.html_template.format(
            title=title,
            content=html_content
        )
        
        # Create temporary HTML file
        temp_dir = tempfile.gettempdir()
        html_file_path = os.path.join(temp_dir, 'ask_ai_plugin_tutorial.html')
        
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        logger.info(f"Created HTML file: {html_file_path}")
        
        # Open in browser
        webbrowser.open(f'file://{html_file_path}')
        
        return True
        
    except Exception as e:
        logger.error(f"Error opening tutorial: {str(e)}")
        print(f"Error opening tutorial: {str(e)}")
        return False


if __name__ == '__main__':
    # Test the converter
    open_tutorial_in_browser()
