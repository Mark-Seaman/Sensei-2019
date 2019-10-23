from test.unc_test import *
from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.review import *
from unc.skills import *
from tasks.summary import *


def quick_test():
    assign_reviews()
    reviewer = Student.lookup('Sensei 200')
    print_reviews(reviewer)


def print_reviews(reviewer):
    print('Design Reviews')
    for r in student_reviews(reviewer.pk):
        print(r)
        print('REQUIREMENTS:\n%s\n' % r.requirement_labels)


bacs200_1_requirements = '''Page exists at bacs200/index.html
Title, Author
Link to class website 
Profile Photo
CSS Stylesheet (in separate file)
Banner with site title and tag line
Project table with page and validation links
Skills table with links to skills
Valid HTML
Valid CSS'''


bacs350_1_requirements = '''Page exists at bacs350/index.php
Title, Author
Link to class website 
Profile Photo
CSS Stylesheet (in separate file)
Banner with site title and tag line
Links to project pages (planner, project, docman, superhero, subscriber, notes)
Skills table with links to skills
Valid HTML
Valid CSS'''


def assign_reviews():

    reviewer = Student.lookup('Sensei 200')
    designer = Student.lookup('Sensei 200')
    page = 'bacs200/index.html'
    due = '2019-10-22'
    create_review(reviewer, designer, page, due, bacs200_1_requirements)

    reviewer = Student.lookup('Sensei 200')
    designer = Student.lookup('Sensei 350')
    page = 'bacs350/index.php'
    due = '2019-10-22'
    create_review(reviewer, designer, page, due, bacs350_1_requirements)



    # init_unc_data()


def init_unc_data():
    # x = import_schedule('bacs200')
    # x = import_schedule('bacs350')
    update_lessons()
    update_projects()
    update_skills()
    x = list_course_content()
    print(x)


def show_course_content():
    x = list_course_content()
    print(x)


