from csv import reader

from unc.models import Skill
from tool.text import as_text
from tool.days import date_str, due_date


def add_skill(course, num, topic, due, images):
    s = Skill.lookup(course, num)
    s.topic = topic
    s.due = due_date(due)
    s.images = images
    s.save()
    return s


def skills_csv(course):
    return 'Documents/unc/%s/skills.csv' % course


def list_skills(course):
    return as_text(Skill.list(course))


def export_skills(course):
    with open(skills_csv(course), 'w') as f:
        for x in Skill.list(course):
            text = ','.join([course, str(x.num), x.topic, date_str(x.due), x.images])
            f.write("%s\n" % text)


def import_skills(course):
    Skill.list(course).delete()
    with open(skills_csv(course)) as f:
        for row in reader(f):
            if len(row) > 4:
                add_skill(row[0], row[1], row[2], row[3], row[4])



# def print_skills(course):
#     return '\n'.join(Skill.list(course))
#
# def update_skills():
#     Skill.create('bacs200', 1, 'Web Hosting', '2019-09-16', 'bluehost.png,wordpress.png')
#     Skill.create('bacs200', 2, 'FTP', '2019-09-16', 'ftp-site-manager.png,ftp-dirs.png,ftp-files.png')
#     Skill.create('bacs200', 3, 'Brackets', '2019-09-20', 'brackets.png')
#     Skill.create('bacs200', 4, 'URL Game', '2019-09-23', 'urlgame.png')
#     Skill.create('bacs200', 5, 'Validate HTML', '2019-09-30', 'validator-ok.png,validator-link.png')
#     Skill.create('bacs200', 6, 'Developer Tools', '2019-10-04', 'devtools.png')
#     Skill.create('bacs200', 7, 'New Page Template', '2019-10-09', 'newpage.png,article.png')
#     Skill.create('bacs200', 8, 'Using Bootstrap', '2019-10-16', 'bootstrap.png,tabs.png,accordion.png')
#     Skill.create('bacs200', 9, 'Version Control', '2019-10-21', 'git-files.png,git-changes.png,git-push.png')
#     Skill.create('bacs200', 10, 'Create Images', '2019-10-30', 'me.png,logo.svg')
#     Skill.create('bacs200', 11, 'Teach a Skill', '2019-11-04', 'teach.png')
#     Skill.create('bacs200', 12, 'Design Diagrams', '2019-11-11', 'layout.png,structure.png,wireframe.png')
#
#     Skill.create('bacs350', 1, 'Web Hosting', '2019-09-16', 'bluehost.png,wordpress.png')
#     Skill.create('bacs350', 2, 'FTP', '2019-09-16', 'ftp-site-manager.png,ftp-dirs.png,ftp-files.png')
#     Skill.create('bacs350', 3, 'Github', '2019-09-16', 'git-files.png,git-changes.png')
#     Skill.create('bacs350', 4, 'Share Code', '2019-09-20', 'git-pull.png')
#     Skill.create('bacs350', 5, 'Apache', '2019-09-25', 'apache.png')
#     Skill.create('bacs350', 6, 'Database', '2019-10-02', 'database.png')
#     Skill.create('bacs350', 7, 'Dev Workflow', '2019-10-09', 'workflow.png,crud.png')
#     Skill.create('bacs350', 8, 'Data Views', '2019-10-16', 'list.png,add.png,edit.png')
#     Skill.create('bacs350', 9, 'Logging', '2019-10-21', 'logging.png')
#     Skill.create('bacs350', 10, 'Render Templates', '2019-10-28', 'home.png')
#     Skill.create('bacs350', 11, 'MVC Design Pattern', '2019-11-04', 'mvc.png')
#     # Skill.create('bacs350', 12, 'Users', '2019-11-15', 'users.png')
#
#     return print_skills('bacs350') + '\n' + print_skills('bacs200')
