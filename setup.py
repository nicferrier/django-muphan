from setuptools import setup

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities',
]

setup(
    name = "muphan",
    version = "0.1",
    author = "Nic Ferrier",
    author_email = "nferrier@ferrier.me.uk",
    description = "A mediahub app to take away drudgery of doing file upload.",
    license = "GPLv2",
    keywords = "django web file upload photo",
    url = "http://github.com/nicferrier/django-muphan",
    packages=['muphan'],
    requires=['django'],
    long_description="""An app that you can use to upload and serve
media files such as photos.""",
    classifiers=classifiers,
)
