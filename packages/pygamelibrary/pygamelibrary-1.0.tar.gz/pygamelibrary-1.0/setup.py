from setuptools import setup, find_packages

setup(
    name='pygamelibrary',  # 패키지 이름
    version='1.0',  # 버전
    author='Eun ho Kim',  # 저자
    author_email='miss6815@naver.com',  # 이메일
    description='my python game library',  # 설명
    long_description=open('README.md').read(),  # README 파일 내용
    long_description_content_type='text/markdown',  # README 형식
    url='https://github.com/yourusername/your_package',  # 프로젝트 URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',  # Python 버전 요구 사항
)