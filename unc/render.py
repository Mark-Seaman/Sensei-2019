from django.template.loader import render_to_string

from mybook.mybook import document_text
from unc.bacs import weekly_lessons
from unc.projects import get_readings, get_assignments, get_lesson


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


def render_project(project, student):
    skills = [
        render_skill_link(get_lesson(project.course.name, 1), student),
        render_skill_link(get_lesson(project.course.name, 2), student),
    ]
    return render_to_string('project.html', dict(project=project, skills=skills, student=student))


def render_skill_link(lesson, student):
    skill = '<a href="/unc/%s/skills/%02d" target="lesson">Skill #%s</a>' % \
            (student.course.name, lesson.lesson, lesson.lesson)
    return render_to_string('skill.html', dict(lesson=lesson, skill=skill, student=student))


def render_skill_doc(doc_path, student):
    course = student.course.name
    image_path = '/static/images/unc/bacs200' if 'bacs200' == course else '/static/images/unc/bacs350'
    text = document_text(doc_path, image_path)
    skills_path = '%s/%s/%s' % ('https://unco-bacs.org', 'bacs350', 'skills')
    text = text.replace('{{ skills }}', skills_path)
    return text


def render_student_info(student):
    return render_to_string('student.html', dict(student=student))


def render_weekly_agenda(plan, student):
    project = render_project(plan['project'], student)
    lessons = render_lessons(plan['lessons'])
    weekly_plan = dict(week=plan['week'], project=project, lessons=lessons)
    return render_to_string('week.html', weekly_plan)


