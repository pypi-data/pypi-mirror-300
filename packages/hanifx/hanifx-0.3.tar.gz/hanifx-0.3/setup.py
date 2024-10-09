from setuptools import setup, find_packages

setup(
    name='hanifx',
    version='0.3',
    packages=find_packages(),
    description='A package for creating custom logos using the Pillow library',
    long_description="""\
This package provides functionality to create custom logos using the Pillow library. 
You can specify the text, dimensions, background color, and text color for your logo. 
The resulting logo is saved as a PNG file with the specified text in the center. 
This is useful for generating custom logos for projects, personal branding, or any other creative purposes.
""",
    author='Hanif',
    author_email='sajim4653@gmail.com',
    url='https://hanif-storess.weebly.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Pillow',
    ],
    include_package_data=True,
    zip_safe=False,
)
