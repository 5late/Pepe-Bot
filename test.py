from os import path

if path.exists('main.py') and path.exists('github.py'):
    print('The two main files are found. Linting complete.')
else:
    exit(code=1)