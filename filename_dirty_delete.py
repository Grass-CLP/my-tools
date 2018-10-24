#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/10/22.
# email to LipsonChan@yahoo.com
#
import codecs
import json
import os
import re

import sys
from time import sleep


def utf8_data_to_file(f, data):
    if hasattr(data, 'decode'):
        f.write(data.decode('utf-8'))
    else:
        f.write(data)


def delete_re_str(filename, res):
    for re_str in res:
        filename = re.sub(re_str, '', filename, flags=re.I | re.U)

    return filename


def delete_replace_str(filename, replaces):
    """

    :param filename:
    :param replaces:
    :type filename: str
    :type replaces: list[str]
    :return:
    """
    for rep in replaces:
        filename = filename.replace(rep, '')

    return filename


def rename_files_in_dir(path, config, only_print=False):
    """
    please run in python3 if your os is windows, cause os.walk has a encoding bug
    :param only_print:
    :type path: str
    :type config: dict
    :param path:
    :param config:
    :return:
    """

    refuse_suffix = config.get('refuse_suffix', [])
    refuse_dir = config.get('refuse_dir', [])
    re_sub = config.get('re_sub', [])
    replaces = config.get('replaces', [])

    for root, dirs, files in os.walk(path):
        rename_dirs = dict()
        new_dirs = list()  # type: list[str]
        for name in dirs:
            if name in refuse_dir:
                continue

            new_name = name
            new_name = delete_replace_str(new_name, replaces)
            new_name = delete_re_str(new_name, re_sub)
            new_name = new_name.strip("@#. -")
            new_dirs.append(name)

            print("rename dir '{}' to '{}' in '{}'".format(name, new_name, root))
            if name != new_name and new_name:
                if not only_print:
                    os.rename(os.path.join(root, name),
                              os.path.join(root, new_name))

            pass
        dirs = dirs  # type: list[str]
        dirs.clear()
        dirs.extend(new_dirs)

        for file in files:  # type: str
            suffix_i = file.rfind('.')
            suffix = file[suffix_i + 1:]
            name = file[:suffix_i]

            if suffix in refuse_suffix:
                continue

            new_name = name
            new_name = delete_replace_str(new_name, replaces)
            new_name = delete_re_str(new_name, re_sub)
            new_name = new_name.strip("#@. -")

            print("rename file '{}' to '{}' in '{}'".format(
                "{}.{}".format(name, suffix),
                "{}.{}".format(new_name, suffix),
                root))
            if name != new_name and new_name:
                if not only_print:
                    os.rename(os.path.join(root, "{}.{}".format(name, suffix)),
                              os.path.join(root, "{}.{}".format(new_name, suffix)))
                    # todo move change name after print and wait for input


def load_config(file_name):
    try:
        with codecs.open(file_name, 'r', 'utf-8') as f:
            string = f.read()
            print(string)
            config = json.loads(string, encoding='utf-8')
            return config
    except IOError or ValueError:
        return dict()


def main():
    path = os.path.dirname(os.path.realpath(__file__))
    config_file_name = os.path.join(path, "filename_dirty_delete_target.json")
    config = load_config(config_file_name)
    rename_files_in_dir(path, config, False)
    # rename_files_in_dir(path, config, False)

    sleep(2)


if __name__ == "__main__":
    main()
    pass
