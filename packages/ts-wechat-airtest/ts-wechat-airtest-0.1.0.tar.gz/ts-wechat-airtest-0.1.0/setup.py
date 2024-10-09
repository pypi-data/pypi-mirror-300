from setuptools import setup, find_packages

setup(
    name='ts-wechat-airtest',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'airtest'
    ],
    author='LiQiang',
    author_email='liqiang944@jd.com',
    description='基于airtest的公共包',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
