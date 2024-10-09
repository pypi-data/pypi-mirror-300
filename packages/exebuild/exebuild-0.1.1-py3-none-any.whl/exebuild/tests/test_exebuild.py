# -*- coding: utf-8 -*-
# Copyright (c) 2024 IKUS Software
#
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import os
import unittest

from exebuild import makensis, signexe


class TestExebuild(unittest.TestCase):
    def test_signexe(self):
        # TODO Not sure how to properly test signexe without environment variables
        exe_path = os.path.join(__file__, '../smallexe64.exe')
        signexe(exe_path)

    def test_makensi(self):
        nsi_file = os.path.join(__file__, '../test.nsi')
        makensis(
            [
                '-NOCD',
                '-INPUTCHARSET',
                'UTF8',
                '-DAppVersion=1.2.3',
                '-DOutFile=installer.exe',
                nsi_file,
            ],
            cwd=os.path.join(__file__, '..'),
        )
