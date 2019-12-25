from setuptools import setup, find_packages

requirements = [
    'cached-property',
    'logical-func>=1.2',
    'returns-decorator',
]

extra_http = [
    'requests',
]
extra_s3 = [
    'boto3>=1.9',
    'botocore',
]
extra_sql = [
    'sqlalchemy',
]
extra_bin = [
    *extra_http,
    *extra_s3,
]
extra_all = [
    *extra_http,
    *extra_s3,
    *extra_sql,
]

extra_test = [
    'pytest>=4',
    'pytest-runner>=4',
    'pytest-cov>=2',
    *extra_sql,
]
extra_dev = [
    *extra_all,
    *extra_test,
]

extra_ci = [
    *extra_test,
    'python-coveralls',
]

setup(
    name='python-stream',

    version='dev',

    python_requires='>=3.6',

    install_requires=requirements,

    extras_require={
        's3': extra_s3,
        'http': extra_http,
        'sqlalchemy': extra_sql,

        'bin': extra_bin,
        'all': extra_all,

        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    packages=find_packages(),

    url='https://github.com/MichaelKim0407/python-stream',
    author='Michael Kim',

    entry_points={
        'console_scripts': [
            's3-upload=stream.io.s3:upload_cmd',
            's3-download=stream.io.s3:download_cmd',
            's3-get=stream.io.s3:get_cmd',
            's3-copy=stream.io.s3:copy_cmd',
            'ftp-download=stream.io.ftp:download_cmd',
            'ftp-get=stream.io.ftp:get_cmd',
            'http-download=stream.io.http:download_cmd',
            'http-get=stream.io.http:get_cmd',
        ],
    },
)
