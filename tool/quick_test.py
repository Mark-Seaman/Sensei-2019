from insight.models import *
from tool.days import *
from tool.text import *
from unc.review import *


def quick_test():
    text = text_lines(open('Documents/info/Test/Outline3').read())
    text = [line for line in text if line.strip()]
    tree, text = outline(text)
    print_outline_indent(tree)


def outline(text, indent=''):
    tree = []
    while text and text[0].startswith(indent):
        label = text[0].strip()
        text = text[1:]
        if label:
            node = [label]
            # print(node[0], '%d' % len(indent))
            kids, text = outline(text, ' '*4+indent)
            if kids:
                node += kids
            tree.append(node)
    return tree, text


def print_outline_markdown(tree, indent='#'):
    for node in tree:
        print(indent + " " + node[0])
        print_outline_markdown(node[1:], indent+'#')


def print_outline_indent(tree, indent=''):
    for node in tree:
        print(indent + node[0])
        print_outline_indent(node[1:], indent+'    ')


def create_insights(month):
    for day in enumerate_month(2019, month):
        date = datetime.strptime(day, "%Y-%m-%d")
        i = Insight.objects.get_or_create(date=date)[0]
        i.save()
        print(i)
