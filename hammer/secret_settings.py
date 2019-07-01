from platform import node

if 'seaman-' in node() or 'sws-' in node() or 'iMac' in node():

# Development server settings

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 
            'NAME': 'db.sqlite3',  # Database file
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

