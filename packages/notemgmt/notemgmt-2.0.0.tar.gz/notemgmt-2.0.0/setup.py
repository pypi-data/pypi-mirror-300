from setuptools import setup

setup(name="notemgmt",
    version="2.0.0",
    description="a note management tool",
    url="https://github.com/VinitraMk/notemgmt",
    author="Vinitra Muralikrishnan",
    author_email="vinitramk@gmail.com",
    license="GNU",
    packages=["notemgmt"],
    entry_points = {
        'console_scripts': [
            'create_lecture_note=notemgmt.create_lecture_note:main',
            'create_answer_note=notemgmt.create_answer_note:main'
        ]
    },
    zip_safe=False
)
