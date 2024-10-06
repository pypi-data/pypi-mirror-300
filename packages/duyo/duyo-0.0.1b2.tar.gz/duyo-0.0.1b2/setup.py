from setuptools import setup, find_packages

setup(
    name="duyo",
    version="0.0.1b2",
    packages=find_packages(exclude=[]),
    install_requires=[
    ],
    license="",
    description="duyo modules",  # 간단한 설명
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="westsea314",
    author_email="westsea314@gmail.com",
    url="https://github.com/westsea314/duyo",
    keywords=['duyo', 'duyo module', 'duyo-kr'],
    # python_requires='>=3.6',          # 최소 Python 버전
    package_data={},
    classifiers=[                     # 패키지 관련 메타데이터
    ],
)