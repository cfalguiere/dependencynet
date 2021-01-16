import nox


@nox.session
def tests(session):
    session.install('pytest')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest')


@nox.session
def lint(session):
    session.install('flake8')
    session.run(
            'flake8',
            '--exclude=.git,__pycache__,.nox,.pytest_cache,target',
            '--select=W,E112,E113,F,C9,N8',
            '--ignore=E501,I202,F401,F841',
            '--show-source',
            '.', 'noxfile.py')
