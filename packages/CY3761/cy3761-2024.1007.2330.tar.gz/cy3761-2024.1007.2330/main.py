# CY3761 | fb764bc@foxmail.com | 2024-09-30 08:52 | main.py
# ----------------------------------------------------------------------------------------------------
from datetime import datetime
from platform import python_version
from pathlib import Path
from typing import Union
from re import sub
from toml import load, dump  # # pip install toml
from subprocess import check_output
from os import listdir

# ----------------------------------------------------------------------------------------------------
S010, S114, S119 = '\n', 'r', 'w'

# ----------------------------------------------------------------------------------------------------
T000 = Union[Path, str]
T001 = Union[S114, S119]
# ----------------------------------------------------------------------------------------------------
p000 = Path(__file__).parent
p001 = p000 / 'template'
p002 = 'LICENSE', 'pyproject.toml', 'README.md'
p003 = [p001 / v for v in p002]
p004, p005, p006 = p003
# ----------------------------------------------------------------------------------------------------
n003 = [p000 / v.name for v in p003]
n004, n005, n006 = n003
# ----------------------------------------------------------------------------------------------------
e00 = 'utf-8'


# ----------------------------------------------------------------------------------------------------

def _open(_0: T000, _1: T001 = S114, _2: str | dict = ''):
    v00 = Path(_0)
    v01 = _1
    v02 = _2
    v03 = v01 == S114  # r
    v04 = v00.suffix == p002[1][-5:]

    if v03 and v04:
        return load(v00)

    with v00.open(v01, encoding=e00) as i0:
        if v03:
            return i0.read()
        else:
            return dump(v02, i0) if v04 else i0.write(v02)


def read(v00: T000):
    return _open(v00, S114)


def save(v00: T000, v01: str):
    return _open(v00, S119, v01)


# ----------------------------------------------------------------------------------------------------
r004, r005, r006 = [read(v) for v in p003]
r007 = r005.get('project', {})

r008 = {
    'version': datetime.now().strftime("%Y.%m%d.%H%M"),
    'requires-python': '>=%s' % python_version(),
    'description': '%s的软件包' % r007.get('name')
}

r007.update(r008)


# ----------------------------------------------------------------------------------------------------
# LICENSE | 4 |  一般无需更新
def build_00():
    return save(n004, r004)


# pyproject.toml | 5
# 版本号更新 (项目版本与环境版本) | r005 完整数据
def build_01():
    save(n005, r005)


# README.md | 6
# 版本号更新 (项目版本与环境版本) | r005 完整数据
def build_02():
    p00 = r'(## %s)'  # ## 2号标题
    p01 = r'\g<1>\n'  # 直接 /1 如果替换字符是数字开头,会被转义
    p02 = r'+ %s: %s'

    v00 = r005.get('project', {})
    v01 = r006

    v01 = sub(p00 % '项目信息', p01 + S010.join([
        p02 % (_0, _1) for _0, _1 in [
            ('项目名称', v00.get('name')),
            ('项目作者', '{name} {email}'.format(**v00.get('authors')[0])),
            ('项目版本', v00.get('version')),
            ('环境版本', v00.get('requires-python')),
        ]
    ]), v01)

    # print(v01)

    v01 = sub(p00 % '依赖项目', p01 + S010.join(v00.get('dependencies')), v01)

    return save(n006, v01)


def clear():
    v00 = Path('./dist')

    [(v00 / v).unlink() for v in listdir(v00)]


def run(code: str, cwd='./', encoding=e00):
    return check_output('python -m ' + code, shell=True, cwd=cwd).decode(encoding)
    # The username to authenticate to the repository (package index) as. (Can also be set via TWINE_USERNAME environment variable.)
    # The password to authenticate to the repository (package index) with. (Can also be set via TWINE_PASSWORD environment variable.)


# python -m build
def run_build():
    return run('build')


def run_twine(*args):
    return run('twine ' + ' '.join(args))


# python -m twine upload dist/* -r pypi -p <token>
def run_upload(password: int, repository='pypi'):
    password = read(p001 / 'PASSWORD').split('\n')[password]

    # print(password)
    return run_twine('upload', '--repository ' + repository, 'dist/*', '-p ' + password)

    # return run_twine('upload', 'dist/*', *[
    #     '-%s %s' % (_0, _1) for _0, _1 in [
    #         ('r', repository),
    #         ('p', password),
    #     ]
    # ])

# ----------------------------------------------------------------------------------------------------
def main():
    build_00()
    build_01()
    build_02()

    clear()

    print(run_build())
    print(run_upload(1))

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
