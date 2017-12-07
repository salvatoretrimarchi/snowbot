import os
import math
import requests
import tarfile
import zipfile
import click

FOO = 'foo'


def convert_size(size_bytes):
    """
    convert size in bytes to human readable string, i.e. 1024 -> 1KB
    copied from https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    :param size_bytes:
    :return:
    """
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '{} {}'.format(s, size_name[i])


def files_exist(folder, files):
    for f in files:
        if not os.path.exists(os.path.join(folder, f)):
            return False
    return True


def files_missing(folder, files):
    missing = []
    for f in files:
        p = os.path.join(folder, f)
        if not os.path.exists(p):
            missing.append(p)
    return missing


def maybe_download(url, download_dir, silent=False, progress=True):
    def p(*args):
        if not silent:
            print(*args)

    # download file
    file_name = url.split('/')[-1]
    file_path = os.path.join(download_dir, file_name)
    if os.path.exists(file_path):
        p(url, 'has already been downloaded to', file_path)
    else:
        p('downloading', url, 'to', file_path)
        with open(file_path, 'wb') as f:
            res = requests.get(url, stream=True)
            size = res.headers.get('content-length')
            if size and progress:
                size = int(size)
                with click.progressbar(length=size,
                                       label='Downloading {} {}'.format(file_name, convert_size(size))) as bar:
                    for data in res.iter_content(chunk_size=4096):
                        f.write(data)
                        bar.update(len(data))
            else:
                f.write(res.content)  # TODO: don't know if this would work...

    return file_path


def maybe_extract(file, folder, silent=False):
    def p(*args):
        if not silent:
            print(*args)

    if not folder:
        p('extract destination not specified')
        return False
    # already extracted
    if os.path.isdir(folder):
        p('folder', folder, 'already exist, assume already extracted')
        return True
    # extract file TODO: can there be progress bar?
    if not os.path.exists(file):
        p(file, 'does not exist')
        return False
    if file.endswith('.zip'):
        zipfile.ZipFile(file=file, mode='r').extractall(folder)
    elif file.endswith(('.tar.gz', '.tgz')):
        tarfile.open(name=file, mode='r:gz').extractall(folder)
    else:
        p('unknown file extension, only support zip, tar.gz but got', file)
        return False
    p('file extracted to', folder)
    return True
