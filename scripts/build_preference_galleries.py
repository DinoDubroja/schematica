"""Build marked preference galleries; --check validates without writing.

Standard library only. Authoring contract: agents/PROJECT_RULES.md.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import html
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit

MARKDOWN_LINK = re.compile(r'(!?\[[^\]\n]*\]\()(<[^>\n]+>|[^\s)]+)([^)\n]*\))')
HTML_LINK = re.compile(r'(\b(?:href|src)\s*=\s*)([\"\x27])(.*?)(\2)', re.I)
GALLERY_START = re.compile(r'<!-- preference-gallery:start level=([2-5]) -->')
GALLERY_END = '<!-- preference-gallery:end -->'
REPRESENTATIVE = re.compile(r'<!-- preference-representative: ([^\n]+?) -->')
THEME = {'gh-light-mode-only', 'gh-dark-mode-only'}


class GalleryError(ValueError):
    pass


def read(path: Path) -> str:
    # Preserve authored CRLF outside generated sections.
    return path.read_bytes().decode('utf-8')


def region(text: str, name: str) -> tuple[int, int]:
    start, end = f'<!-- preference-{name}:start -->', f'<!-- preference-{name}:end -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise GalleryError(f'Expected one {name} marker pair')
    a, b = text.index(start) + len(start), text.index(end)
    if b < a:
        raise GalleryError(f'Reversed {name} markers')
    return a, b


def section(text: str, name: str) -> str:
    a, b = region(text, name)
    return text[a:b].strip().replace('\r\n', '\n')


def title(text: str) -> str:
    matches = re.findall(r'^# (.+?)\s*$', text, re.M)
    if len(matches) != 1:
        raise GalleryError('Expected exactly one level-one title')
    return matches[0]


def refs(text: str) -> list[str]:
    # Code and comments are documentation, not links.
    text = re.sub(r'```.*?```|~~~.*?~~~|<!--.*?-->|`[^`\n]+`', '', text, flags=re.S)
    return [m[1].strip('<>') for m in MARKDOWN_LINK.findall(text)] + [m[2] for m in HTML_LINK.findall(text)]


def local_target(url: str, source: Path) -> tuple[Path, str] | None:
    parts = urlsplit(html.unescape(url))
    if parts.scheme or parts.netloc:
        return None
    if parts.path.startswith('/'):
        raise GalleryError(f'{source}: use repository-relative links: {url}')
    return (source.parent / unquote(parts.path)).resolve() if parts.path else source, unquote(parts.fragment)


def rebase(url: str, source: Path, destination: Path) -> str:
    target = local_target(url, source)
    if target is None:
        return url
    path, _ = target
    parts = urlsplit(html.unescape(url))
    relative = quote(Path(os.path.relpath(path, destination.parent)).as_posix(), safe='/._-~')
    if parts.path.endswith('/'):
        relative += '/'
    return html.escape(urlunsplit(('', '', relative, parts.query, parts.fragment)), quote=True)


def rewrite(text: str, source: Path, destination: Path) -> str:
    text = MARKDOWN_LINK.sub(lambda m: m[1] + rebase(m[2].strip('<>'), source, destination) + m[3], text)
    return HTML_LINK.sub(lambda m: m[1] + m[2] + rebase(m[3], source, destination) + m[4], text)


def anchors(text: str) -> set[str]:
    result = set(re.findall(r'\b(?:id|name)=[\"\x27]([^\"\x27]+)', text))
    counts: dict[str, int] = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        # GitHub omits image alt text when generating heading anchors.
        heading = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', heading)
        heading = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', heading)
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug + (f'-{n}' if n else ''))
    return result


@dataclass
class Rule:
    readme: Path
    visual: str
    good: str


class Builder:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.originals: dict[Path, str] = {}
        self.outputs: dict[Path, str] = {}
        self.rules: dict[Path, Rule] = {}
        self.ids: set[str] = set()

    def load(self, path: Path) -> str:
        if not path.is_file():
            raise GalleryError(f'Missing file: {path}')
        if path not in self.originals:
            self.originals[path] = read(path)
        return self.originals[path]

    def check_links(self, path: Path, text: str) -> None:
        for url in refs(text):
            target = local_target(url, path)
            if target is None:
                continue
            file, fragment = target
            if not file.is_relative_to(self.root):
                raise GalleryError(f'{path}: reference leaves repository: {url}')
            if not file.exists():
                raise GalleryError(f'{path}: missing reference: {url}')
            if file.is_dir():
                file = file / 'README.md'
                if not file.is_file():
                    raise GalleryError(f'{path}: directory has no README: {url}')
            if fragment and fragment not in THEME and file.suffix.lower() == '.md':
                content = self.outputs.get(file, self.load(file))
                if fragment not in anchors(content):
                    raise GalleryError(f'{path}: missing anchor: {url}')

    def rule(self, folder: Path) -> Rule | None:
        record = folder / 'RULE.md'
        content = self.load(record)
        fields = {}
        for key in ('ID', 'Status'):
            values = re.findall(rf'^{key}: ([^\r\n]+)\r?$', content, re.M)
            if len(values) != 1:
                raise GalleryError(f'{record}: expected one {key} field')
            fields[key] = values[0].strip()
        if fields['ID'] in self.ids:
            raise GalleryError(f'{record}: duplicate ID {fields["ID"]}')
        self.ids.add(fields['ID'])
        if fields['Status'] not in {'accepted', 'proposed', 'deferred', 'rejected', 'superseded'}:
            raise GalleryError(f'{record}: unknown status')
        if fields['Status'] != 'accepted':
            return None
        page = folder / 'README.md'
        visual = section(self.load(page), 'visual')
        title(visual)
        if re.search(r'```|~~~|\]\[|^\s*\[[^\]]+\]:', visual, re.M):
            raise GalleryError(f'{page}: unsupported code fence or reference-style link in visual section')
        good = section(visual, 'good')
        examples = []
        if '<!-- preference-variants:start -->' in visual:
            raise GalleryError(f'{page}: place accepted variants inside the Good column of a Good/Bad comparison')
        if '<!-- preference-comparison:start -->' in visual:
            comparison = section(visual, 'comparison')
            rows = re.findall(r'<tr>\s*(.*?)\s*</tr>', comparison, re.S)
            cells = [re.findall(r'<t[hd]\b[^>]*>(.*?)</t[hd]>', row, re.S) for row in rows]
            if len(cells) != 4 or any(len(row) != 2 for row in cells):
                raise GalleryError(f'{page}: comparison needs four rows of two columns: labels, images, captions, downloads')
            for index, label in enumerate(('Good', 'Bad')):
                match = re.fullmatch(r'\s*<img src="([^"]+)" alt="' + label + r'">\s*', cells[0][index])
                if not match:
                    raise GalleryError(f'{page}: comparison must place Good left and Bad right')
                preview = section(visual, label.lower())
                if preview not in cells[1][index]:
                    raise GalleryError(f'{page}: {label} preview must be in its image column')
                examples.append((label, match[1], '\n'.join(row[index] for row in cells)))
        else:
            single = re.split(r'^## ', visual, flags=re.M)[1:]
            if len(single) != 1:
                raise GalleryError(f'{page}: use one Good section or a side-by-side comparison table')
            example = single[0]
            heading = example.splitlines()[0].strip()
            match = re.fullmatch(r'!\[Good\]\(([^)]+)\)', heading)
            if not match:
                raise GalleryError(f'{page}: expected a colored Good label heading')
            examples.append(('Good', match[1], example))
        for label, url, example in examples:
            expected = self.root / 'preferences/assets' / f'{label.lower()}-label.svg'
            if local_target(url, page) != (expected, ''):
                raise GalleryError(f'{page}: use the shared {label} label asset')
            urls = refs(example)
            if not all(any(urlsplit(u).path.endswith(s) for u in urls)
                       for s in ('-light.svg', '-dark.svg', '.png')):
                raise GalleryError(f'{page}: each example needs light/dark SVG and PNG links')
        for theme in ('light', 'dark'):
            if f'#gh-{theme}-mode-only' not in good or f'-{theme}.svg' not in good:
                raise GalleryError(f'{page}: good preview missing {theme} theme')
        rule = Rule(page, visual, good)
        self.rules[page] = rule
        return rule

    def replace_gallery(self, page: Path, cards: list[str]) -> None:
        text = self.load(page)
        matches = list(GALLERY_START.finditer(text))
        if len(matches) != 1 or text.count(GALLERY_END) != 1:
            raise GalleryError(f'{page}: expected one gallery marker pair')
        a, b = matches[0].end(), text.index(GALLERY_END)
        if b < a:
            raise GalleryError(f'{page}: reversed gallery markers')
        newline = '\r\n' if '\r\n' in text else '\n'
        body = '\n\n'.join(cards)
        generated = ('\n\n' + body + '\n\n').replace('\n', newline)
        self.outputs[page] = text[:a] + generated + text[b:]

    def level(self, page: Path) -> int:
        match = GALLERY_START.search(self.load(page))
        if not match:
            raise GalleryError(f'{page}: missing gallery marker')
        return int(match[1])

    def rule_card(self, rule: Rule, page: Path) -> str:
        level = self.level(page)
        text = re.sub(r'<!-- preference-\w+:(?:start|end) -->\n?', '', rule.visual)
        text = rewrite(text, rule.readme, page)
        def heading(m: re.Match) -> str:
            depth = len(m[1]) + level - 1
            if depth > 6:
                raise GalleryError(f'{rule.readme}: heading exceeds level six')
            label = m[2]
            if len(m[1]) == 1:
                label = f'[{label}]({rebase("README.md", rule.readme, page)})'
            return '#' * depth + ' ' + label
        return re.sub(r'^(#{1,6}) (.+)$', heading, text, flags=re.M).strip()

    def preview(self, category: Path, representative: Rule, page: Path) -> str:
        target = category / 'README.md'
        url = rebase('README.md', target, page)
        good = rewrite(representative.good, representative.readme, page)
        # Make both theme variants open their immediate category.
        good = re.sub(r'href="[^"]*#(gh-(?:light|dark)-mode-only)"',
                      lambda m: f'href="{url}#{m[1]}"', good)
        return f'{"#" * self.level(page)} [{title(self.load(target))}]({url})\n\n{good}'

    def category(self, folder: Path, top: bool = False) -> Rule | None:
        if not folder.resolve().is_relative_to(self.root):
            raise GalleryError(f'Category leaves repository: {folder}')
        page = folder / 'README.md'
        self.load(page)
        # Folders without a record or category README are assets, not entries.
        children = sorted(p for p in folder.iterdir() if p.is_dir() and
                          ((p / 'RULE.md').exists() or (p / 'README.md').exists()))
        if any(p.is_symlink() or p.resolve() != p for p in children):
            raise GalleryError(f'{folder}: linked categories are unsupported')
        rules = [p for p in children if (p / 'RULE.md').exists()]
        categories = [p for p in children if p not in rules]
        if rules and categories:
            raise GalleryError(f'{folder}: mixed rules and subcategories; organization needs agent review')
        cards = []
        descendants = []
        for child in rules:
            rule = self.rule(child)
            if rule:
                descendants.append(rule)
                cards.append(self.rule_card(rule, page))
        for child in categories:
            representative = self.category(child)
            if representative:
                descendants.append(representative)
                cards.append(self.preview(child, representative, page))
        self.replace_gallery(page, cards)
        if top:
            main = self.root / 'README.md'
            if rules:
                raise GalleryError('Top-level preferences must contain categories')
            self.replace_gallery(main, [self.preview(child, rep, main) for child, rep in
                                        self.category_representatives(categories)])
            return None
        choices = REPRESENTATIVE.findall(self.load(page))
        if not descendants:
            if choices:
                raise GalleryError(f'{page}: representative points into a category with no accepted rules')
            return None
        if len(choices) != 1:
            raise GalleryError(f'{page}: choose one representative explicitly')
        candidate = (folder / choices[0]).resolve()
        if not candidate.is_relative_to(folder) or candidate not in self.rules:
            raise GalleryError(f'{page}: representative must be an accepted descendant README')
        return self.rules[candidate]

    def category_representatives(self, categories: list[Path]):
        for child in categories:
            choices = REPRESENTATIVE.findall(self.load(child / 'README.md'))
            if choices:
                yield child, self.rules[(child / choices[0]).resolve()]

    def build(self, check: bool = False) -> list[Path]:
        self.category(self.root / 'preferences', top=True)
        # Validate all outputs before any writes, including destinations of rebased links.
        for path, content in list(self.originals.items()):
            if path.suffix == '.md':
                self.check_links(path, self.outputs.get(path, content))
        for path in (self.root / 'preferences/GENERAL.md',):
            self.check_links(path, self.load(path))
        changed = [p for p, content in self.outputs.items() if content != self.originals[p]]
        if not check:
            for path in self.originals:
                if read(path) != self.originals[path]:
                    raise GalleryError(f'Concurrent edit detected; rerun: {path}')
            for path in changed:
                path.write_bytes(self.outputs[path].encode('utf-8'))
        return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail on stale outputs or missing references; write nothing')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1], help='Repository root (also useful for isolated validation fixtures)')
    args = parser.parse_args()
    try:
        changed = Builder(args.root).build(args.check)
    except (GalleryError, OSError, UnicodeError) as error:
        print(f'Gallery error: {error}', file=sys.stderr)
        return 2
    for path in changed:
        print(f'{"Stale" if args.check else "Updated"}: {path.relative_to(args.root.resolve())}')
    if args.check and changed:
        return 1
    print('Preference galleries are current; local references passed.' if not changed else 'Preference galleries built; local references passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
