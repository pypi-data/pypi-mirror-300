from setuptools import setup , find_packages


setup(
        name='snapsort',
        version='0.1.0',
        author='Haseen',
        author_mail='matharhaseen18@gmail.com',
        description='A CLI tool built in python to segregate people in the group photos .',
        packages=find_packages(),
        entry_points={
        'console_scripts': [
            'snapsort=snapsort:snap',  # Replace with your actual command and main function
        ],
    },
        install_requires=[
            'ultralytics==8.3.5',
            'opencv-python==4.10.0.84',
            'tqdm==4.66.5',
            'tf_keras==2.17.0',
            'tensorflow==2.17.0',
            'deepface==0.0.93',
            'matplotlib==3.7.1',
            ]



        )
