import nox

nox.options.sessions = ['lint', 'tests']
nox.options.reuse_existing_virtualenvs = True


@nox.session
def tests(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '--cov-report', 'term', '--cov=dependencynet')


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


# scenarios

@nox.session
def tests_fanout(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'fanout')


@nox.session
def tests_journey(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'journey')


@nox.session
def tests_towns(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'towns')


@nox.session
def tests_trips(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'trips')


@nox.session
def tests_twolevels(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'twolevels')


# api

@nox.session
def tests_api_schema(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'schema')


@nox.session
def tests_api_model(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'model')


@nox.session
def tests_api_graph_model(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'graph_model')


@nox.session
def tests_api_graph_style(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'graph_style')


@nox.session
def tests_api_graph_viewer(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'graph_viewer')


@nox.session
def tests_api_graphml(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'graphml')
    # session.run('pytest', '--pyargs', 'tests.api.graphml')


# core functions

@nox.session
def tests_core(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '-m', 'core')


# notebooks

@nox.session
def tests_notebooks(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov', 'pytest-notebook')
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '--nb-test-files')


@nox.session
def lint_notebooks(session):
    # flakehell requieres toml
    # session.install('flake8', 'flakehell')
    # session.run(
    #        'flakehell',
    #        'lint',
    #        './notebooks/')
    session.install('nblint')
    session.install('--quiet', '-r', 'requirements.txt')

    import os
    for root, dirs, files in os.walk('./notebooks/'):
        if 'output' not in root:
            for name in files:
                if name.endswith('.ipynb'):
                    if 'checkpoint' not in name:
                        filename = os.path.join(root, name)
                        session.run(
                                'nblint',
                                '--linter',
                                'pyflakes',
                                filename)
    # TODO ignore magic


@nox.session
def check_notebooks(session):
    session.install('nbconvert')
    session.install('--quiet', '-r', 'requirements.txt')
    import os
    for root, dirs, files in os.walk('./notebooks/'):
        if 'output' not in root:
            for name in files:
                if name.endswith('.ipynb'):
                    if 'checkpoint' not in name:
                        filename = os.path.join(root, name)
                        session.run(
                                'jupyter',
                                'nbconvert',
                                '--to',
                                'notebook',
                                '--execute',
                                '--output',
                                'check',
                                filename)
