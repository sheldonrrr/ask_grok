#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tutorial Viewer - Simple markdown to HTML converter
"""

import os
import re
import tempfile
import webbrowser
from pathlib import Path


class MarkdownToHTMLConverter:
    """Simple markdown to HTML converter"""
    
    def __init__(self):
        self.html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{ margin-top: 30px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        h2 {{ margin-top: 25px; border-bottom: 1px solid #666; padding-bottom: 8px; }}
        h3 {{ margin-top: 20px; }}
        code {{ background: #f4f4f4; padding: 2px 5px; font-family: monospace; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        pre code {{ background: none; padding: 0; }}
        ul, ol {{ margin-left: 25px; }}
        li {{ margin-bottom: 5px; }}
        blockquote {{ border-left: 3px solid #666; padding-left: 15px; margin: 15px 0; color: #666; }}
        a {{ color: #333; }}
    </style>
</head>
<body>
    {content}
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
        # Get plugin instance to use get_resources
        from calibre.customize.ui import find_plugin
        plugin = find_plugin('Ask AI Plugin')
        
        if not plugin:
            logger.error("Plugin not found")
            return False
        
        # Read tutorial using plugin's get_resources method
        tutorial_data = plugin.get_resources('tutorial/tutorial_v0.3_for_Ask_AI_Plugin_v1.3.3.md')
        
        if not tutorial_data:
            logger.error("Failed to read tutorial")
            return False
        
        tutorial_content = tutorial_data.decode('utf-8')
        logger.info(f"Read tutorial: {len(tutorial_content)} bytes")
        
        # Convert to HTML
        converter = MarkdownToHTMLConverter()
        
        # Extract title
        title_match = re.match(r'^# (.+)$', tutorial_content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Ask AI Plugin Tutorial"
        
        # Convert markdown to HTML
        html_content = converter.convert(tutorial_content)
        
        # Create full HTML
        full_html = converter.html_template.format(
            title=title,
            content=html_content
        )
        
        # Create temporary HTML file using calibre's temp directory
        from calibre.ptempfile import PersistentTemporaryFile
        
        # Create a persistent temp file that won't be deleted immediately
        with PersistentTemporaryFile(suffix='.html', prefix='ask_ai_plugin_tutorial_') as f:
            f.write(full_html.encode('utf-8'))
            html_file_path = f.name
        
        logger.info(f"Created HTML: {html_file_path}")
        
        # Open in browser
        webbrowser.open(f'file://{html_file_path}')
        
        return True
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False


if __name__ == '__main__':
    # Test the converter
    open_tutorial_in_browser()
