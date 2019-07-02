from os.path import join

from tool.document import text_to_html


def has_kids(text, depth):
    return len(split_text(text, seperator(depth+1)))>1


def outline(text):
    tree = parse_outline(text, [], 1)
    # print(tree)
    return tree


def parse_outline(text, tree, depth):
    kids = []
    if has_kids(text, depth):
        for subtext in split_text(text, seperator(depth+1))[1:]:
            # print_node(title(subtext, depth+1)[0], depth+1)
            kids = parse_outline(subtext, kids, depth+1)
    node = title(text, depth)
    if kids:
        tree.append((node[0], kids, node[1]))
    else:
        tree.append((node[0], None, node[1]))
    return tree


def print_node(name, depth=1, char='    '):
    print('%s %s' % (char * depth, name))


def seperator(depth):
    return '\n%s ' % ("#"*depth)


def split_text(text, sep):
    return [x for x in text.split(sep) if x]


def title(text, depth):
    parts = split_text(text, seperator(depth+1))
    text = parts[0]
    x = len(text.split('\n')[0])
    title = text[:x]
    body = text_to_html(text[x + 1:])
    return title, body


def read_cards(doc):
    text = open(join('Documents', doc)).read()[2:]
    sections = split_text(text, seperator(2))
    return [title(x, 3) for x in sections]


def tabs_data(doc):

    def tab_choice(i,tab):
        return ('tab%d'%i, tab[0], tab[1], 'active' if i==0 else '')

    tabs = read_cards(doc)
    return [tab_choice(i,tab) for i,tab in enumerate(tabs)]
