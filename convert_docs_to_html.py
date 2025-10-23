import markdown2
from pathlib import Path

# HTML template
html_template = """<!DOCTYPE html>
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .nav-button {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 10px 20px;
            margin: 10px 5px;
            border-radius: 5px;
            text-decoration: none;
            transition: all 0.3s ease;
        }}
        
        .nav-button:hover {{
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }}
        
        .content {{
            padding: 40px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #667eea;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        
        h1 {{ font-size: 2.5em; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        h2 {{ font-size: 2em; border-bottom: 2px solid #667eea; padding-bottom: 8px; }}
        h3 {{ font-size: 1.5em; }}
        
        p {{
            margin: 1em 0;
        }}
        
        ul, ol {{
            margin: 1em 0;
            padding-left: 2em;
        }}
        
        li {{
            margin: 0.5em 0;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1em 0;
        }}
        
        pre code {{
            background: none;
            padding: 0;
            color: #e2e8f0;
        }}
        
        blockquote {{
            border-left: 4px solid #667eea;
            padding: 10px 20px;
            margin: 1em 0;
            background: #f8f9fa;
            font-style: italic;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        tr:hover {{
            background: #f7fafc;
        }}
        
        a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1em 0;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 5px;
        }}
        
        .badge-success {{
            background: #48bb78;
            color: white;
        }}
        
        .badge-info {{
            background: #4299e1;
            color: white;
        }}
        
        .badge-warning {{
            background: #ed8936;
            color: white;
        }}
        
        .footer {{
            background: #2d3748;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 40px;
        }}
        
        .back-to-home {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 50px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .back-to-home:hover {{
            background: #764ba2;
            transform: scale(1.05);
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .back-to-home {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div style="margin-top: 20px;">
                <a href="../demodocs.html" class="nav-button">🏠 Home</a>
                <a href="readme.html" class="nav-button">📖 Main README</a>
            </div>
        </div>
        
        <div class="content">
            {content}
        </div>
        
        <div class="footer">
            <p>Week 3 Multi-Agent System - AI Agent Bootcamp</p>
            <p style="margin-top: 10px;">
                <span class="badge badge-success">✅ Complete</span>
                <span class="badge badge-info">📚 Documented</span>
                <span class="badge badge-warning">🎬 Ready to Demo</span>
            </p>
        </div>
    </div>
    
    <a href="../demodocs.html" class="back-to-home">🏠 Back to Home</a>
</body>
</html>
"""

def convert_md_to_html(md_file_path, output_dir):
    """Convert a markdown file to HTML"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'tables', 'break-on-newline'])
    
    # Get title from filename
    filename = Path(md_file_path).stem
    title = filename.replace('_', ' ').replace('-', ' ').title()
    
    # Create full HTML
    full_html = html_template.format(title=title, content=html_content)
    
    # Save to output directory
    output_filename = filename.lower() + '.html'
    output_path = Path(output_dir) / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ Converted: {filename} -> {output_filename}")
    return output_filename, title

# Main execution
if __name__ == "__main__":
    # Setup paths
    base_dir = Path(__file__).parent
    demo_docs_dir = base_dir / "week3" / "docs" / "demo"
    output_dir = base_dir / "html"
    readme_path = base_dir / "week3" / "README.md"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    print("🔄 Converting demo documentation to HTML...\n")
    
    # Convert all demo markdown files
    demo_files = []
    for md_file in sorted(demo_docs_dir.glob("*.md")):
        filename, title = convert_md_to_html(md_file, output_dir)
        demo_files.append((filename, title))
    
    print("\n🔄 Converting main README...\n")
    
    # Convert main README
    readme_filename, readme_title = convert_md_to_html(readme_path, output_dir)
    
    print("\n✅ All conversions complete!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📄 Total files created: {len(demo_files) + 1}")
