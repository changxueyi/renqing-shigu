#!/usr/bin/env python3
"""从 book/*.md 汇总每章 A、B 级条目的来源，生成 docs/核实记录/依据清单.md，方便逐条复核。"""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = ['# 依据清单', '', '[← 回核实记录](README.md)', '',
       '按章节列出 A 级（法律法规、官方文件）和 B 级（学术研究、权威著作）条目的来源，由 tools/build_sources.py 从正文自动生成。C 级为经验共识，不在此列。', '']
count = {'A': 0, 'B': 0, 'C': 0}
for f in sorted(glob.glob(os.path.join(ROOT, 'book', '*.md'))):
    s = open(f, encoding='utf-8').read()
    chap = re.search(r'^# (\d+)\. (.+)$', s, re.M)
    rows = []
    for part in re.split(r'^### ', s, flags=re.M)[1:]:
        m = re.match(r'(\d+)\. (.+)', part)
        g = re.search(r'^- 证据等级：(\S+)', part, re.M)
        src = re.search(r'^- 来源：(.+)$', part, re.M)
        if not (m and g and src):
            continue
        grade = g.group(1)
        count[grade] = count.get(grade, 0) + 1
        if grade in ('A', 'B'):
            rows.append(f'| {m.group(1)} | {grade} | {m.group(2).strip()} | {src.group(1).strip()} |')
    if rows:
        out += [f'## 第 {chap.group(1)} 章 {chap.group(2)}', '', '| 条 | 等级 | 条目 | 来源 |', '| --- | --- | --- | --- |'] + rows + ['']
out.insert(6, f'全书 A 级 {count["A"]} 条、B 级 {count["B"]} 条、C 级 {count["C"]} 条。')
out.insert(7, '')
path = os.path.join(ROOT, 'docs', '核实记录', '依据清单.md')
open(path, 'w', encoding='utf-8').write('\n'.join(out).rstrip() + '\n')
print('A', count['A'], 'B', count['B'], 'C', count['C'])
