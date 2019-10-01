from unc.models import Skill


def build_skills():
    Skill.create('bacs200', 1, 'Web Hosting',   '2019-09-16', 'bluehost.png,wordpress.png')
    Skill.create('bacs200', 2, 'FTP',           '2019-09-16', 'ftp-site-manager.png,ftp-dirs.png,ftp-files.png')
    Skill.create('bacs200', 3, 'Brackets',      '2019-09-20', 'brackets.png')
    Skill.create('bacs200', 4, 'URL Game',      '2019-09-23', 'urlgame.png')
    Skill.create('bacs200', 5, 'Validate HTML', '2019-09-30', 'validator-ok.png,validator-link.png')

    Skill.create('bacs350', 1, 'Web Hosting',   '2019-09-16', 'bluehost.png,wordpress.png')
    Skill.create('bacs350', 2, 'FTP',           '2019-09-16', 'ftp-site-manager.png,ftp-dirs.png,ftp-files.png')
    Skill.create('bacs350', 3, 'Github',        '2019-09-16', 'git-files.png,git-changes.png')
    Skill.create('bacs350', 4, 'Share Code',    '2019-09-20', 'git-pull.png')
    Skill.create('bacs350', 5, 'Apache',        '2019-09-25', 'apache.png')
    Skill.create('bacs350', 6, 'Database',      '2019-10-02', 'database.png')


def print_skills(course):
    return '\n'.join(Skill.list(course))


def update_skills():
    build_skills()
    return print_skills('bacs350') + '\n' + print_skills('bacs200')
