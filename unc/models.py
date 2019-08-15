from django.db import models
from django.utils.timezone import now
from datetime import datetime
from tool.days import date_str


class Course(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    teacher = models.CharField(null=True, max_length=100)
    description = models.TextField(null=True)

    # , default='You must type a description of the course', validators=[MinLengthValidator(100)])

    def __str__(self):
        # return 'Course: %s - %s' % (self.name, self.title)
        return '%4d %-10s %-44s %-20s %s' % (self.pk, self.name, self.title, self.teacher, self.description)

    @staticmethod
    def query():
        return Course.objects.all()

    @staticmethod
    def list():
        return [str(o) for o in Course.query()]


class Student(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=40)
    domain = models.CharField(max_length=100)
    zbooks = models.CharField(max_length=100, null=True)

    # @property
    # def name(self):
    #     return 'Status: Requirement met' if self.correct == self.actual else 'Status: Requirement FAILED'
    #
    def __unicode__(self):
        return '%s, %s, %s' % (self.email, self.name, self.domain)

    @staticmethod
    def list():
        return [str(o) for o in Student.objects.all()]


class Project(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.IntegerField()
    title = models.CharField(max_length=100)
    page = models.CharField(max_length=100, editable=False)
    due = models.DateTimeField(default=datetime.now(), null=True, editable=False)
    instructions = models.URLField()

    def __str__(self):
        return '%s/project/%02d   %s  %-30s %s' % (self.course.name, self.num, self.title, self.page, self.due.strftime("%Y-%m-%d"))
        # return 'Project %02d. %s - %s' % (self.num, self.title, self.due)

    def add_requirement(self, selector):
        r = Requirement.objects.get_or_create(project=self, selector=selector)[0]
        r.num = -1
        r.label = selector
        r.save()

    @property
    def requirements(self):
        return Requirement.objects.filter(project=self)

    @staticmethod
    def lookup(course, id):
        return Project.objects.get(course__name=course, num=id)

    @staticmethod
    def list(course):
        return [str(o) for o in Project.objects.filter(course__name=course).order_by('due')]


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
        return 'Status: Requirement met' if self.correct == self.actual else 'Status: Requirement FAILED'

    def __str__(self):
        return 'Requirement %02d. %s' % (self.num, self.label)

    @staticmethod
    def list():
        return [str(o) for o in Requirement.objects.all()]


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(editable=False)
    status = models.IntegerField()

    def __str__(self):
        return 'Assignment %02d. Student %s, Project %s' % (self.pk, self.student.name, self.project.num)

    @staticmethod
    def list():
        return [str(o) for o in Assignment.objects.all()]


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
        return '%d -- %5d %5d   %-15s %-30s %s' % (self.course.pk, self.lesson, self.week, date_str(self.date), self.topic, self.reading)

    @staticmethod
    def query(course):
        return Lesson.objects.filter(course__name=course).order_by('date')

    @staticmethod
    def list(course):
        return [str(c) for c in Lesson.query(course)]

