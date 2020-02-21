# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the tests for the code-blocks in the use-cases category."""

import logging
import os
from pathlib import Path

from ..helper import extract_code_blocks, read_md_file
from ...conftest import ROOT_DIR

logger = logging.getLogger(__name__)


class TestStepByStepDocs:
    """This class contains the tests for the bash-blocks in the car-park-skills.md file."""

    def test_code_blocks_exist(self):
        """Test that all the code-blocks exist in the python file."""
        path = Path(
            ROOT_DIR, "tests", "test_docs", "test_step_by_step_guides", "md_files"
        )
        logger.info(os.listdir(path))
        for file in os.listdir(path):
            if file.endswith(".md"):
                bash_file = read_md_file(file=Path(path, file))
                md_path = os.path.join(ROOT_DIR, "docs", file.replace("bash-", ""))
                code_blocks = extract_code_blocks(file=md_path, filter="bash")
                for blocks in code_blocks:
                    assert (
                        blocks in bash_file
                    ), "[{}]: FAILED. Code must be identical".format(file)
                logger.info("[{}]: PASSED".format(file))
