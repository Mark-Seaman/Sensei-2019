from django.core.mail import send_mail
from os import listdir, walk
from os.path import join, exists, isdir
from platform import node
from re import split
from subprocess import Popen, PIPE
from sys import version_info

from tool.text import text_join, text_lines


def banner(name):
    '''Show a banner for this file in the output'''
    return '\n%s\n%s%s\n%s\n' % ('-' * 80, ' ' * 30, name, '-' * 80)


def check_dirs(path, min=0, max=0):
    '''Count directories in a directory and compare to known limits'''
    if max==0:
        max = min
    dirs = dir_tree_list(path)
    num_dirs = len(dirs)
    if num_dirs < min or num_dirs > max:
        message = 'dirs(%s) --> %d dirs (should be between %d and %d)'
        return (message % (path, num_dirs, min, max))
    return ''


def check_dir_list(path, dir_list):
    '''Count directories in a list of directories and compare to known limits'''
    results = [check_dirs(join(path, d[0]), d[1], d[2] if d[2:] else 0) for d in dir_list]
    return '\n'.join(results)


def check_files(path, min=0, max=0):
    '''Count files in a directory and compare to known limits'''
    files = file_tree_list(path)
    num_files = len(files)
    if max==0:
        max = min
    if num_files < min or num_files > max:
        message = 'files(%s) --> %d files (should be between %d and %d)'
        return (message % (path, num_files, min, max))
    return ''


def check_file_list(path, dir_list):
    '''Count files in a list of directories and compare to known limits'''
    results = [check_files(join(path, d[0]), d[1], d[2] if d[2:] else 0) for d in dir_list]
    return '\n'.join(results)


def check_lines(label, lines, min=0, max=10):
    '''Verify the number of lines in text'''
    lines = lines.split('\n')
    if len(lines) < min or len(lines) > max:
        message = 'shell(%s) --> %d lines (should be between %d and %d)'
        return (message % (label, len(lines), min, max))


def check_shell_lines(cmd, min=0, max=10):
    '''Check for lines returned by the shell command output'''
    return check_lines(cmd, shell(cmd), min, max)


def curl_get(url):
    html = shell('curl -s %s' % url)
    return redact_css(html)


def redact_css(text):
    from tool.text import text_replace
    match = r'\.css\?.*">\n*'
    replacement = r'.css">\n'
    return text_replace(text, match, replacement)


def differences(answer, correct):
    '''   Calculate the diff of two strings   '''
    if answer != correct:
        t1 = '/tmp/diff1'
        t2 = '/tmp/diff2'
        with open(t1, 'wt') as file1:
            # print (answer)
            file1.write(str(answer) + '\n')
        with open(t2, 'wt') as file2:
            file2.write(str(correct) + '\n')
        diffs = shell('diff %s %s' % (t1, t2))
        if diffs:
            # print('Differences detected:     < actual     > expected')
            # print (diffs)
            return diffs


def dir_list(path):
    '''Return a list of directories in the directory'''
    if not exists(path):
        return ['No directory exists']
    return [d for d in listdir(path) if isdir(join(path,d))]


def dir_tree_list(path):
    '''Return a list of dirs in the directory tree'''
    dirs = []
    if not exists(path):
        return ['No directory exists']
    for root, dirnames, filenames in walk(path):
        if not '.git' in root:
            for filename in dirnames:
                dirs.append(join(root, filename))
    return dirs


def file_tree_list(path, filetype=None):
    '''Return a list of files in the directory tree (ignoring .git)'''
    files = []
    if not exists(path):
        return ['No directory exists']
    for root, dirnames, filenames in walk(path):
        if not '.git' in root:
            for filename in filenames:
                files.append(join(root, filename))
    return filter_types(files, filetype)


def file_list(path, filetype=None):
    '''Return a list of files in the directory'''
    if not exists(path):
        return ['No directory exists']
    files = listdir(file_path(path))
    if filetype:
        files = [f for f in files if f.endswith(filetype)]
    return files


def file_path(d='', f=''):
    '''Form a file path'''
    path = d
    if f:
        return join(path, f)
    return path


def filter_types(files, filetype=None):
    '''Select files of a certain type'''
    if filetype:
        files = [f for f in files if f.endswith(filetype)]
    return files


def hostname():
    '''Get the hostname of this computer'''
    return node()


def is_imac():
    return 'imac' in hostname() 

    
def is_macbook():
    return 'macbook' in hostname() 


def is_server():
    return hostname() == 'sensei-server'


def line_match(word, text):
    '''Find lines that contain text pattern'''
    return '\n'.join([x for x in text.split('\n') if word in x])


def line_exclude(word, text):
    '''Remove lines that contain a text pattern'''
    return '\n'.join([x for x in text.split('\n') if not word in x])


def line_count(path):
    '''Read a file and count the lines of text'''
    return len(read_file(path).split('\n'))


def lines(text):
    return text.split('\n')


def limit_lines(shell_command, min=None, max=None):
    '''Limit the lines to a certain number or echo all the output'''
    text = shell (shell_command)
    violation = check_lines(shell_command, text, min, max)
    if violation:
        text = text.split('\n')
        text = '\n'.join([line[:60] for line in text])
        return violation
    return ''


def read_file(path):
    '''Read a file and return the text'''
    if not exists(path):
        return 'Error:  File not found %s' % path
    try:
        if version_info.major == 3:
            return open(path).read()
        else:
            return open(path).read().decode(encoding='UTF-8').encode('ascii', 'ignore')
    except:
        return '**error**: Bad file read, %s' % path


def shell(command):
    '''Execute a shell command and return stdout'''
    return shell_script(command)


def no_blank_lines(text):
    text = text_lines(text)
    text = [x for x in text if x.strip() != '']
    text = text_join(text)
    return text


def send_email_test():
    send_mail(
        'Test Message from webserver',
        'Here is the message.',
        'mark.b.seaman@gmail.com',
        ['mark@seamanfamily.org'],
        fail_silently=False,
    )


def shell_file_list(path='.', filetype='', exclude_directories=[]):
    if filetype != '':
        filetype = '-name "*.%s"' % filetype
    exclude_dirs = ' '.join([("-not -path '*/%s/*'" % d) for d in exclude_directories])
    shell_command = 'find %s %s -type f %s' % (path, exclude_dirs, filetype)
    files = shell_script(shell_command)
    return no_blank_lines(files)


def shell_pipe(command, stdin=''):
    p = Popen(command, stdin=PIPE, stdout=PIPE)
    (out, error) = p.communicate(input=stdin.encode('utf-8'))
    if error:
        return error.decode('utf-8') + out.decode('utf-8')
    return out.decode('utf-8')


def shell_script(command_string):
    p = Popen('bash', stdin=PIPE, stdout=PIPE)
    (out, error) = p.communicate(input=command_string.encode('utf-8'))
    if error:
        return error.decode('utf-8') + out.decode('utf-8')
    return out.decode('utf-8')


def word_count(text):
    '''Count the lines of text'''
    return len(split('\s+', text))


def write_file(path, text):
    '''Save the text in the file'''
    try:
        open(path, 'w').write(text)
    except:
        return '**error**: Bad file write, %s' % path
