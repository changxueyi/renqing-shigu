#!/usr/bin/env python3
"""从 book/*.md 生成 README.md 的目录和统计。静态文字在 tools/readme_head.md 与 tools/readme_tail.md。"""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def read(p):
    return open(os.path.join(ROOT, p), encoding='utf-8').read() if os.path.exists(os.path.join(ROOT, p)) else ''
files = sorted(glob.glob(os.path.join(ROOT, 'book', '*.md')))
toc, total, grades = [], 0, {'A': 0, 'B': 0, 'C': 0}
for f in files:
    s = open(f, encoding='utf-8').read()
    m = re.search(r'^# (\d+)\. (.+)$', s, re.M)
    n = len(re.findall(r'^### \d+\. ', s, re.M)); total += n
    for g in re.findall(r'^- 证据等级：([ABC])', s, re.M): grades[g] += 1
    titles = re.findall(r'^### \d+\. (.+)$', s, re.M)
    rel = 'book/' + os.path.basename(f)
    toc.append(f"{m.group(1)}. [{m.group(2)}]({rel})（{n} 条）")
head = read('tools/readme_head.md').replace('{{TOTAL}}', str(total)).replace('{{CHAPTERS}}', str(len(files)))
for g, c in grades.items(): head = head.replace('{{' + g + '}}', str(c))
tail = read('tools/readme_tail.md')
out = head.rstrip() + '\n\n## 目录\n\n' + '\n'.join(toc) + '\n\n## 正文\n\n正文在 [book/](book/) 目录下，每章一个文件。\n\n' + tail.strip() + '\n'
open(os.path.join(ROOT, 'README.md'), 'w', encoding='utf-8').write(out)
print(f'{len(files)} 章，{total} 条')
