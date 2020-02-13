from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author="T Belcher",
    author_email="tbelcher@verizon.net",
    description="Webotron 80 is a tool to deploy static websites to AWS",
    license="GPLv3+",
    packages=['webotron'],
    url="https://github.com/TJBelcher/automating-aws-with-python",
    install_requres=[
        'click',
        'boto3',
        'pprint'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)
