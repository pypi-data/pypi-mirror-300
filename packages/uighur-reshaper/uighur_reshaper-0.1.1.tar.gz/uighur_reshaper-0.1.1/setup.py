from setuptools import setup, find_packages

setup(
    name='uighur_reshaper',
    version='0.1.1',  # 提升版本号
    author='Sulayman',
    author_email='Sulayman@eotor.net',
    description='一个用于维吾尔语文本转换扩展区的Python工具',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sulayman/uighur_reshaper',
    packages=find_packages(),  # 这会找到你的 uighur_reshaper 包
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='维吾尔语文本转扩展区',
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'uighur_reshaper=uighur_reshaper.shaper:uighur_reshaper',
        ],
    },
)
