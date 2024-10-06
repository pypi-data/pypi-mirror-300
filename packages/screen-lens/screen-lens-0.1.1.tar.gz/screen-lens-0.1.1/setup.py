from setuptools import setup

setup(
    name='screen-lens',
    version='0.1.1',
    py_modules=['screen_lens_wrapper'],
    scripts=['screen_lens.sh'],
    entry_points={
        'console_scripts': [
            'screen-lens=screen_lens_wrapper:run_shell_script',
        ],
    },
    include_package_data=True,
    description='Perform Google Lens search by taking a simple screenshot from anywhere in your system.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sanchit Tanwar',
    author_email='connectwithme@sanchittanwar7.in',
    url='https://github.com/sanchittanwar7/screen-lens',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Unix Shell',
    ],
)
