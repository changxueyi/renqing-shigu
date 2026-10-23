#!/usr/bin/env python3
"""从 book/*.md 抽取每条的「怎么说」，生成 docs/话术速查.md。开头的万能句式在 tools/phrasebook_head.md。"""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
head = open(os.path.join(ROOT, 'tools', 'phrasebook_head.md'), encoding='utf-8').read().rstrip()
out, total = [head, ''], 0
for f in sorted(glob.glob(os.path.join(ROOT, 'book', '*.md'))):
    s = open(f, encoding='utf-8').read()
    chap = re.search(r'^# (\d+)\. (.+)$', s, re.M)
    items = []
    for part in re.split(r'^### ', s, flags=re.M)[1:]:
        m = re.match(r'(\d+)\. (.+)', part)
        say = re.search(r'^- 怎么说：(.+)$', part, re.M)
        if m and say:
            items.append(f'- {say.group(1).strip()}（第 {chap.group(1)} 章第 {m.group(1)} 条：{m.group(2).strip()}）')
    if not items:
        continue
    total += len(items)
    out.append(f'### 第 {chap.group(1)} 章 {chap.group(2)}')
    out.append('')
    out.extend(items)
    out.append('')
open(os.path.join(ROOT, 'docs', '话术速查.md'), 'w', encoding='utf-8').write('\n'.join(out).rstrip() + '\n')
print(f'话术 {total} 条')
