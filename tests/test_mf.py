#!/usr/bin/python3.3
import unittest

from py2exe.mf3 import ModuleFinder
from tests.test_make import _TestPackageBase, Test_PEP328 as _PEP328

class MFTest(_TestPackageBase):
    data = """
    testmods/test_tools.py
            from testmods.tools import bar
            from testmods.tools import baz
            from testmods.tools import spam
            from testmods.tools import foo
            try: from testmods.tools import spam_and_eggs
            except ImportError: pass

    testmods/__init__.py
            # empty

    testmods/tools/spamfoo.py
            spam = 'spam'
            foo = 'foo'

    testmods/tools/bazbar.py
            baz = 'baz'
            bar = 'bar'

    testmods/tools/__init__.py
            from .bazbar import *
            from .spamfoo import spam
            from .spamfoo import foo
    """

    # c:/python33/lib/collections/
    def test_collections(self):
        """
        collections contains namedtuple, ChainMap, OrderedDict
        global names, which are imported from string, inspect,
        and others.
        """
        
        mf = ModuleFinder()
        mf.import_hook("collections")
        modules = set([name for name in mf.modules
                       if name.startswith("collections")])
        self.assertEqual({"collections", "collections.abc"},
                         modules)
        missed = [name for name in mf.missing()
                  if name.startswith("collections")]
        self.assertEqual([], missed)

    # /python33/lib/site-packages/nose/tools/nontrivial.py
    def test_tools(self):
        """
        check that these are not reported as missing modules:
        
        - testmods.tools.bar
        - testmods.tools.baz
        - testmods.tools.spam
        - testmods.tools.foo
        """

        mf = ModuleFinder(verbose=2)
        mf.import_hook("testmods.test_tools")
        self.assertEqual(set(mf.modules.keys()), {
            "testmods",
            "testmods.test_tools",
            "testmods.tools",
            "testmods.tools.bazbar",
            "testmods.tools.spamfoo"})
        self.assertFalse(mf.missing())

class Test_PEP328(_PEP328):
    def test_pep328(self):
        """
        The package structure from pep328.
        """

        mf = ModuleFinder()
        mf.import_hook("pep328.sub1")
        self.assertEqual(set(mf.modules.keys()),
                         {"pep328",
                          "pep328.moduleA",
                          "pep328.subpackage1",
                          "pep328.subpackage1.moduleX",
                          "pep328.subpackage1.moduleY",
                          "pep328.subpackage2",
                          "pep328.subpackage2.moduleZ",
                          })
        self.assertFalse(mf.missing())

if __name__ == "__main__":
    unittest.main()
