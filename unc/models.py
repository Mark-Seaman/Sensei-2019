from django.db import models
from tool.days import date_str
from django.contrib.auth.models import User

from tool.days import due_date


class Course(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    teacher = models.CharField(null=True, max_length=100)
    description = models.TextField(null=True)

    # Require chars, default='You must type a description of the course', validators=[MinLengthValidator(100)])

    def __str__(self):
        return '%4d %-10s %-44s %-20s %s' % (self.pk, self.name, self.title, self.teacher, self.description)

    @staticmethod
    def all():
        return [c.name for c in Course.objects.all()]

    @staticmethod
    def lookup(course):
        return Course.objects.get(name=course)

    @staticmethod
    def query():
        return Course.objects.all()

    @staticmethod
    def list():
        return [str(o) for o in Course.query()]

    @staticmethod
    def students(course):
        return Student.objects.filter(course__name=course).order_by('user__last_name')


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=40)
    domain = models.CharField(max_length=100, null=True)
    zbooks = models.CharField(max_length=100, null=True)

    def __str__(self):
        return '%d. %-40s %-40s %s' % (self.pk, self.email, self.name, self.domain)

    @staticmethod
    def list():
        return [str(o) for o in Student.objects.all()]


class Project(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.IntegerField()
    title = models.CharField(max_length=100)
    page = models.CharField(max_length=100, editable=False)
    due = models.DateTimeField(null=True, editable=False)
    instructions = models.URLField()

    def __str__(self):
        return '%s/project/%02d   %-30s  %-30s %s' % (self.course.name, self.num, self.title, self.page, self.due.strftime("%Y-%m-%d"))

    @property
    def due_date(self):
        return self.due.strftime("%A, %b %d")

    @property
    def directions(self):
        return '/unc/%s/project/%02d' % (self.course.name, self.num)

    @staticmethod
    def lookup(course, id):
        return Project.objects.get(course__name=course, num=id)

    @staticmethod
    def list(course):
        return [str(o) for o in Project.objects.filter(course__name=course).order_by('due')]

    @staticmethod
    def query(course):
        return Project.objects.filter(course__name=course).order_by('due')

    @property
    def requirements(self):
        return Requirement.objects.filter(project=self).order_by('num')

    @property
    def test_link(self):
        return '/unc/%s/%02d/test' % (self.course.name, self.num)


class Requirement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    num = models.IntegerField(default=-1)
    label = models.CharField(default='None', max_length=100)
    selector = models.CharField(max_length=100)
    actual = models.TextField(default='Test not run yet')
    correct = models.TextField(default='Test not run yet')
    results = models.TextField(default='Test not run yet')
    transform = models.CharField(null=True, max_length=200)

    @property
    def status(self):
        return 'Requirement PASSED' if self.correct == self.actual else 'Requirement FAILED'

    @property
    def face(self):
        return '/static/images/happy.jpg' if self.correct == self.actual else '/static/images/sad.jpg'

    def __str__(self):
        return 'Requirement %02d. %s' % (self.num, self.label)

    @staticmethod
    def list():
        return [str(o) for o in Requirement.objects.all()]


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(null=True, editable=False)
    due = models.DateTimeField(null=True, editable=False)
    status = models.IntegerField()

    def __str__(self):
        return '%4d.  %-30s  %-10s %-15s %-15s %s' % (self.pk, self.student.name, self.project.num, date_str(self.due), self.state, date_str(self.date))

    @staticmethod
    def list():
        return [str(o) for o in Assignment.objects.all()]

    @property
    def state(self):
        if self.status == 0:
            label = 'Assigned'
        elif self.status == 1:
            label = 'Tested'
        elif self.status == 2:
            label = 'Reviewed'
        return label


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    week = models.IntegerField(default=1)
    date = models.DateTimeField(default=None, null=True, editable=False)
    lesson = models.IntegerField(default=1)
    topic = models.CharField(default='none', max_length=100)
    reading = models.CharField(default='none', max_length=200)

    # CSV Data -- Week, Day, Date, Lesson, Topic, Reading, Projects, Process, Parts
    def __str__(self):
        return '%d -- %5d %5d   %-15s %-20s %s' % (self.course.pk, self.lesson, self.week, date_str(self.date), self.topic, self.reading)

    @staticmethod
    def query(course):
        return Lesson.objects.filter(course__name=course).order_by('date')

    @staticmethod
    def list(course):
        return [str(c) for c in Lesson.query(course)]


class Skill(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.IntegerField()
    due = models.DateTimeField(default=None, null=True)
    topic = models.CharField(default='none', max_length=100)
    images = models.CharField(default='', max_length=200)

    # CSV Data -- Course, Num, Topic, Due
    def __str__(self):
        return '%s - Skill #%s - %-20s - due %s - %s' % (self.course.name, self.num, self.topic, date_str(self.due), self.images)

    @staticmethod
    def create(course, num, topic, due, images):
        course = Course.lookup(course)
        s = Skill.objects.get_or_create(course=course, num=num)[0]
        s.topic = topic
        s.due = due_date(due)
        s.images = images
        s.save()
        return s

    @staticmethod
    def get(course, num):
        return Skill.objects.get(course__name=course, num=num)

    @staticmethod
    def query(course):
        return Skill.objects.filter(course__name=course).order_by('num')

    @staticmethod
    def list(course):
        return [str(c) for c in Skill.query(course)]

