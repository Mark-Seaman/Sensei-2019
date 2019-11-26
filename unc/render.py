from django.template.loader import render_to_string

from mybook.mybook import document_text
from tool.document import text_to_html
from unc.bacs import weekly_lessons
from unc.projects import get_readings, get_assignments
from unc.models import Lesson, Skill, Project
from unc.review import review_feedback, student_reviews, student_reviews_done, get_review


def render_course_agenda(course, student):
    weeks = weekly_lessons(course)
    return [(w['week'], render_weekly_agenda(w, student)) for w in weeks]


def render_homework_data(student, **kwargs):
    kwargs['student'] = student
    kwargs['weeks'] = render_course_agenda(student.course.name, student)
    kwargs['student_info'] = render_student_info(student)
    kwargs['homework'] = render_homework_scorecard(student)
    kwargs['skills'] = render_skills(student)
    kwargs['reviews'] = render_reviews(student)
    kwargs['projects'] = render_projects(Project.list(student.course.name))
    return kwargs


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


def render_overview(course):
    lessons = Lesson.list(course)
    projects = Project.list(course)
    skills = Skill.list(course)
    data = dict(course=course, lessons=lessons, projects=projects, skills=skills)
    return render_to_string('overview.html', data)


def render_project(student, project):
    skills = render_skills(student)
    return render_to_string('project.html', dict(project=project, skills=skills, student=student))


def render_projects(student):
    projects = Project.list(student.course.name)
    return render_to_string('projects.html', dict(projects=projects, student=student))


def render_review(review_id):
    review = get_review(review_id)
    return dict(title='Design Review',
                review=review,
                requirements=requirements_met(review),
                notes=render_notes(review))


def render_review_list(text, reviews, **options):
    data = dict(description=text, reviews=reviews)
    data.update(options)
    return render_to_string('review.html', data)


def render_reviews(student):
    to_do_text = '''
         The following reviews are scheduled to be completed by the due date. You will only 
         get credit if the review is done correctly and on time.
         '''
    done_text = '''
         You have completed these reviews.  You can updated them at any time with new information
         '''
    feedback_text = '''
         These reviews are for feedback on your design work.
         '''
    reviews_to_do = render_review_list(to_do_text, student_reviews(student.pk), edit=True)
    reviews_done = render_review_list(done_text, student_reviews_done(student.pk), edit=True, score=True)
    feedback = render_review_list(feedback_text, review_feedback(student.pk), show=True, score=True)

    todo_data = [0, 'Reviews To Do', reviews_to_do, 'active']
    done_data = [1, 'Reviews Done', reviews_done, '']
    feedback_data = [2, 'Design Feedback', feedback, '']

    data = dict(student=student, reviews=[todo_data, done_data, feedback_data])
    return render_to_string('reviews.html', data)


def render_skills(student):
    skills = Skill.list(student.course.name)
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
    project = render_project(student, plan['project'])
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
