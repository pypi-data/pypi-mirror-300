from setuptools import setup, find_packages

setup(
    name='subseq_tamil',  # Name of your package
    version='0.1.6',  # Incremented version
    packages=find_packages(where='src'),  # Specify the source directory
    package_dir={'': 'src'},  # Indicate that packages are under src
    install_requires=[     # List of dependencies
        # 'numpy',  # Uncomment and add your dependencies here
    ],
    author='Your Name',    # Your name
    author_email='your_email@example.com',  # Your email
    description='A brief description of your package',  # Package description
    long_description=open('README.md').read(),  # Long description from README file
    long_description_content_type='text/markdown',  # Markdown type for long description
    url='https://github.com/yourusername/subseq_tamil',  # URL to the package repository
    classifiers=[          # Classifiers for package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
