from django.template.loader import render_to_string

from mybook.mybook import document_text
from tool.document import text_to_html
from unc.bacs import weekly_lessons
from unc.projects import get_readings, get_assignments, get_lesson
from unc.models import Skill
from unc.review import review_feedback, student_reviews, student_reviews_done, get_review


def render_course_agenda(course, student):
    weeks = weekly_lessons(course)
    return [(w['week'], render_weekly_agenda(w, student)) for w in weeks]


def render_homework_scorecard(student):
    title = '%s Homework Scorecard' % student.name
    return render_to_string('homework.html',
                            dict(title=title, assignments=get_readings(student) + get_assignments(student)))


def render_lesson(lesson):
    return render_to_string('lesson.html', dict(lesson=lesson))


def render_lessons(lessons):
    return ''.join([render_lesson(lesson) for lesson in lessons])


def render_notes(review):
    return text_to_html(review.notes)


def render_project(project, student):
    skills = render_skills(student)
    return render_to_string('project.html', dict(project=project, skills=skills, student=student))


def render_review(review_id):
    review = get_review(review_id)
    return dict(title='Design Review',
                review=review,
                requirements=requirements_met(review),
                notes=render_notes(review))


def render_reviews(student):
    reviews_to_do = student_reviews(student.pk)
    reviews_done = student_reviews_done(student.pk)
    feedback = review_feedback(student.pk)
    return render_to_string('review.html',
                            dict(student=student,
                                 reviews_to_do=reviews_to_do,
                                 reviews_done=reviews_done,
                                 review_feedback=feedback))


def render_skills(student):
    skills = Skill.query(student.course.name)
    skills = [dict(num="%02d" % s.num, skill=s, images=s.images.split(',')) for s in skills]
    return render_to_string('skills.html', dict(skills=skills, student=student))


def render_skill_link(lesson, student):
    skill = '<a href="/unc/%s/skills/%02d" target="lesson">Skill #%s</a>' % \
            (student.course.name, lesson.lesson, lesson.lesson)
    return render_to_string('skill.html', dict(lesson=lesson, skill=skill, student=student))


def render_skill_doc(doc_path, student):
    course = student.course.name
    image_path = '/static/images/unc/bacs200' if 'bacs200' == course else '/static/images/unc/bacs350'
    text = document_text(doc_path, image_path)
    skills_path = '%s/%s/%s' % (student.domain, course, 'skills')
    text = text.replace('{{ skills }}', skills_path)
    return text


def render_student_info(student):
    return render_to_string('student.html', dict(student=student))


def render_weekly_agenda(plan, student):
    project = render_project(plan['project'], student)
    lessons = render_lessons(plan['lessons'])
    weekly_plan = dict(week=plan['week'], project=project, lessons=lessons)
    return render_to_string('week.html', weekly_plan)


def requirements_met(review):
    def status(req):
        return '<span class="green">PASS</span>' if req else '<span class="red blinking">FAIL</span><b></b>'

    status = [status(review.requirement_1), status(review.requirement_2), status(review.requirement_3),
              status(review.requirement_4), status(review.requirement_5), status(review.requirement_6),
              status(review.requirement_7), status(review.requirement_8), status(review.requirement_9),
              status(review.requirement_10)]
    labels = [r.strip() for r in review.requirement_labels.split('\n')]
    return zip(labels, status)


