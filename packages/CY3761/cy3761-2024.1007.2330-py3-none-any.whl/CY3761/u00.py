# CY3761 | fb764bc@outlook.com | 2024-10-02 17:28 | u00.py
# ----------------------------------------------------------------------------------------------------
from pathlib import Path
from io import TextIOWrapper
from collections.abc import Callable
from json import load, dump

# ----------------------------------------------------------------------------------------------------
T000 = Path | str  # Path
T001 = bytes | str | None  # io.write
# ----------------------------------------------------------------------------------------------------
M000, M001, M002, M003, M004 = 'r', 'w', 'a', 'b', 't'

# ----------------------------------------------------------------------------------------------------
D000 = None
D001 = 'utf-8'
D002 = M000
D003 = M003
# ----------------------------------------------------------------------------------------------------
D900 = dict(
    read=M000,
    save=M001,
    push=M002,
)
D901 = dict(
    bytes=M003,
    text=M004,
    json=M004,
    code=M004,
)


# ----------------------------------------------------------------------------------------------------
def open_decorator(*r_args, **r_kwargs):
    def decorator(func: Callable):
        d00 = str(func.__name__)
        d01, d02 = d00.split('_', 1)
        d03 = D900.get(d01, D002)
        d04 = D901.get(d02, D003)
        d05 = d03 + d04

        # print(d01, d02, d03, d04, d05)

        def wrapper(
                w00: T000,
                w01: T001 = D000,  # io.write
                *w_args,
                **w_kwargs
        ):
            v00 = Path(w00)
            v01 = d05  # mode
            v02 = w01  # io.write
            v03 = w_kwargs.get('encoding', D001)
            v03 = D000 if d03 == D003 else v03

            # print(59, v00, v01, v02, v03)

            with v00.open(v01, encoding=v03) as io:
                r00 = func(io, v02)

            return r00

        return wrapper

    return decorator


def read(v00: TextIOWrapper):
    return v00.read()


def save(v00: TextIOWrapper, v02: T001):
    return v00.write(v02)


# ----------------------------------------------------------------------------------------------------
@open_decorator()
def read_bytes(v00: T000, *args) -> bytes:
    v10: TextIOWrapper = v00

    return read(v10)


@open_decorator()
def save_bytes(v00: T000, v02: bytes) -> int:
    v10: TextIOWrapper = v00
    v11: bytes = v02

    return save(v10, v11)


@open_decorator()
def push_bytes(v00: T000, v02: bytes) -> int:
    v10: TextIOWrapper = v00
    v11: bytes = v02

    return save(v10, v11)


def chunk(v00: T001, v01: int = 1):
    return [v00[i:i + v01] for i in range(0, len(v00), v01)]


# ----------------------------------------------------------------------------------------------------
@open_decorator()
def read_text(v00: T000, *args, encoding=D001) -> str:
    v10: TextIOWrapper = v00

    return read(v10)


@open_decorator()
def save_text(v00: T000, v02: str, *, encoding=D001) -> int:
    v10: TextIOWrapper = v00
    v11: str = v02

    return save(v10, v11)


@open_decorator()
def push_text(v00: T000, v02: str, *, encoding=D001) -> int:
    v10: TextIOWrapper = v00
    v11: str = v02

    return save(v10, v11)


# ----------------------------------------------------------------------------------------------------
@open_decorator()
def read_code(v00: T000, *args) -> list:
    v10: TextIOWrapper = v00

    return read(v10).splitlines()


@open_decorator()
def save_code(v00: T000, v02: list) -> int:
    v10: TextIOWrapper = v00
    v11: str = '\n'.join(v02)

    return save(v10, v11)


# ----------------------------------------------------------------------------------------------------
@open_decorator()
def read_json(v00: T000, *args) -> dict | list:
    v10: TextIOWrapper = v00

    return load(v10)


@open_decorator()
def save_json(v00: T000, v02: dict | list) -> None:
    v10: TextIOWrapper = v00

    return dump(v02, v10, ensure_ascii=False, indent=4)


# ----------------------------------------------------------------------------------------------------
def sum(*args):
    import builtins
    return builtins.sum([+v for v in args if isinstance(v, int | float)])


# ----------------------------------------------------------------------------------------------------
def main_00(_v0: str):
    v00 = [1, 3.1, 1e3]
    v01 = v00.copy()
    v01.insert(1, 'a')
    v02 = range(0x00, 0x64 + 1)

    print(*[(sum(*_0), _0) for _0 in [
        v00,
        v01,
        v02
    ]], sep=_v0)


def main_01(_v0: str):
    v00 = 't00.py'
    v01 = 't01.py'
    v02 = 't02.py'
    v03 = '# 这是注释' + _v0
    v04 = 'gbk'

    print(*[(repr(_0(*_1, **_2)), _1, _2) for (_0, _1, _2) in [
        (read_text, (v00,), {}),
        (save_text, (v00, v03), {}),
        (push_text, (v00, v03), {}),
        (save_text, (v02, v03), dict(encoding=v04)),
        (read_text, (v02,), dict(encoding=v04)),
    ]], sep=_v0)

    # print(read_text('t00.py'))
    # print(save_text('t00.py', '# 这是注释\n'))
    # print(push_text('t00.py', '# 这是注释\n'))
    # print(save_text('t01.py', '# 这是注释\n', encoding='gbk'))
    # print(read_text('t01.py', encoding='gbk'))

    return v01, v02


def main_02(_v0: str):
    v00 = 't00.json'
    v01 = 't01.json'
    v02 = 't02.json'
    v03 = 't03.json'

    print(*[(repr(_0(*_1)), type(_0(*_1))) for (_0, _1) in [
        (read_json, (v00,)),
        (save_json, (v01, read_json(v00))),
        (read_json, (v02,)),
        (save_json, (v03, read_json(v02))),
    ]])

    # JSON
    # print(type(read_json('t00.json')))
    # print(read_json('t00.json'))
    # print(save_json('t01.json', read_json('t00.json')))

    # Array
    # print(type(read_json('t02.json')))
    # print(read_json('t02.json'))
    # print(save_json('t03.json', read_json('t02.json')))

    return v01, v03


def main_03(_v0: str):
    v00 = 't00.png'
    v01 = 't01.png'
    v02 = 't02.png'

    print(*[(repr(_0(*_1)), type(_0(*_1))) for (_0, _1) in [
        (read_bytes, (v00,)),
        (save_bytes, (v01, read_bytes(v00))),
    ]])

    [push_bytes(v02, v) for v in chunk(read_bytes(v00))]

    # v00 = read_bytes('20201124032511.png')
    # print(type(v00))
    # print(v00)
    # print(save_bytes('000.png', v00))
    # 需要将完整的数据进行切割
    # [push_bytes('002.png', v) for v in chunk(v00)]

    return v01, v02


def main_04(_v0: str):
    v00 = 't00.py'
    v01 = 't03.py'

    print(*[(repr(_0(*_1)), type(_0(*_1))) for (_0, _1) in [
        (read_code, (v00,)),
        (save_code, (v01, read_code(v00))),
    ]])

    # print(read_code('t00.py'))
    # print(save_code('t03.py', read_code('t00.py')))

    return v01,


def main(_v0='\n'):
    v00 = []

    [v00.extend(v) for v in [
        main_00(_v0),
        main_01(_v0),
        main_02(_v0),
        main_03(_v0),
        main_04(_v0),
    ] if v]

    1 and [Path(v).unlink(missing_ok=True) for v in v00]


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
