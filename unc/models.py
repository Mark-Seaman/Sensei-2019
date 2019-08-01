from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    teacher = models.CharField(null=True, max_length=100)
    description = models.TextField(null=True)

    def __init__(self, name, title, teacher, description):
        Course.objects.get_or_create(name, title, teacher, description)

    # , default='You must type a description of the course', validators=[MinLengthValidator(100)])

    def __str__(self):
        return 'Course: %s - %s' % (self.name, self.title)


class Student(models.Model):
    course  = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    name    = models.CharField(max_length=100)
    email   = models.CharField(max_length=40)
    domain  = models.CharField(max_length=100)
    zbooks  = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return '%s, %s, %s' % (self.email, self.name, self.domain)


class Project(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.IntegerField()
    title = models.CharField(max_length=100)
    page = models.CharField(max_length=100, editable=False)
    score = models.IntegerField(default=-1)
    date = models.DateTimeField(null=True, editable=False)
    due = models.DateTimeField(editable=False)
    instructions = models.URLField()

    def __str__(self):
        return 'Project %02d. %s - %s' % (self.num, self.title, self.date)


class Requirement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    actual = models.TextField()
    correct = models.TextField()
    label = models.CharField(max_length=100)
    selector = models.CharField(max_length=100)

    @property
    def status(self):
        return 'Status: Requirement met' if self.correct == self.actual else 'Status: Requirement FAILED'

    def __str__(self):
        return 'Requirement %02d. %s' % (self.num, self.label)

