##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2019, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
Tests for idaes.dmf.commands
"""
import logging
import os
import shutil
import sys

#
import pytest

#
from idaes.dmf import dmfbase, commands, errors, workspace, util
from idaes.util.system import mkdtemp
from .util import init_logging

__author__ = "Dan Gunter <dkgunter@lbl.gov>"

if sys.platform.startswith("win"):
    pytest.skip("skipping DMF tests on Windows", allow_module_level=True)

init_logging()
_log = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def wspath():
    dirname = mkdtemp()
    yield dirname
    # teardown
    shutil.rmtree(dirname)


def test_workspace_init(wspath):
    commands.workspace_init(wspath, {"some": "metadata"})
    try:
        commands.workspace_init(wspath, {"some": "metadata"})
        assert False, "Duplicate workspace init succeeded"
    except errors.CommandError:
        pass


def test_workspace_info(wspath):
    commands.workspace_init(wspath, {"some": "metadata"})
    commands.workspace_info(wspath)

    #    subdir = os.path.join(wspath, 'stuff')
    #    os.mkdir(subdir)
    #    commands.workspace_info(subdir)

    notasubdir = os.path.join(wspath, "nope")
    try:
        commands.workspace_info(notasubdir)
        assert False, "Nonexistent subdir workspace info success"
    except errors.CommandError:
        pass


def test_find_html_docs(wspath):
    filedir = os.path.dirname(__file__)
    docpath = os.path.join(filedir, "..", "docs", "build", "html")
    if os.path.exists(docpath):
        commands.workspace_init(wspath, {}, html_paths=[docpath])
        dmfobj = dmfbase.DMF(wspath)
        filenames = commands.find_html_docs(dmfobj, dmfobj)
        assert len(filenames) > 0
