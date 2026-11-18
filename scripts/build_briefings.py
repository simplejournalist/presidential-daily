#!/usr/bin/env python3
"""Create source-linked editorial drafts; never publishes or emails automatically."""
import argparse, datetime as dt, json, pathlib, urllib.parse, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
DRAFTS = ROOT / 'drafts'
API = 'https://www.federalregister.gov/api/v1/documents.json'

def documents(day):
    params = [('conditions[presidential_document_type][]', 'executive_order'),
              ('conditions[presidential_document_type][]', 'proclamation'),
              ('conditions[publication_date][gte]', (day - dt.timedelta(days=3)).isoformat()),
              ('conditions[publication_date][lte]', day.isoformat()),
              ('per_page', '40'), ('order', 'newest')]
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent':'PresidentialDailyDraftBot/1.0 (editorial research)'})
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.load(resp)
    return data.get('results', []), url

def daily(day):
    results, search_url = documents(day)
    lines = [f'# Presidential Daily — Daily Briefing — {day:%B %d, %Y}', '',
             '> EDITORIAL DRAFT — NOT FOR PUBLICATION WITHOUT REVIEW', '',
             'This list covers recently published Federal Register presidential documents, not a complete account of presidential activity. Publication dates may differ from signing dates.', '',
             '## Official documents to verify', '']
    if not results:
        lines.append('No matching documents returned in the search window. This does not mean there was no presidential activity.')
    for doc in results[:20]:
        title = doc.get('title', 'Untitled document').replace('\n',' ')
        link = doc.get('html_url') or doc.get('pdf_url') or search_url
        pub = doc.get('publication_date','Date not supplied')
        typ = doc.get('type','Document')
        lines.extend([f'- **{title}** — {typ}; Federal Register publication: {pub}. [Primary record]({link})', ''])
    lines.extend(['## Editor checklist', '- [ ] Open and verify every cited record', '- [ ] Confirm which items belong in today’s briefing and whether they were signed earlier', '- [ ] Check official public schedule and White House announcements separately', '- [ ] Write original, neutral summaries; do not imply this list is comprehensive', '- [ ] Approve before publication or emailing', '', f'Search used: {search_url}', ''])
    out = DRAFTS / 'daily' / f'{day.isoformat()}.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(out.relative_to(ROOT))

def weekly(day):
    start = day - dt.timedelta(days=6)
    daily_files = sorted((DRAFTS/'daily').glob('*.md')) if (DRAFTS/'daily').exists() else []
    matching = [p for p in daily_files if start.isoformat() <= p.stem <= day.isoformat()]
    lines = [f'# Presidential Daily — Weekly Roundup — {start:%B %d}–{day:%B %d, %Y}', '',
             '> EDITORIAL DRAFT — NOT FOR PUBLICATION WITHOUT REVIEW', '',
             '## Daily research drafts available for this week', '']
    if not matching: lines.append('No daily research drafts available. Do not publish an empty roundup.')
    for p in matching:
        lines.append(f'- [{p.stem}](../daily/{p.name})')
    lines += ['', '## Weekly highlights', '', '_Editor: select 3–5 significant, verified developments and write concise original summaries._', '',
              '## Presidential history', '', '_Editor: add one verified historical fact and cite the National Archives or another primary source._', '',
              '## Editor checklist', '- [ ] Check all sources and dates', '- [ ] Remove duplicated developments', '- [ ] Verify every summary and historical fact', '- [ ] Approve before publication or emailing', '']
    out = DRAFTS/'weekly'/f'{day.isoformat()}.md'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text('\n'.join(lines),encoding='utf-8')
    print(out.relative_to(ROOT))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('cadence',choices=['daily','weekly'])
    parser.add_argument('--date',help='UTC date YYYY-MM-DD, defaults to today')
    args=parser.parse_args()
    date=dt.date.fromisoformat(args.date) if args.date else dt.datetime.now(dt.timezone.utc).date()
    (daily if args.cadence=='daily' else weekly)(date)
