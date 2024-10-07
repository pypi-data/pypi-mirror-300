import os


def write(text: str, mode: str, f: str):
    os.makedirs('tmp', exist_ok=True)
    with open(f'tmp/{f}', mode=mode, encoding='utf-8') as o:
        o.write(text)


def read(f: str) -> str:
    os.makedirs('tmp', exist_ok=True)
    f = f'tmp/{f}'
    with open(f, mode='a', encoding='utf-8') as _:
        pass
    with open(f, mode='r', encoding='utf-8') as i:
        return i.read()


def read_rows(f: str = 'input') -> list:
    text = read(f)
    if text == '':
        return []
    return text.split('\n')


def append(text: str, f: str = 'output'):
    write(text=f'{text}\n', mode='a+', f=f)


def append_e(text, f='error'):
    append(text=text, f=f)


def truncate(f):
    write(text='', mode='w', f=f)


def rename(f: str, new_f: str):
    os.rename(f'tmp/{f}', f'tmp/{new_f}')


def remove(f: str):
    os.remove(f'tmp/{f}')
