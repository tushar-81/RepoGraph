import pdfkit
import markdown as md_converter
from pathlib import Path

def save_as_pdf(tutorial_text: str):
    html_content = md_converter.markdown(
        tutorial_text,
        extensions=['fenced_code', 'tables', 'codehilite']
    )

    # wkhtmltopdf can't paint page margins, so a full-bleed dark PDF leaves white bands on every page.
    # The document is light with the brand carried by a dark masthead and dark code blocks.
    styled_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700;800&display=swap');

            * {{ margin: 0; padding: 0; box-sizing: border-box; }}

            body {{
                background: #ffffff;
                color: #44403c;
                font-family: 'Geist', 'Segoe UI', Arial, sans-serif;
                font-size: 12.5px;
                line-height: 1.75;
            }}

            /* Masthead — tables, since wkhtmltopdf has no flexbox */
            .masthead {{
                background: #1c1917;
                border-radius: 6px;
                padding: 14px 18px;
                margin-bottom: 36px;
            }}

            .masthead table {{ width: 100%; border-collapse: collapse; margin: 0; }}
            .masthead td {{ border: none; padding: 0; vertical-align: middle; color: inherit; }}
            .masthead .mark {{ width: 44px; }}
            .masthead .mark svg {{ display: block; }}

            .wordmark {{
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 18px;
                font-weight: 800;
                letter-spacing: -0.04em;
                color: #fafaf9;
                line-height: 1.2;
            }}

            .wordmark span {{ color: #ea580c; }}

            .wordmark-sub, .doc-kind {{
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 8.5px;
                font-weight: 500;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: #78716c;
            }}

            .doc-kind {{ text-align: right; color: #a8a29e; }}
            .doc-kind b {{ color: #ea580c; font-weight: 500; }}

            /* Headings */
            h1 {{
                font-size: 24px;
                font-weight: 700;
                color: #1c1917;
                letter-spacing: -0.02em;
                line-height: 1.25;
                margin: 32px 0 14px;
            }}

            h2 {{
                font-size: 17px;
                font-weight: 650;
                color: #1c1917;
                letter-spacing: -0.01em;
                line-height: 1.3;
                margin: 30px 0 12px;
                padding-bottom: 6px;
                border-bottom: 1px solid #e7e5e4;
                page-break-after: avoid;
            }}

            h3 {{
                font-size: 14px;
                font-weight: 600;
                color: #1c1917;
                margin: 22px 0 8px;
                page-break-after: avoid;
            }}

            h4, h5, h6 {{
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 10px;
                font-weight: 500;
                color: #78716c;
                margin: 16px 0 8px;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            }}

            h1:first-child {{ margin-top: 0; }}

            /* Paragraphs */
            p {{ margin-bottom: 12px; }}
            strong {{ color: #1c1917; font-weight: 600; }}

            /* Inline code */
            code {{
                background: #f5f5f4;
                border: 1px solid #e7e5e4;
                color: #1c1917;
                padding: 1px 5px;
                border-radius: 3px;
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 10.5px;
            }}

            /* Code blocks — dark, like the app */
            pre {{
                background: #1c1917;
                border: 1px solid #292524;
                border-radius: 4px;
                padding: 14px 16px;
                margin: 16px 0;
                overflow-x: auto;
                page-break-inside: avoid;
            }}

            pre code {{
                background: none;
                border: none;
                padding: 0;
                color: #e7e5e4;
                font-size: 10.5px;
                line-height: 1.65;
            }}

            /* Syntax highlighting (stone + orange) */
            .codehilite {{ background: #1c1917 !important; }}
            .codehilite .k, .codehilite .kn, .codehilite .kd, .codehilite .kc, .codehilite .nd {{ color: #fb923c; }}
            .codehilite .s, .codehilite .s1, .codehilite .s2, .codehilite .sd {{ color: #fcd34d; }}
            .codehilite .mi, .codehilite .mf {{ color: #fcd34d; }}
            .codehilite .n  {{ color: #e7e5e4; }}
            .codehilite .o, .codehilite .p {{ color: #a8a29e; }}
            .codehilite .c, .codehilite .c1, .codehilite .cm {{ color: #78716c; font-style: italic; }}
            .codehilite .nf, .codehilite .nc {{ color: #fafaf9; font-weight: 700; }}
            .codehilite .nb, .codehilite .bp {{ color: #fdba74; }}

            /* Lists */
            ul, ol {{ padding-left: 22px; margin-bottom: 12px; }}
            li {{ margin-bottom: 5px; padding-left: 3px; }}

            /* Blockquotes */
            blockquote {{
                border-left: 2px solid #ea580c;
                padding: 8px 16px;
                margin: 16px 0;
                background: #fafaf9;
                color: #57534e;
            }}

            blockquote p {{ margin-bottom: 0; }}

            /* Tables */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 18px 0;
                font-size: 11.5px;
            }}

            th {{
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 9.5px;
                font-weight: 500;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #78716c;
                text-align: left;
                padding: 8px 12px 8px 0;
                border-bottom: 1px solid #d6d3d1;
            }}

            td {{
                padding: 8px 12px 8px 0;
                border-bottom: 1px solid #e7e5e4;
            }}

            tr {{ page-break-inside: avoid; }}

            /* Horizontal rule */
            hr {{
                border: none;
                border-top: 1px solid #e7e5e4;
                margin: 28px 0;
            }}

            /* Links */
            a {{
                color: #c2410c;
                text-decoration: none;
                border-bottom: 1px solid #fed7aa;
            }}

            /* Footer */
            .doc-footer {{
                width: 100%;
                border-collapse: collapse;
                margin: 48px 0 0;
            }}

            .doc-footer td {{
                padding: 12px 0 0;
                border: none;
                border-top: 1px solid #e7e5e4;
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 8.5px;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: #a8a29e;
            }}

            .doc-footer .doc-footer-right {{ text-align: right; }}
        </style>
    </head>
    <body>
        <div class="masthead">
            <table><tr>
                <td class="mark">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="8 8 64 64">
                        <rect x="8" y="8" width="64" height="64" rx="16" fill="#292524"/>
                        <path d="M24 20 H46 L56 30 V58 C56 60.2 54.2 62 52 62 H24 C21.8 62 20 60.2 20 58 V24 C20 21.8 21.8 20 24 20 Z" fill="none" stroke="#57534E" stroke-width="2"/>
                        <path d="M46 20 V30 H56" fill="none" stroke="#57534E" stroke-width="2" stroke-linejoin="round"/>
                        <path d="M30 28 V52" stroke="#EA580C" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M30 36 C36 36, 38 40, 44 40" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M44 40 V50" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M41 48 L44 52 L47 48" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="30" cy="28" r="3.5" fill="#FAFAF9" stroke="#EA580C" stroke-width="2"/>
                        <circle cx="30" cy="36" r="3.5" fill="#FAFAF9" stroke="#EA580C" stroke-width="2"/>
                        <circle cx="30" cy="52" r="3.5" fill="#EA580C"/>
                        <circle cx="44" cy="40" r="3.5" fill="#F59E0B"/>
                    </svg>
                </td>
                <td>
                    <div class="wordmark">Repo<span>Graph</span></div>
                    <div class="wordmark-sub">Code analyzer &amp; docs</div>
                </td>
                <td class="doc-kind"><b>&#9632;</b> Repository analysis</td>
            </tr></table>
        </div>

        {html_content}

        <table class="doc-footer"><tr>
            <td>Generated by RepoGraph</td>
            <td class="doc-footer-right">Code analyzer &amp; docs</td>
        </tr></table>
    </body>
    </html>
    """

    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    )

    pdf_bytes=pdfkit.from_string(
        styled_html,
        False,
        configuration=config,
        options={
            'encoding': 'UTF-8',
            'enable-local-file-access': None,
            'background': None,           # renders background colors
            'print-media-type': None,
            'page-size': 'A4',
            'margin-top': '16mm',         # white page, so real margins keep text off the edge on every page
            'margin-bottom': '16mm',
            'margin-left': '16mm',
            'margin-right': '16mm',
        }
    )
    return pdf_bytes
