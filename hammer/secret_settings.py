from platform import node

if 'seaman-' in node() or 'sws-' in node() or 'iMac' in node():

# Development server settings

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 
            'NAME': 'hammer/sensei.db',  # Database file
            'USER': '',            # Not used with sqlite3.
            'PASSWORD': '',        # Not used with sqlite3.
            'HOST': '',            # Set to empty string for localhost. 
            'PORT': '',            # Set to empty string for default. 
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'sensei',
            'USER': 'sensei',
            'PASSWORD': 'MS1959-li',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$itxljw#m_u#=)av=e4s-yrl^yc%z39m$whh%hej54z_n8^@q4'

'''
Create a super user

$ dj createsuperuser --username MarkSeaman --email mark.b.seaman@gmail.com
'''


# Django Email Settings

# GMAIL - fails

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'mark.b.seaman@gmail.com'
# EMAIL_HOST_PASSWORD = 'MS1959-gmail'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

# Bluehost - fails

# EMAIL_HOST = 'mail.unco-bacs.org'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'uncobacs'
# EMAIL_HOST_PASSWORD = 'MS1959-bh'
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
