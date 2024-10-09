from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='informatikunterricht',
    version='0.2.2',
    author='Henning Mattes',
    author_email='henning_mattes@gmx.de',
    description='Ein Paket für den Informatikunterricht, das Module zur Bildverarbeitung und Diagrammerstellung enthält.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/henningmattes/informatikunterricht',
    packages=find_packages(),
    install_requires=[
        'matplotlib',  
        'numpy',       
        'Pillow'       
    ],
    license='MIT with additional terms',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='bildung informatik bildverarbeitung diagramme informatikunterricht',
    package_data={
        '': ['LICENSE.txt', 'README.md', 'csedu_package_img_small.png']
    },
    include_package_data=True,
    python_requires='>=3.7',
)
