from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='deauthorized django starter app',
    version='0.1.1',
    description='Deauthorized Django Starter App',
    url='https://github.com/Deauthorized/django_openidconnect_starter_app',
    author='Deauthorized',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Authentication',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='biometric authentication u2f fido',
    packages=find_packages(),
    install_requires=['pyoidc', 'django', 'requests',
                      'pytest', 'pytest-django']
)
