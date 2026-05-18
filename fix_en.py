"""
WooaSheet EN 페이지 및 KO 도구 페이지 헤더 수정 스크립트
- EN pages: <header> → <header class="header">, <nav> → <nav class="nav">, lang-btn → lang-switcher, + GA
- KO tool pages: add lang-switcher (KO active | EN)
"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

GA_TAG = ('<script async src="https://www.googletagmanager.com/gtag/js?id=G-9ZGENFSXWC"></script>\n'
          '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-9ZGENFSXWC\');</script>\n')

ADSENSE_TAG = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6464921081676309" crossorigin="anonymous"></script>\n'

# EN 파일 목록: (파일명, KO href, EN href)
EN_FILES = [
    ('en/index.html',        '../index.html',        'index.html'),
    ('en/csv-excel.html',    '../csv-excel.html',    'csv-excel.html'),
    ('en/chart.html',        '../chart.html',        'chart.html'),
    ('en/editor.html',       '../editor.html',       'editor.html'),
    ('en/deduplicate.html',  '../deduplicate.html',  'deduplicate.html'),
    ('en/merge-csv.html',    '../merge-csv.html',    'merge-csv.html'),
    ('en/split-csv.html',    '../split-csv.html',    'split-csv.html'),
]

def fix_en_page(relpath, ko_href, en_href):
    path = os.path.join(BASE, relpath.replace('/', os.sep))
    with open(path, encoding='utf-8') as f:
        html = f.read()

    changed = []

    # 1. Add GA tag after <head> (if missing)
    if 'G-9ZGENFSXWC' not in html:
        html = html.replace('<head>\n', '<head>\n' + GA_TAG, 1)
        if 'G-9ZGENFSXWC' not in html:
            # try without newline
            html = html.replace('<head>', '<head>\n' + GA_TAG, 1)
        changed.append('GA tag')

    # 2. Add AdSense (if missing)
    if 'ca-pub-6464921081676309' not in html:
        # Insert before </head>
        html = html.replace('</head>', ADSENSE_TAG + '</head>', 1)
        changed.append('AdSense')

    # 3. Fix <header> → <header class="header">
    # Only replace bare <header> (not already classed)
    html = re.sub(r'<header(?!\s+class)', '<header class="header"', html)
    changed.append('header class')

    # 4. Fix <nav> → <nav class="nav">
    html = re.sub(r'<nav(?!\s+class)', '<nav class="nav"', html)
    changed.append('nav class')

    # 5. Fix lang-btn → lang-switcher
    lang_switcher = (
        f'<div class="lang-switcher">\n'
        f'      <a href="{ko_href}">KO</a>\n'
        f'      <span>|</span>\n'
        f'      <a href="{en_href}" class="active">EN</a>\n'
        f'    </div>'
    )
    # Replace entire header-right content
    html = re.sub(
        r'<div class="header-right">\s*<a[^>]+class="lang-btn"[^>]*>[^<]*</a>\s*</div>',
        f'<div class="header-right">\n      {lang_switcher}\n    </div>',
        html
    )
    # Simpler fallback pattern
    html = re.sub(
        r'<a\s+href="[^"]*"\s+class="lang-btn">[^<]*</a>',
        f'<div class="lang-switcher"><a href="{ko_href}">KO</a><span>|</span><a href="{en_href}" class="active">EN</a></div>',
        html
    )
    changed.append('lang-switcher')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK {relpath}: {", ".join(changed)}')

# KO 도구 페이지 목록: (파일명, 현재파일, EN 경로)
KO_TOOL_FILES = [
    ('csv-excel.html',   'csv-excel.html',   'en/csv-excel.html'),
    ('chart.html',       'chart.html',       'en/chart.html'),
    ('editor.html',      'editor.html',      'en/editor.html'),
    ('deduplicate.html', 'deduplicate.html', 'en/deduplicate.html'),
    ('merge-csv.html',   'merge-csv.html',   'en/merge-csv.html'),
    ('split-csv.html',   'split-csv.html',   'en/split-csv.html'),
]

def fix_ko_tool_page(relpath, ko_href, en_href):
    path = os.path.join(BASE, relpath.replace('/', os.sep))
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # Check if already has lang-switcher HTML element (not just CSS definition)
    if '<div class="lang-switcher">' in html:
        # Fix active state if needed - skip if already correct
        print(f'  SKIP  {relpath}: lang-switcher already exists, skipping')
        return

    # Add header-right with KO active lang-switcher before </nav></div></header>
    lang_html = (
        f'<div class="header-right">'
        f'<div class="lang-switcher">'
        f'<a href="{ko_href}" class="active">KO</a>'
        f'<span>|</span>'
        f'<a href="{en_href}">EN</a>'
        f'</div></div>'
    )

    # The KO tool pages have minified header ending with </nav></div></header>
    # We need to insert header-right between </nav> and </div></header>
    if '</nav></div></header>' in html:
        html = html.replace('</nav></div></header>',
                            f'</nav>{lang_html}</div></header>', 1)
        print(f'  OK {relpath}: added KO lang-switcher (minified)')
    elif '</nav>\n  </div>\n</header>' in html:
        html = html.replace('</nav>\n  </div>\n</header>',
                            f'</nav>\n    {lang_html}\n  </div>\n</header>', 1)
        print(f'  OK {relpath}: added KO lang-switcher (pretty)')
    else:
        # Generic: insert before </div></header>
        html = re.sub(
            r'(</nav>)(\s*</div>\s*</header>)',
            rf'\1\n    {lang_html}\2',
            html, count=1
        )
        print(f'  OK {relpath}: added KO lang-switcher (regex)')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print('=== Fixing EN pages ===')
for relpath, ko_href, en_href in EN_FILES:
    fix_en_page(relpath, ko_href, en_href)

print('\n=== Fixing KO tool pages ===')
for relpath, ko_href, en_href in KO_TOOL_FILES:
    fix_ko_tool_page(relpath, ko_href, en_href)

print('\nDone!')
