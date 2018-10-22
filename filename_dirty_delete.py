#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/10/22.
# email to LipsonChan@yahoo.com
#
import os


def delete_re_target(filename, res):
    for re_str in res:
        re.sub(re_str)


def rename_files_in_dir(path):
    """
    please run in python3 if your os is windows, cause os.walk has a encoding bug
    :type path: str
    :param path:
    :return:
    """

    for root, dirs, files in os.walk(path):
        for file in files:  # type: str
            suffix_i = file.rfind('.')
            suffix = file[suffix_i + 1:]
            name = file[:suffix_i]

            new_name = ""
            os.rename(os.path.join(root, file), os.path.join(root, new_name))