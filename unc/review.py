from django.utils.timezone import make_aware
from datetime import datetime
from random import shuffle

from unc.models import Course, Review


def assign_reviews(course, page, due, requirements):
    pairs = review_pairs(review_groups(course))
    for p in pairs:
        create_review(p[0], p[1], page, due, requirements)
    return len(pairs)


def count_score(r):
    requirements = [r.requirement_1, r.requirement_2, r.requirement_3, r.requirement_4, r.requirement_5,
                    r.requirement_6, r.requirement_7, r.requirement_8, r.requirement_9, r.requirement_10]
    return len([x for x in requirements if x])


def create_review(reviewer, designer, page, due, requirements):
    due = '%s 23:59' % due
    due = make_aware(datetime.strptime(due, "%Y-%m-%d %H:%M"))
    return Review.objects.get_or_create(reviewer=reviewer, designer=designer, page=page, due=due,
                                        requirement_labels_id=requirements, requirements='NONE')[0]


def get_review(id):
    return Review.objects.get(pk=id)


def query_reviewers(course):

    def reviewer_summary(student):
        student_id = student.pk
        reviews = student_reviews_done(student_id)
        not_done = student_reviews(student_id)
        assigned = len(reviews) + len(not_done)
        rounds = 13
        points = 10 * rounds * len(reviews) / assigned
        return student, reviews, "%d done of %d assigned, score = %d" % (len(reviews), assigned, points)

    all_students = Course.students(course)
    return [reviewer_summary(s) for s in all_students]


def query_designers(course):

    def designer_summary(student):
        student_id = student.pk
        reviews = review_feedback(student_id).filter(page='bacs200/projects/nonprofit.html')
        scores = ','.join([str(r.score) for r in reviews if r.page=='bacs200/projects/nonprofit.html'])
        return student, reviews, "%d reviews, scores: %s" % (len(reviews), scores)

    all_students = Course.students(course)
    return [designer_summary(s) for s in all_students]


def projects():
    return len(Review.objects.all().distinct('due'))


def review_feedback(student_id):
    return Review.objects.filter(designer=student_id).exclude(score=-1)


def review_groups(course):

    groups = []
    num = 8
    s = Course.students(course)
    shuffle(s)
    x = 0
    while s[x:x + num]:
        groups.append(s[x:x + num])
        x += num
    # groups = [groups[0] + groups[-1]] + groups[1:-1]
    return groups


def review_pairs(groups):
    x = []
    for team in groups:
        for reviewer in team:
            for designer in team:
                if reviewer != designer:
                    x.append((designer, reviewer))
    print(len(x))
    return x


def student_reviews(student_id):
    return Review.objects.filter(reviewer=student_id, score=-1)


def student_reviews_done(student_id):
    return Review.objects.filter(reviewer=student_id).exclude(score=-1)


def url_feedback(answer, correct):
    if answer == correct:
        return 'smiley1.jpg'
    else:
        return 'sad1.jpg'