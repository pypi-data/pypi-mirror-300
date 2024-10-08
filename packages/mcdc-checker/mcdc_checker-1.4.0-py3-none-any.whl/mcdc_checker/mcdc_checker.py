#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import argparse
import re
import sys
import os
import tempfile

try:
    import clang.cindex  # type: ignore[import-untyped]
except ModuleNotFoundError:
    print(
        "The Clang Python bindings were not found. Please make sure to \n"
        "install Clang on your system before running MCDC Checker."
    )
    sys.exit(1)
from glob import glob
import itertools
import json
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../PBL/include")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../PBDD/include")
import BDD  # type: ignore[import-untyped]

errors = {}
statistics = {}


def reset_errors():
    """
    Initialize the global errors dictionary with no errors occurred, which is an empty
    list for each of the following error types:

    clang_parse_failed:
        Clang could not parse a given file. Make sure that the include paths
        are correct and complete.
    invalid_operator_nesting:
        A condition contains a decision operator. Please refactor the code in
        question.
    unexpected_node:
        While walking the AST a node could not be parsed. This is a bug in the
        MCDCTreeChecker.
    bdd_is_not_tree_like:
        A decision was found which has a non tree-like BDD. Refactor the code
        in question.

    Each of these lists should be appended with a tuple containing the
    location and a possible solution::

        ((filename, line, column), solution)
    """
    global errors
    errors = {
        "clang_parse_failed": [],
        "failed_to_create_bdd": [],
        "invalid_operator_nesting": [],
        "unexpected_node": [],
        "bdd_is_not_tree_like": [],
    }
    global errors_format_str
    errors_format_str = {
        "clang_parse_failed": "Clang failed to parse file",
        "failed_to_create_bdd": "No BDD could be created for decision",
        "invalid_operator_nesting": "Decision has invalid operator nesting",
        "unexpected_node": "Unexpected node was found in the AST",
        "bdd_is_not_tree_like": "BDD is not tree-like",
    }


def reset_statistics():
    """
    Initialize the global statistics dictionary.
    """
    global statistics
    statistics = {
        "num_decisions": 0,
        "num_tree_like_decision": 0,
        "num_correctable_non_tree_like_decisions": 0,
        "num_non_correctable_non_tree_like_decisions": 0,
        "num_compiler_issues": 0,
        "num_files_checked": 0,
    }
    global statistics_format_str
    statistics_format_str = {
        "num_decisions": "Number of decisions: {}",
        "num_tree_like_decision": "Number of tree-like decisions: {}",
        "num_correctable_non_tree_like_decisions": "Number of correctable non-tree-like decisions: {}",
        "num_non_correctable_non_tree_like_decisions": "Number of non-correctable non-tree-like decisions: {}",
        "num_compiler_issues": "Number of compiler preprocess/parse errors: {}",
        "num_files_checked": "Number of files checked: {}",
    }


reset_errors()
reset_statistics()


def is_interesting_decision(node):
    """
    Returns true, if the given *node* is a binary operator at the top level of
    a interesting decision in the sense of MCDC. Otherwise false is returned.
    """
    try:
        return node.kind == clang.cindex.CursorKind.BINARY_OPERATOR and (
            node.binary_operator == clang.cindex.BinaryOperator.LAnd
            or node.binary_operator == clang.cindex.BinaryOperator.LOr
        )
    except AttributeError:
        print(
            "It looks like the version of Clang you have installed is too old.\n"
            "Please install Clang 19 or newer."
        )
        sys.exit(1)


def check_bdd_is_tree(bdd):
    """
    Returns true if the given *bdd* is a tree. Otherwise false is returned.

    In the context of this function, a BDD is a tree when every non-leaf node
    can be reached from the root via exactly one path. This is done by
    examining every edge in the T table of the BDD and saving the end node in a
    visitation list. If, at the end, the visitation list contains every node
    exactly once, the BDD is a tree.
    """
    visited = []
    for _, (_, l, h) in bdd["t_table"].items():
        if l and l != 0 and l != 1:
            visited.append(l)
        if h and h != 0 and h != 1:
            visited.append(h)

    return len(visited) == len(set(visited))


def bdd_to_dot(bdd, filename, line, column, suffix):
    """
    Save the dot graph of the *bdd* to a file. The parameters *filename*,
    *line*, *column* and *suffix* (in that order) are used to generate the
    filename of the resulting file.

    The *filename* parameter refers to the source file the graph is generated
    for. It may contain slashes which will be replaced by hyphens.

    The *line* and *column* refer to the top level binary operator of the decision
    represented by the BDD.

    An additional *suffix* can be appended to the filename of the resulting dot
    file to distinguish different graphs for the same decision.
    """
    BDD.dot_bdd(
        bdd,
        "file_{}_line_{}_col_{}_{}.dot".format(
            filename.replace(os.path.sep, "-"), line, column, suffix
        ),
    )


def get_children_list(node):
    """
    Get a list of children of the given *node*.

    Returns a true list instead of an iterable as node.get_children does. This
    means you can count the number of children with len() or access the n-th
    children with [n].
    """
    return [child for child in node.get_children()]


class MCDCTreeChecker:
    """
    The main class of this tool, which implements the logic to generate and walk
    the AST of a C file to find interesting decisions in the MCDC sense.

    Example:

    >>> reset_errors()
    >>> c = MCDCTreeChecker("mcdc_checker/tests/test.h")
    >>> c.parse()
    >>> c.find_decision()
    >>> c.create_bdds()
    >>> c.check_bdds_are_tree_like()
      Non tree-like decision in file mcdc_checker/tests/test.h at line 8, column 9
    """

    def __init__(self, filename):
        """
        Creates a new MCDCTreeChecker to check the file referenced by *filename*.

        :param filename: The preprocessed source code file. This file is read,
            parsed and analyzed by the methods of this class.
        """
        self.filename = filename
        self.preprocessor_lines = open(self.filename).readlines()
        self.debug = False
        self.exprs = []
        self.bdds = []
        self.literal_counter = 0

    def parse(self):
        """
        Use libclang to parse the file referenced by self.filename. After
        calling this function, self.tu will contain the AST of the translation
        unit.
        """
        index = clang.cindex.Index.create()
        self.tu = index.parse(self.filename)

    def get_original_location(self, node):
        """
        Get the location (line, column) of *node* in the non-preprocessed
        original file by looking at the location markers inserted by clang into
        the preprocessed C code.

        This is used to print user-readable messages with line numbers
        referring to the original source file.
        """
        linemarker_offset = 1
        node_location_index = node.location.line - 1

        try:
            while not re.match(
                r'# \d+ ".*"',
                self.preprocessor_lines[node_location_index - linemarker_offset],
            ):
                linemarker_offset += 1
        except IndexError:
            # No preprocessor marker was found, either the code was not preprocessed
            # or the preprocessor didn't create linemarkers. Return the location of the
            # node.
            return self.filename, node.location.line, node.location.column

        linemarker = self.preprocessor_lines[node_location_index - linemarker_offset].split(" ")

        try:
            orig_line, orig_file = (
                int(linemarker[1]) + linemarker_offset - 1,
                linemarker[2].split('"')[1],
            )
        except ValueError:
            # Something went wrong when parsing the location comment
            return self.filename, node.location.line, node.location.column

        return orig_file, orig_line, node.location.column

    def check_no_more_interesting_operators_below(self, node, level):
        """
        Check that for no descendants of *node* the
        :class:`is_interesting_decision` function returns true. In case an
        offending node is found, an error message is printed and the global
        error dict is appended.

        This function is used to sanity check the C code so that a condition
        does not contain a decision.
        """
        if is_interesting_decision(node):
            print(
                "{}ERROR: Invalid operator nesting! {} [line={}, col={}]".format(
                    " " * (level * 2 + 2),
                    self.get_condition_spelling(node),
                    self.get_original_location(node)[1],
                    node.location.column,
                )
            )
            errors["invalid_operator_nesting"].append((self.get_original_location(node), None))
        else:
            # Recursively call this function for each child of the given node
            if self.debug:
                print(
                    "{}Node {} [line={}, col={}]".format(
                        " " * (level * 2 + 2),
                        node.kind,
                        self.get_original_location(node)[1],
                        node.location.column,
                    )
                )
                for child in node.get_children():
                    self.check_no_more_interesting_operators_below(child, level + 1)
            else:
                for child in node.get_children():
                    self.check_no_more_interesting_operators_below(child, level)

    def get_condition_spelling(self, node):
        """
        Returns the name of a condition referenced by *node* in pseudo-C-like
        syntax. This function is used to name the found conditions in the BDD.

        The function supports the following C constructs:

            * Function calls
            * Conditional operators
            * Unary expressions (such as sizeof)
            * Member reference expressions (such as struct->member)
            * Binary Operators
            * Parens expressions
            * Array accesses
            * Compound Literals
            * Unions
            * Leaf nodes such as literals or declaration references

        For unexposed expressions it will try to generate the name for the
        descendants first. If that comes up empty, the name of the unexposed
        node itself will be used.
        """
        children = get_children_list(node)

        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            # Handle function calls by concatenating the spelling of all
            # parameters (children) and the function's name (current node)
            params = ", ".join(self.get_condition_spelling(c) for c in children[1:])
            return node.spelling + "({})".format(params)
        elif node.kind == clang.cindex.CursorKind.CONDITIONAL_OPERATOR:
            return self.get_condition_spelling(children[0])
        elif node.kind == clang.cindex.CursorKind.CXX_UNARY_EXPR:
            # Handle unary expressions such as sizeof
            if len(children) > 0:
                return "UnaryExpr({})".format(self.get_condition_spelling(children[0]))
            else:
                self.literal_counter += 1
                return "UnaryExpr(literal_{})".format(self.literal_counter)
        elif node.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
            if len(children) > 0:
                # Handle member references such as struct->member
                return "{}->{}".format(self.get_condition_spelling(children[0]), node.spelling)
            else:
                return node.spelling
        elif node.kind == clang.cindex.CursorKind.CSTYLE_CAST_EXPR:
            if len(children) == 1:
                return "({})".format(self.get_condition_spelling(children[0]))
            else:
                return "({}){}".format(
                    self.get_condition_spelling(children[0]),
                    self.get_condition_spelling(children[1]),
                )
        elif node.kind == clang.cindex.CursorKind.BINARY_OPERATOR and len(children) == 2:
            return "{} {} {}".format(
                self.get_condition_spelling(children[0]),
                node.spelling,
                self.get_condition_spelling(children[1]),
            )
        elif node.kind == clang.cindex.CursorKind.ARRAY_SUBSCRIPT_EXPR and len(children) == 2:
            return "{}[{}]".format(
                self.get_condition_spelling(children[0]),
                self.get_condition_spelling(children[1]),
            )
        elif node.kind == clang.cindex.CursorKind.COMPOUND_LITERAL_EXPR and len(children) == 2:
            return "CompoundLiteral({}, {})".format(
                self.get_condition_spelling(children[0]),
                self.get_condition_spelling(children[1]),
            )
        elif node.kind == clang.cindex.CursorKind.UNION_DECL and len(children) == 2:
            return "UnionDecl({}, {})".format(
                self.get_condition_spelling(children[0]),
                self.get_condition_spelling(children[1]),
            )
        elif len(children) == 1:
            # Handle nodes with a single children, such as parens expressions
            if node.kind == clang.cindex.CursorKind.PAREN_EXPR:
                return "({})".format(
                    self.get_condition_spelling(children[0]),
                )
            if node.kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
                from_children = self.get_condition_spelling(children[0])
                if from_children:
                    return from_children
                else:
                    return node.spelling
            else:
                if node.spelling:
                    return node.spelling
                else:
                    return self.get_condition_spelling(children[0])
        elif len(children) == 0:
            # Handle leaf nodes by returning their spelling
            if node.kind in (
                clang.cindex.CursorKind.INTEGER_LITERAL,
                clang.cindex.CursorKind.FLOATING_LITERAL,
                clang.cindex.CursorKind.CHARACTER_LITERAL,
            ):
                return "".join(
                    [
                        token.spelling
                        for token in clang.cindex.TokenGroup.get_tokens(
                            node._tu, extent=node.extent
                        )
                    ]
                )
            if node.spelling:
                return node.spelling
            else:
                self.literal_counter += 1
                return "literal_{}".format(self.literal_counter)
        elif node.kind == clang.cindex.CursorKind.UNEXPOSED_EXPR or len(children) >= 2:
            # Handle unexposed expr nodes in a generic way
            return (
                "(" + ", ".join([self.get_condition_spelling(child) for child in children]) + ")"
            )
        else:
            # We encountered something which has more than two children
            print(
                "ERROR: Unexpected node or number of children: children={} kind={} line={}".format(
                    len(children), node.kind, self.get_original_location(node)[1]
                )
            )
            errors["unexpected_node"].append((self.get_original_location(node), None))

    def build_decision(self, node, level, expr, var_order):
        """
        Build a decision object which can be used in BDD object from a descision in the AST.

        :param node: The top level node of the decision in the AST
        :param level: Indentation level for debug messages
        :param expr: The expression is built recursively in this parameter.
            When first calling the method, this should be an empty dict.
        :param var_order: The variables discovered while building the expression.
            When first calling the method, this should be an empty list.

        After calling this functions, the *expr* and *var_order* values can be
        used in a BDD, which can be created with :class:`bdd_init`.
        """
        if is_interesting_decision(node):
            if self.debug:
                print(
                    "{}Decision {} [line={}, col={}]".format(
                        " " * (level * 2 + 2),
                        node.spelling,
                        self.get_original_location(node)[1],
                        node.location.column,
                    )
                )
            if node.binary_operator == clang.cindex.BinaryOperator.LAnd:
                expr["type"] = "and"
            elif node.binary_operator == clang.cindex.BinaryOperator.LOr:
                expr["type"] = "or"
            expr["expr1"] = {}
            expr["expr2"] = {}

            children = get_children_list(node)
            self.build_decision(children[0], level + 1, expr["expr1"], var_order)
            self.build_decision(children[1], level + 1, expr["expr2"], var_order)
        elif node.kind == clang.cindex.CursorKind.CONDITIONAL_OPERATOR:
            self.build_decision(get_children_list(node)[0], level, expr, var_order)
        elif node.kind == clang.cindex.CursorKind.PAREN_EXPR:
            for child in node.get_children():
                self.build_decision(child, level, expr, var_order)
        else:
            if node.kind == clang.cindex.CursorKind.BINARY_OPERATOR:
                text = node.binary_operator
            else:
                text = node.kind
            name = self.get_condition_spelling(node)
            expr["name"] = (name, 0)
            expr["type"] = "var"
            var_order.append(name)
            if self.debug:
                print(
                    "{}Node {} [line={}, col={}]".format(
                        " " * (level * 2 + 2),
                        node.kind,
                        self.get_original_location(node)[1],
                        node.location.column,
                    )
                )
            self.check_no_more_interesting_operators_below(node, level + 1)

    def find_decision(self, node=None, level=None):
        """
        Walk the AST recursively to find the top-level node of each decision.
        For each found node, the :class:`build_decision` method is called.

        :param node: The node to check if it is a decision. If this is None,
            the root of the AST will be used.
        :param level: Indentation level for debug messages. If None, zero will
            be used.
        """
        if not node:
            node = self.tu.cursor
        if not level:
            level = 0

        if is_interesting_decision(node):
            statistics["num_decisions"] += 1

            expr = {}
            var_order = []

            self.build_decision(node, level, expr, var_order)
            self.exprs.append((expr, var_order, self.get_original_location(node)))
        else:
            if self.debug:
                print(
                    "{}Node {} [line={}, col={}]".format(
                        " " * (level * 2 + 2),
                        node.kind,
                        self.get_original_location(node)[1],
                        node.location.column,
                    )
                )
                for child in node.get_children():
                    self.find_decision(child, level + 1)
            else:
                for child in node.get_children():
                    self.find_decision(child, level)

    def bdd_init(self, expr, var_order):
        """
        Create a BDD dictionary from the given expression and variable ordering
        which can be used with the PBDD library.

        This is similar to the bdd_init function from PBDD itself, with the
        difference that it doesn't read an expression from a file but instead
        uses the expression passed in with parameter expr.

        :param expr: An expression as built by :class:`build_decision`.
        :param var_order: A variable order list as built by :class:`build_decision`.
        """
        num_vars = len(var_order)

        bdd = {
            "expr": expr,
            "t_table": {
                0: ((num_vars + 1), None, None),
                1: ((num_vars + 1), None, None),
            },
            "u": 1,
            "n": num_vars,
            "h_table": {},
            "var_order": var_order,
        }

        return bdd

    def create_bdds(self):
        """
        For each expression and variable order found in the source file, build
        a BDD with ITE (If-then-else) method.
        """
        for expr, var_order, location in self.exprs:
            try:
                bdd = self.bdd_init(expr, var_order)
                BDD.ite_build(bdd)
                self.bdds.append((bdd, location))
            except Exception as e:
                errors["failed_to_create_bdd"].append((location, None))

    def permutate_bdd_vars(self, bdd):
        """
        Permutate the variable order given in *bdd* in all possible ways, build
        a minimal BDD with the modified order and given expression and check if
        the resulting BDD is a tree.

        :param bdd: The BDD which shall be permutated. The expression is used unmodified.
        :returns: A tree-like BDD if one is found, None otherwise.
        """
        original_order = bdd["var_order"]
        expr = bdd["expr"]
        for order in itertools.permutations(original_order, len(original_order)):
            bdd = self.bdd_init(expr, list(order))
            BDD.reorder_ite_build(bdd)

            if check_bdd_is_tree(bdd):
                return bdd

    def check_bdds_are_tree_like(self):
        """
        For each BDD, check whether it is tree-like. If not try to find a
        tree-like solution by calling :class:`permutate_bdd_vars`. For each
        non-tree like BDD an error is appended to the global error dictionary
        together with the possible solution, if any.
        """
        for bdd, (orig_filename, line, column) in self.bdds:
            if not check_bdd_is_tree(bdd):
                print(
                    "  Non tree-like decision in file {} at line {}, column {}".format(
                        orig_filename, line, column
                    )
                )
                if bdd["n"] <= 5:
                    reordered_bdd = self.permutate_bdd_vars(bdd)
                    if reordered_bdd:
                        tree_order = reordered_bdd["var_order"]
                        bdd_to_dot(reordered_bdd, orig_filename, line, column, "reordered")
                    else:
                        tree_order = None
                else:
                    reordered_bdd = None
                    tree_order = None

                if tree_order:
                    statistics["num_correctable_non_tree_like_decisions"] += 1
                else:
                    statistics["num_non_correctable_non_tree_like_decisions"] += 1

                errors["bdd_is_not_tree_like"].append(
                    (
                        (orig_filename, line, column),
                        ", ".join(tree_order) if tree_order else None,
                    )
                )

                bdd_to_dot(bdd, orig_filename, line, column, "orig")
            else:
                statistics["num_tree_like_decision"] += 1
                if self.debug:
                    print(
                        "  Decision in file {} in line {}, column {} is tree-like".format(
                            orig_filename, line, column
                        )
                    )


def check_file(filename, include_paths, defines, debug):
    """
    Check a file for non-tree like BDDs by preprocessing the file and using an
    MCDCTreeChecker instance.

    :param filename: Path to the file to check
    :param include_paths: List of include paths to pass to the preprocessor
    :param debug: If set to true, debug messages will be printed while processing the file
    """
    print("Processing file {}".format(filename))

    # Call Clang preprocess and save to a temporary file
    tf = tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1])
    command = "clang {} {} -E {} > {}".format(
        " ".join("-I {}".format(x) for x in include_paths) if include_paths else "",
        " ".join("-D {}".format(x) for x in defines) if defines else "",
        filename,
        tf.name,
    )
    exitcode = os.system(command)

    if exitcode != 0:
        print("ERROR: Clang failed to preprocess the file {}".format(filename))
        errors["clang_parse_failed"].append(((filename, None, None), None))
        statistics["num_compiler_issues"] += 1
    if exitcode == 2:
        sys.exit(2)

    c = MCDCTreeChecker(tf.name)
    c.debug = debug
    c.parse()
    c.find_decision()
    c.create_bdds()
    c.check_bdds_are_tree_like()

    statistics["num_files_checked"] += 1


def print_statistics():
    """
    Print statistics values
    """
    print(
        "\nStatistics (including decisions encountered multiple times, e.g. in included headers):"
    )
    for stat_type, stat in statistics.items():
        print("  " + statistics_format_str[stat_type].format(stat))


def print_error_summary():
    """
    Print all errors which have been appended to the global error dictionary.
    """
    if any([len(error_list) > 0 for _, error_list in errors.items()]):
        print(
            "\nThe following errors were found (excluding decisions encountered multiple times, e.g. in headers):"
        )
    else:
        print("\nNo errors were found.")
    for error_type, error_list in errors.items():
        unique_errors = set(error_list)
        if len(unique_errors) > 0:
            print("  " + errors_format_str[error_type] + ":")
            for (filename, line, column), solution in unique_errors:
                if line:
                    print("    file {} in line {} column {}".format(filename, line, column))
                else:
                    print("    file {}".format(filename))

                if solution:
                    print("      Found solution: {}".format(solution))


def save_json_report(file):
    severity_map = {
        "clang_parse_failed": "blocker",
        "failed_to_create_bdd": "minor",
        "invalid_operator_nesting": "critical",
        "unexpected_node": "minor",
        "bdd_is_not_tree_like": "critical",
    }

    report = []

    for error_type, error_list in errors.items():
        unique_errors = set(error_list)
        if len(unique_errors) > 0:
            for (filename, line, column), solution in unique_errors:
                digest = hashlib.sha256()
                digest.update("{}{}{}".format(file, error_type, solution).encode("utf-8"))
                fingerprint = digest.hexdigest()

                report.append(
                    {
                        "type": "issue",
                        "description": f"{errors_format_str[error_type]}. Found solution: {solution}",
                        "check_name": error_type,
                        "categories": ["Bug Risk", "Complexity"],
                        "location": {
                            "path": filename,
                            "positions": {
                                "begin": {"line": line, "column": column},
                                "end": {"line": line, "column": column},
                            },
                        },
                        "severity": severity_map[error_type],
                        "fingerprint": fingerprint,
                    }
                )

    with open(file, "w") as file:
        file.write(json.dumps(report, indent=2))


def main():
    """
    The main function of this project. Parses the commandline, then creates and
    starts MCDCTreeChecker instances for each file to check.
    """

    parser = argparse.ArgumentParser(description="MCDC Tree Checker")
    parser.add_argument(
        "-j",
        "--json-output",
        action="store",
        type=str,
        metavar="file",
        help="Output JSON report to file",
    )
    parser.add_argument(
        "-I",
        "--include",
        action="append",
        type=str,
        nargs="+",
        help="Add include path for preprocessor",
    )
    parser.add_argument(
        "-D",
        "--define",
        action="append",
        type=str,
        nargs="+",
        help="Add define for preprocessor",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        required=False,
        help="Check all C/C++ implementation and header files in current directory recursively",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        required=False,
        help="Enable additional debug output",
    )
    parser.add_argument(
        "file",
        type=str,
        nargs="?",
        default=None,
        help="Path to a single file which shall be checked. If file is '-', a list of files is read from stdin",
    )
    args = parser.parse_args()
    if args.include:
        args.include = [include for include_list in args.include for include in include_list]
    if args.define:
        args.define = [define for define_list in args.define for define in define_list]

    if args.all:
        for ext in ("c", "cc", "cxx", "cpp", "c++", "h", "hh", "hxx", "hpp", "h++"):
            files = glob("**/*.{}".format(ext), recursive=True)
            for filename in files:
                check_file(filename, args.include, args.define, args.debug)
    elif args.file:
        if args.file == "-":
            f = sys.stdin.readline().strip()
            while f:
                check_file(f, args.include, args.define, args.debug)
                f = sys.stdin.readline().strip()
        else:
            check_file(args.file, args.include, args.define, args.debug)
    else:
        parser.print_usage()
        sys.exit(3)

    print_statistics()
    print_error_summary()

    if args.json_output:
        save_json_report(args.json_output)

    for _, error_list in errors.items():
        if len(error_list) > 0:
            sys.exit(2)


if __name__ == "__main__":
    main()
