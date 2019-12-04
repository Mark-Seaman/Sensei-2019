from django.utils.timezone import make_aware
from datetime import datetime
from random import shuffle

from unc.models import Course, Project, Review, Student


def assign_reviews_round1():
    for s in Course.students('bacs200'):
        create_review(s, s, 'bacs200/index.html', '2019-10-25', bacs200_1_requirements, bacs200_1_notes)
    for s in Course.students('bacs350'):
        create_review(s, s, 'bacs350/index.php', '2019-10-25', bacs350_1_requirements, bacs350_1_notes)

        
def assign_reviews_round2():
    assign_team_reviews('bacs200', 'bacs200/index.html', '2019-10-28', bacs200_1_requirements, bacs200_1_notes)
    assign_team_reviews('bacs350', 'bacs350/index.php', '2019-10-28', bacs350_1_requirements, bacs350_1_notes)


def assign_reviews_round3():
    assign_team_reviews('bacs200', 'bacs200/teach.html', '2019-11-04', bacs200_3_requirements, bacs200_3_notes)
    assign_team_reviews('bacs350', 'bacs350/superhero/index.php', '2019-11-04', bacs350_3_requirements, bacs350_3_notes)


def assign_reviews_round4():
    assign_team_reviews('bacs200', 'bacs200/travel/index.html', '2019-11-11', bacs200_4_requirements, bacs200_4_notes)
    assign_team_reviews('bacs350', 'bacs350/slides/index.php',  '2019-11-11', bacs350_4_requirements, bacs350_4_notes)


def assign_team_reviews(course, page, due, requirements, notes):
    groups = review_groups(course)
    pairs = review_pairs(review_groups(course))
    for p in pairs:
        print('create review: %s,  %s' % (p[0], p[1]))
        create_review(p[0], p[1], page, due, requirements, notes)
    return len(pairs)


def count_score(r):
    requirements = [r.requirement_1, r.requirement_2, r.requirement_3, r.requirement_4, r.requirement_5,
                    r.requirement_6, r.requirement_7, r.requirement_8, r.requirement_9, r.requirement_10]
    return len([x for x in requirements if x])


def create_review(reviewer, designer, page, due, requirements, notes):
    due = '%s 23:59' % due
    due = make_aware(datetime.strptime(due, "%Y-%m-%d %H:%M"))
    r = Review.objects.get_or_create(reviewer_id=reviewer, designer_id=designer, page=page, due=due)[0]
    # r.due = due
    r.requirement_labels = requirements
    r.notes = notes
    r.save()
    return r


def get_review(id):
    return Review.objects.get(pk=id)


def grade_reviews(page):
    print('\nTo Do ' + page)
    for r in Review.objects.filter(page=page, score=-1):
        print("    " + r.reviewer.name)
    print('\nDone ' + page)
    for r in Review.objects.filter(page=page).exclude(score=-1):
        print("    " + r.reviewer.name)

    
def review_pairs(groups):
     x = []
     for team in groups:
         for reviewer in team:
             for designer in team:
                 if reviewer != designer:
                     x.append((designer, reviewer))
     print(len(x))
     return x


# def show_groups(course):
#     show_students(course)
#     groups = review_groups(course)
#     print('Groups - %s' % len(groups))
#     for g in groups:
#         print(g)
#     print(review_pairs(groups))
        
        
def show_students(course):
    print('Students - %s' % len(Course.students(course)))
    for s in Course.students(course):
        print('%s. %s' % (s.pk, s.name))

        
# def show_reviews_overdue(course):
#     print('\nTo Do '+course)
#     for r in Review.objects.filter(reviewer__course__name=course, score=-1):
#         print("    " + r.reviewer.name)
#     print('\nDone '+course)
#     for r in Review.objects.filter(reviewer__course__name=course).exclude(score=-1):
#         print("    " + r.reviewer.name)
#
        
def review_groups(course):
     show_students(course)
     groups = []
     num = 4
     s = [a.pk for a in Course.students(course)]
     shuffle(s)
     x = 0
     while s[x:x + num]:
         groups.append(s[x:x + num])
         x += num
     # groups = [groups[0] + groups[-1]] + groups[1:-1]
     return groups


def query_current_reviews(student_id):
    student = Student.get_record(student_id)
    page = Project.objects.get(course=student.course, num=13).page
    reviews = Review.objects.filter(page=page, due__gte='2019-12-02')
    return reviews


def reviewer_scores(student_id):
    reviews = student_reviews_done(student_id)
    return [r.score for r in reviews]


def designer_scores(student_id):
    reviews = review_feedback(student_id)
    return [r.score for r in reviews]


def review_feedback(student_id):
    return query_current_reviews(student_id).filter(designer=student_id).exclude(score=-1)


def student_reviews(student_id):
    return query_current_reviews(student_id).filter(reviewer=student_id, score=-1)


def student_reviews_done(student_id):
    return query_current_reviews(student_id).filter(reviewer=student_id).exclude(score=-1)


def print_reviews(reviewer=None):
    print('Design Reviews')
    if reviewer:
        for r in student_reviews(reviewer.pk):
            print(r)
            print('REQUIREMENTS:\n%s\n' % r.requirement_labels)
            print('NOTES:\n%s\n' % r.notes)
    else:
        for r in Review.objects.all():
            print(r)
            # print('REQUIREMENTS:\n%s\n' % r.requirement_labels)
            # print('NOTES:\n%s\n' % r.notes)


# BACS 200 Reviews

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
bacs200_1_notes = '''* Page exists at bacs200/index.html
* Title, Author
* Link to class website 
* Profile Photo
* CSS Stylesheet (in separate file)
* Banner with site title and tag line
* Project table with page and validation links
* Skills table with links to skills
* Valid HTML
* Valid CSS
'''

bacs200_3_requirements = '''Page exists at bacs200/teach.html
Teaches a skill from W3Schools
Contains example code
Good "how to" explanation
Easy to apply to your "demo" page
Shows running demonstration 
Page looks visually appealing
CSS Stylesheet (in separate file)
Valid HTML
Valid CSS'''
bacs200_3_notes = '''Write a summary of all the problems and how to fix them.   Must be 100 characters.'''

bacs200_4_requirements = '''Page is located at correct URL (bacs200/travel/index.html)
All pages validate HTML and CSS and links
All JavaScript widgets work
All links work properly
Other pages are working properly
Page is beautiful
Marketing message is clear and compelling
Page shows marketing carousel with photos
Page shows products
Page shows activities'''
bacs200_4_notes = '''Write a summary of all the problems and how to fix them.   Must not be blank.'''

bacs200_5_requirements = '''Page Exists at correct URL (your domain/index.php)
Page can be used in your marketing efforts
Clear professional identity
Business article
Clear navigation
Include a link to another website to learn more
Great images
Titles, favicon, supporting text
Good page layout
Valid HTML & CSS'''
bacs200_5_notes = '''Write a summary of all the problems and how to fix them.   Must not be blank.'''


# BACS 350 Reviews

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
bacs350_1_notes = '''* Page exists at bacs350/index.php
* Title, Author
* Link to class website 
* Profile Photo
* CSS Stylesheet (in separate file)
* Banner with site title and tag line
* Links to project pages (planner, project, docman, superhero, subscriber, notes)
* Skills table with links to skills
* Valid HTML
* Valid CSS
'''

bacs350_3_requirements = '''Page exists at bacs350/superhero.php
Displays existing superheroes
Links to home page
Home page has link to Github repo for code review
Banner with site title and tag line
Can add new superhero
Can remove a superhero
Can edit superhero
Valid HTML
Valid CSS'''
bacs350_3_notes = '''Write a summary of all the problems and how to fix them.   Must be 100 characters.'''

bacs350_4_requirements = '''Main page is "bacs350/slides/index.php"
Data Views (list, detail, add, edit, delete)
Create and modify markdown content
Run slide show in new browser tab
Custom styles for your app
Log all pages loaded and CRUD events
Use design patterns to avoid duplication
Page HTML and CSS validate
Several slide shows created with Markdown
Show presentation records'''
bacs350_4_notes = '''Write a summary of all the problems and how to fix them.   Must not be blank.'''

bacs350_5_requirements = '''* Top app is located at "bacs350/index.php"
* Brain contains links to each component: Documents, Notes, Slides, Planner, Reviewer, Subscribers, Superhero
* Each app component works properly
* Each app component has valid HTML and CSS
* Design is consistent with the code
* All code is updated in Github account
* All outstanding issues are logged in database
* Visual appearance and behavior (look and feel)
* Add User Auth
* Reusable code eliminates duplication'''
bacs350_5_notes = '''Write a summary of all the problems and how to fix them.   Must not be blank.'''


def student_project_data(course):
    data = []
    for s in Course.students(course):
        data.append(dict(student=s, designer=designer_scores(s.pk), reviewer=reviewer_scores(s.pk)))
    return data