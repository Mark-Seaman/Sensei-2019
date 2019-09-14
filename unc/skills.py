from unc.models import Skill


def build_skills():
    Skill.create('bacs200', 1, 'Web Hosting',   '2019-09-16')
    Skill.create('bacs200', 2, 'FTP',           '2019-09-16')
    Skill.create('bacs350', 1, 'Web Hosting',   '2019-09-16')
    Skill.create('bacs350', 2, 'FTP',           '2019-09-16')


def print_skills(course):
    return '\n'.join(Skill.list(course))


def update_skills():
    build_skills()
    return print_skills('bacs350') + '\n' + print_skills('bacs200')
