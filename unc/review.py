from django.utils.timezone import make_aware
from datetime import datetime
from random import shuffle

from unc.models import Course, Review, Student


def assign_reviews_round1():
    for s in Course.students('bacs200'):
        create_review(s, s, 'bacs200/index.html', '2019-10-25', bacs200_1_requirements, bacs200_1_notes)
    for s in Course.students('bacs350'):
        create_review(s, s, 'bacs350/index.php', '2019-10-25', bacs350_1_requirements, bacs350_1_notes)

        
def assign_reviews_round2():
    assign_team_reviews('bacs200', 'bacs200/index.html', '2019-10-28', bacs200_1_requirements, bacs200_1_notes)
    assign_team_reviews('bacs350', 'bacs350/index.php', '2019-10-28', bacs350_1_requirements, bacs350_1_notes)


def assign_team_reviews(course, page, due, requirements, notes):
    groups = review_groups(course)
    pairs = review_pairs(review_groups(course))
    for p in pairs:
        print('create review: %s,  %s' % (p[0], p[1]))
        create_review(p[0], p[1], page, due, requirements, notes)
    return len(pairs)


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


def show_groups(course):
    show_students(course)
    groups = review_groups(course)
    print('Groups - %s' % len(groups))
    for g in groups:
        print(g)
    print(review_pairs(groups))
        
        
def show_students(course):
    print('Students - %s' % len(Course.students(course)))
    for s in Course.students(course):
        print('%s. %s' % (s.pk, s.name))

        
def show_reviews_overdue(course):
    print('\nTo Do '+course)
    for r in Review.objects.filter(reviewer__course__name=course, score=-1):
        print("    " + r.reviewer.name)
    print('\nDone '+course)
    for r in Review.objects.filter(reviewer__course__name=course).exclude(score=-1):
        print("    " + r.reviewer.name)

        
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



def count_score(r):
    requirements = [r.requirement_1, r.requirement_2, r.requirement_3, r.requirement_4, r.requirement_5,
                    r.requirement_6, r.requirement_7, r.requirement_8, r.requirement_9, r.requirement_10]
    return len([x for x in requirements if x])


def create_review(reviewer, designer, page, due, requirements, notes):
    due = '%s 23:59' % due
    due = make_aware(datetime.strptime(due, "%Y-%m-%d %H:%M"))
    r = Review.objects.get_or_create(reviewer_id=reviewer, designer_id=designer, page=page)[0]
    r.due = due
    r.requirement_labels = requirements
    r.notes = notes
    r.save()
    return r


def get_review(id):
    return Review.objects.get(pk=id)


# def query_reviewers(course):
#
#     def reviewer_summary(student):
#         student_id = student.pk
#         reviews = student_reviews_done(student_id)
#         not_done = student_reviews(student_id)
#         assigned = len(reviews) + len(not_done)
#         rounds = 13
#         points = 10 * rounds * len(reviews) / assigned
#         return student, reviews, "%d done of %d assigned, score = %d" % (len(reviews), assigned, points)
#
#     all_students = Course.students(course)
#     return [reviewer_summary(s) for s in all_students]
#
#
# def query_designers(course):
#
#     def designer_summary(student):
#         student_id = student.pk
#         reviews = review_feedback(student_id).filter(page='bacs200/projects/nonprofit.html')
#         scores = ','.join([str(r.score) for r in reviews if r.page=='bacs200/projects/nonprofit.html'])
#         return student, reviews, "%d reviews, scores: %s" % (len(reviews), scores)
#
#     all_students = Course.students(course)
#     return [designer_summary(s) for s in all_students]
#
#
# def projects():
#     return len(Review.objects.all().distinct('due'))


# def review_groups(course):
#
#     groups = []
#     num = 8
#     s = Course.students(course)
#     shuffle(s)
#     x = 0
#     while s[x:x + num]:
#         groups.append(s[x:x + num])
#         x += num
#     # groups = [groups[0] + groups[-1]] + groups[1:-1]
#     return groups
#
#
# def review_pairs(groups):
#     x = []
#     for team in groups:
#         for reviewer in team:
#             for designer in team:
#                 if reviewer != designer:
#                     x.append((designer, reviewer))
#     print(len(x))
#     return x


def review_feedback(student_id):
    return Review.objects.filter(designer=student_id).exclude(score=-1)


def student_reviews(student_id):
    return Review.objects.filter(reviewer=student_id, score=-1)


def student_reviews_done(student_id):
    return Review.objects.filter(reviewer=student_id).exclude(score=-1)


# def url_feedback(answer, correct):
#     if answer == correct:
#         return 'smiley1.jpg'
#     else:
#         return 'sad1.jpg'
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
    *
    *
* Title, Author
    *
    *
* Link to class website 
    *
* Profile Photo
    *
* CSS Stylesheet (in separate file)
    *
* Banner with site title and tag line
    *
* Project table with page and validation links
    *
* Skills table with links to skills
    *
* Valid HTML
    *
* Valid CSS
    *
'''
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
    *
    *
* Title, Author
    *
    *
* Link to class website 
    *
* Profile Photo
    *
* CSS Stylesheet (in separate file)
    *
* Banner with site title and tag line
    *
* Links to project pages (planner, project, docman, superhero, subscriber, notes)
    *
* Skills table with links to skills
    *
* Valid HTML
    *
* Valid CSS
    *
'''

