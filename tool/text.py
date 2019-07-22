from re import compile, findall, search
from os.path import exists


# ------------------------------
# Command Interpreter
from tool.files import read_text
# from tool.shell import shell_script


def text_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        if cmd == 'match':
            m = text_match(args[0], args[1])
            print('\n'.join(m))
        elif cmd == 'no-match':
            text_no_match(args[0], args[1])
        elif cmd == 'replace':
            text_replace(args[0], args[1], args[2])
        else:
            text_help(args)
    else:
        text_help()


def text_help(args=None):
    print('''
        text Command

        usage: x text COMMAND

        COMMAND:

            match - show lines that match
            no_match - show lines that don't match
            replace - replace lines
            select - pattern matching in doc

        ''')


# ------------------------------
# Functions

def count_lines(text):
    return len(text_lines(text))


def delete_lines(text, match_pattern):
    text = text.split('\n')
    text = [t for t in text if match_pattern not in t]
    return '\n'.join(text)


def doc_filter(doc, match_pattern, replace_pattern):
    text = open(doc).read()
    return text_replace(text, match_pattern, replace_pattern)


def find_agents(text):
    pattern = r'(.{15}) +(.{15}) +([\w\d_\-\.]+\@[\w\d_\-\.]+)'
    return transform_matches(text, pattern, r'email: \3, company: \2, user: \1')


def find_anchors(text):
    return findall('<a href="(https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)">(.*)</a>', text)


def find_links(text):
    def link(anchor):
        return findall('(https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)">(.*)</a>', anchor)[0]

    results = []
    for anchor in text.split(r'<a ')[1:]:
        anchor = r'<a ' + anchor
        results.append(link(anchor))
    return str(results)


def find_markdown_links(text):
    # Look for links in markdown text
    match_pattern = r'\[(.*)\]\((.*)\)'
    results = [match[1] for match in findall(match_pattern, text)]
    return '\n'.join(results)


def find_quotes(text):
    return findall('<div class=\'noteText\'>(.*?)</div>', text)


def find_urls(text):
    return findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)


def markdown_list_links(host, lines):
    return markdown_list_string(['[%s](%s/%s)' % (x, host, x) for x in lines])


def markdown_list_string(mylist):
    return '* ' + '\n* '.join(mylist)


def match_lines(text, pattern):
    text = text.split('\n')
    text = [line for line in text if search(pattern, line)]
    return '\n'.join(text)


def match_pattern(text, pattern):
    text = text.split('\n')
    text = [search(pattern, line) for line in text]
    text = [x.string for x in text if x]
    return '\n'.join(text)


def text_join(text):
    return '\n'.join(text)


def text_lines(text):
    return text.split('\n')


def text_markdown(outline, depth=1):
    def text_body(lines):
        if lines and len(lines[0].strip()) == 0:
            return text_body(lines[1:])
        elif lines and len(lines[-1].strip()) == 0:
            return text_body(lines[:-1])
        else:
            return lines

    results = []
    for n in outline:
        results.append('#' * depth + ' ' + n[0] + '\n')
        t = text_body(n[2])
        if t:
            for t in text_body(n[2]):
                results.append(t)
            results.append('')
        children = text_markdown(n[1], depth + 1)
        if children:
            results.append(children)
    return '\n'.join(results)


def text_match(match_pattern, doc):
    matches = []
    if doc and exists(doc):
        text = open(doc).read()
        if text:
            for line in text.split('\n'):
                match = search(r'^.*(%s).*$' % match_pattern, line)
                if match:
                    matches.append(match.string)
            return '\n'.join([('%s: %s' % (doc, m)) for m in matches])


def text_no_match(match_pattern, doc):
    text = open(doc).read()
    for line in text_lines(text):
        match = search(r'^.*(%s).*$' % match_pattern, line)
        if not match:
            print(line)


def text_outline(text):
    lines = text_lines(text)
    root = []
    active = None
    for line in lines:
        if line.startswith('# '):
            active = [line[2:], [], []]
            root.append(active)
            h1 = active
        elif line.startswith('## '):
            active = [line[3:], [], []]
            h1[1].append(active)
            h2 = active
        elif line.startswith('### '):
            active = [line[4:], [], []]
            h2[1].append(active)
            h3 = active
        elif line.startswith('#### '):
            active = [line[5:], [], []]
            h3[1].append(active)
        else:
            if active:
                active[2].append(line)
    return root


def text_outline_string(outline, depth=0):
    results = []
    for n in outline:
        results.append('    ' * depth + n[0])
        for t in n[2]:
            if t.strip():
                results.append('    ' * (depth + 1) + '* ' + t)
        results.append(text_outline_string(n[1], depth + 1))
    return '\n'.join(results)


def text_replace(text, match_pattern, replace_pattern):
    return compile(match_pattern).sub(replace_pattern, text)


def text_title(text):
    return text.split('\n')[0]


def text_body(text):
    return '\n'.join(text.split('\n')[1:])


def transform_matches(text, match_pattern, select_pattern):
    results = []
    for line in text.split('\n'):
        match = compile(match_pattern).sub(select_pattern, line)
        if match != line:
            results.append(match)
    return '\n'.join(results)


def file_search(files, words):
    matches = []
    for f in files:
        text = text_lines(read_text(f))
        for pattern in words:
            text = [('%s: %s' % (f, line)) for line in text if search(pattern, line)]
        if text:
            matches += text
    return text_join(matches)



