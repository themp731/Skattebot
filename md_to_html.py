#!/usr/bin/env python3
"""
Convert power_rankings_analysis.md to HTML with embedded images.
"""

import markdown
import os
import base64
from pathlib import Path
import re

def image_to_base64(image_path):
    """Convert image file to base64 data URI."""
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        ext = Path(image_path).suffix.lower()
        mime = 'image/png' if ext == '.png' else 'image/jpeg'
        return f'data:{mime};base64,{data}'
    return None

def convert_md_to_html(md_file='power_rankings_analysis.md', output_file='power_rankings_analysis.html'):
    """Convert markdown to HTML with embedded images."""
    
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'nl2br']
    )
    
    image_files = [
        'visualizations/power_rankings.png',
        'visualizations/power_breakdown.png',
        'visualizations/power_rankings_evolution.png',
        'visualizations/wax_leaderboard.png',
        'visualizations/wins_vs_expected.png',
        'visualizations/total_points.png',
        'visualizations/weekly_performance.png',
        'visualizations/weekly_rank_heatmap.png',
        'visualizations/consistency.png',
        'visualizations/monte_carlo_summary.png',
    ]
    
    mc_dir = Path('visualizations/monte_carlo')
    if mc_dir.exists():
        for mc_file in mc_dir.glob('*.png'):
            image_files.append(str(mc_file))
    
    for img_path in image_files:
        if os.path.exists(img_path):
            base64_data = image_to_base64(img_path)
            if base64_data:
                html_content = html_content.replace(
                    f'src="{img_path}"',
                    f'src="{base64_data}"'
                )
                html_content = html_content.replace(
                    f'alt="{img_path}"',
                    f'alt="{Path(img_path).stem}"'
                )
    
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fantasy Football Power Rankings Analysis</title>
    <style>
        :root {{
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-card: #0f3460;
            --text-primary: #eaeaea;
            --text-secondary: #a0a0a0;
            --accent: #e94560;
            --accent-secondary: #0f3460;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #2a2a4a;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            color: var(--text-primary);
            line-height: 1.7;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(15, 52, 96, 0.3);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        }}
        
        h1 {{
            color: var(--accent);
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(233, 69, 96, 0.3);
        }}
        
        h2 {{
            color: var(--text-primary);
            font-size: 1.8em;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--accent);
        }}
        
        h3 {{
            color: var(--accent);
            font-size: 1.4em;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        p {{
            margin-bottom: 15px;
            color: var(--text-secondary);
        }}
        
        strong {{
            color: var(--text-primary);
        }}
        
        em {{
            color: var(--warning);
            font-style: italic;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 15px;
            margin: 25px 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            border: 2px solid var(--border);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(22, 33, 62, 0.6);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        th {{
            background: var(--accent);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: bold;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid var(--border);
            color: var(--text-secondary);
        }}
        
        tr:hover {{
            background: rgba(233, 69, 96, 0.1);
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        code {{
            background: var(--bg-secondary);
            padding: 3px 8px;
            border-radius: 5px;
            font-family: 'Consolas', 'Monaco', monospace;
            color: var(--success);
            font-size: 0.9em;
        }}
        
        pre {{
            background: var(--bg-secondary);
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 20px 0;
            border-left: 4px solid var(--accent);
        }}
        
        pre code {{
            background: none;
            padding: 0;
            color: var(--success);
        }}
        
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            margin: 40px 0;
        }}
        
        ul, ol {{
            margin: 15px 0 15px 30px;
            color: var(--text-secondary);
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        blockquote {{
            border-left: 4px solid var(--accent);
            padding-left: 20px;
            margin: 20px 0;
            color: var(--text-secondary);
            font-style: italic;
        }}
        
        .confidence-interval {{
            background: rgba(46, 204, 113, 0.1);
            border-left: 4px solid var(--success);
            padding: 15px;
            margin: 15px 0;
            border-radius: 0 10px 10px 0;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            h2 {{
                font-size: 1.4em;
            }}
            
            table {{
                font-size: 0.85em;
            }}
            
            th, td {{
                padding: 8px 6px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>'''
    
    with open(output_file, 'w') as f:
        f.write(full_html)
    
    file_size = os.path.getsize(output_file)
    print(f"✓ Created HTML file: {output_file}")
    print(f"  - File size: {file_size / 1024 / 1024:.2f} MB")
    
    mc_count = len(list(Path('visualizations/monte_carlo').glob('*.png'))) if Path('visualizations/monte_carlo').exists() else 0
    print(f"  - Embedded images: {len(image_files)} (including {mc_count} Monte Carlo plots)")
    
    return output_file

if __name__ == '__main__':
    convert_md_to_html()
