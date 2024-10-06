from setuptools import setup, find_packages

setup(
    name='ahui626_test',  # 包名
    version='0.1',  # 版本号
    packages=find_packages(),
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ahui',
    author_email='your.email@example.com',
    # url='https://github.com/yourusername/my_package',  # 项目链接（可选）
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 在此处添加任何依赖项，例如
        'requests',
    ],
)
