# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from mcdc_checker import mcdc_checker


def setup_function(method):
    mcdc_checker.reset_errors()


def test_mcdc_checker():
    mcdc_checker.check_file("mcdc_checker/tests/main.c", None, None, None)

    expected_errors = {
        "bdd_is_not_tree_like": [
            (("mcdc_checker/tests/main.c", 8, 9), "c, a, b"),
            (("mcdc_checker/tests/test.h", 8, 9), "c, a, b"),
            (("mcdc_checker/tests/main.c", 46, 13), "c, a, b"),
            (("mcdc_checker/tests/main.c", 50, 12), "c, a, b"),
            (("mcdc_checker/tests/main.c", 62, 18), "c, a, b"),
            (
                ("mcdc_checker/tests/main.c", 66, 13),
                "b < c, a < b, c > 4, b < 2.5",
            ),
            (("mcdc_checker/tests/main.c", 70, 13), "b, a, c"),
            (("mcdc_checker/tests/main.c", 78, 13), None),
        ],
        "failed_to_create_bdd": [],
        "clang_parse_failed": [],
        "invalid_operator_nesting": [(("mcdc_checker/tests/main.c", 74, 19), None)],
        "unexpected_node": [],
    }

    expected_statistics = {
        "num_compiler_issues": 0,
        "num_correctable_non_tree_like_decisions": 8,
        "num_decisions": 13,
        "num_files_checked": 1,
        "num_non_correctable_non_tree_like_decisions": 1,
        "num_tree_like_decision": 4,
    }

    assert mcdc_checker.errors == expected_errors
    assert mcdc_checker.statistics == expected_statistics

    os.system("rm file_mcdc_checker-tests-*.dot")
