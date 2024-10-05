from setuptools import setup, find_packages

setup(
    name='DarkFream',
    version='1.0',
    description='DarkFream',
    author='vsp210',
    author_email=' psv449@yandex.ru',
    entry_points={
        'console_scripts': [
            'Dark=DarkFream.main:main',
        ],
    },
    # scripts=['DarkFream/app.py'],
    packages=find_packages(),
    data_files=[('DarkFream/templates', ['DarkFream/templates/index.html', 'DarkFream/templates/404.html'])],
    install_requires=['Jinja2>=3.1.4', 'MarkupSafe>=2.1.5', 'winotify>=1.1.0']
)
