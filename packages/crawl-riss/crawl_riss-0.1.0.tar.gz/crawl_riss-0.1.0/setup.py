from setuptools import setup, find_packages

setup(
    name='crawl_riss',  # 패키지 이름
    version='0.1.0',  # 패키지 버전
    description='A package for crawling papers from RISS',
    author='길완제 Wan Je Gil',
    author_email='jaygil8755@gmail.com',
    url='https://github.com/jaygil8755/crawl_riss',  # GitHub 리포지토리 링크
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'tqdm',
        'time',
        'openpyxl',
    ],
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
