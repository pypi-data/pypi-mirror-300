# -*- coding: utf-8 -*-
# Copyright (c) 2024 IKUS Software
#
# This software is licensed under the MIT License.
# See the LICENSE file for more details.
import argparse

from . import makensis, signexe


def main_signexe():
    parser = argparse.ArgumentParser(
        prog="signexe",
        description="Sign an executable.",
    )
    parser.add_argument('file', metavar='FILE', help='Executable to be sign')
    cfg = parser.parse_args()
    signexe(exe_path=cfg.file)


def main_makensis():
    makensis()
