from django import forms
from django.forms import Form
from django.views.generic import FormView, TemplateView
from os.path import join
from random import choice, randint

from unc.models import Student, UrlGame
from unc.views import UncPage
from unc.bacs import get_student


def generate_url_question():
    url_type = choice(['Relative', 'Absolute', 'Server'])
    d1 = random_domain()
    d2 = random_domain()

    path = random_path()
    page = join(d1, path, random_page())
    file_name = random_file()
    dir_name = random_path()

    if url_type == 'Absolute':
        url = join(d2, dir_name, file_name)
        correct = join(d2, dir_name, file_name)
    elif url_type == 'Server':
        url = join(d1, dir_name, file_name)
        correct = join('/', dir_name, file_name)
    else:
        url = join(d1, dir_name, file_name)
        dir_name = relative_path(path, dir_name)
        correct = join(dir_name, file_name)

    return dict(page=page, url=url, url_type=url_type, correct=correct)


def get_hint(url_type):
    hint = "URL Type is %s URL." % url_type
    if url_type == 'Absolute':
        hint += '  Always include the protocol and domain in the URL.'
    elif url_type == 'Relative':
        hint += '  Only list the path (directory path and filename).'
    else:
        hint += '  Always start with "/" to get to the root of the current domain in the URL.'
    return hint


def relative_path(p1, p2):
    if p1 == p2: return ''
    p1 = p1.split('/')
    p2 = p2.split('/')
    x1 = p1
    x2 = p2
    print('before', p1, p2)
    if p1 == ['']:
        x1 = []

    for i,x in enumerate(p1):
        if p1[i:] and p2[i:] and p1[i] == p2[i]:
            x1 = p1[i+1:]
            x2 = p2[i+1:]
            print('same', x1, x2)
        else:
            break

    p1 = '/'.join(['..' for d in x1])
    p2 = '/'.join([d for d in x2])
    print('after', p1, p2)
    print(p1+'/'+p2)
    return join(p1, p2)


def random_page():
    pages = [
        "lesson40.html",
        "image.html",
        "color.html",
        "lesson10.html",
        "pie.html",
    ]
    return choice(pages)


def random_file():
    files = [
        "cat.jpg",
        "dog.png",
        "abe.png",
        "Abe.png",
        "abe.PNG",
        "dog.gif",
        "index.html",
        "animals.html",
        "projects.html",
        "Lesson-1.html",
        "styles.css",
    ]
    return choice(files)


def random_domain():
    protocols = [
        'http:/',
        'https:/',
    ]

    domains = [
        'www.unco.edu',
        'shrinking-world.com',
        'unco-bacs.org',
        'google.com',
        'greeley-colorado.gov',
    ]

    return '/'.join([choice(protocols), choice(domains)])


def random_path():
    directories = [
        "css",
        "images",
        "assets",
        "bacs200",
        "pages",
        "project",
    ]
    return '/'.join([choice(directories) for d in range(randint(0, 2))])


def reset_questions_left():
    for game in UrlGame.objects.all():
        print(game.student.name, game.answered, game.left)
        game.left = 10
        game.save()


def url_feedback(answer, correct):
    if answer == correct:
        return 'smiley1.jpg'
    else:
        return 'sad1.jpg'


class UncUrlGameAnswer(FormView):

    class UrlForm(Form):
        answer = forms.CharField()
        url = forms.CharField()
        url_type = forms.CharField()
        page = forms.CharField()
        correct = forms.CharField()
        answered = forms.IntegerField()
        left = forms.IntegerField()

    form_class = UrlForm
    template_name = 'urlgame.html'

    def get_context_data(self, **kwargs):
        student = get_student(self.request)
        header = ['UNC BACS', student.name, "/static/images/unc/Bear.200.png", 'UNC Bear']
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3])

        self.answer = self.request.GET.get('answer', "None")
        self.page = self.request.GET.get('page', "None")
        self.url = self.request.GET.get('url', "None")
        self.url_type = self.request.GET.get('url_type', "None")
        self.correct = self.request.GET.get('correct', 'None')
        self.iscorrect = (self.request.GET.get('iscorrect') == u'True')
        self.image = self.request.GET.get('image')
        hint = get_hint(self.url_type)

        answer = dict(a=dict(answer=self.answer, url=self.url, correct=self.correct, image=self.image,
                      page=self.page, url_type=self.url_type, iscorrect=self.iscorrect, hint=hint))

        game = UrlGame.objects.get_or_create(student=student)[0]
        game = dict(correct=game.correct, incorrect=game.answered - game.correct, answered=game.answered, left=game.left)

        kwargs.update(answer)
        kwargs.update(game)
        return kwargs

        # return dict(title=title, student=student, a=answer, answered=game.answered, correct=game.correct, incorrect=game.answered-game.correct, left=game.left)

    def form_valid(self, form):
        student = get_student(self.request)
        game = UrlGame.objects.get_or_create(student=student)[0]

        self.url = form.data.get('url')
        self.answer = form.data.get('answer')
        self.correct = form.data.get('correct')
        self.page = form.data.get('page')
        self.url_type = form.data.get('url_type')

        self.iscorrect = (self.correct == self.answer)
        if self.iscorrect:
            game.left = game.left - 1
            game.correct += 1
        else:
            game.left = 10
        game.answered = game.answered + 1
        game.save()

        return super(UncUrlGameAnswer, self).form_valid(form)

    def get_success_url(self):
        student = get_student(self.request)
        game = UrlGame.objects.get_or_create(student=student)[0]
        if game.left < 1:
            return '/unc/url-game-done'
        else:
            parms = '&'.join([
                "answer=%s" % self.answer,
                "url=%s" % self.url,
                "correct=%s" % self.correct,
                "page=%s" % self.page,
                "url_type=%s" % self.url_type,
                "image=%s" % url_feedback(self.answer, self.correct),
                "iscorrect=%s" % self.iscorrect,
            ])
            return '/unc/url-answer?%s' % parms


class UncUrlGameQuestion(UncPage):
    template_name = 'urlgame.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'URL Crusher'
        kwargs = super(UncUrlGameQuestion, self).get_context_data(**kwargs)
        game = UrlGame.objects.get_or_create(student=kwargs['student'])[0]
        question = generate_url_question()
        # return dict(title=title, student=student, q=question, correct=game.correct, incorrect=game.answered-game.correct, answered=game.answered, left=game.left)
        game = dict(q=question, correct=game.correct, incorrect=game.answered-game.correct, answered=game.answered, left=game.left)
        kwargs.update(game)
        return kwargs


class UncUrlGameDone(UncPage):
    template_name = 'urlgame_done.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'URL Crusher'
        kwargs = super(UncUrlGameDone, self).get_context_data(**kwargs)
        game = UrlGame.objects.get_or_create(student=kwargs['student'])[0]
        game = dict(correct=game.correct, incorrect=game.answered-game.correct, answered=game.answered, left=game.left)
        kwargs.update(game)
        return kwargs
