from test_case import TestCase
from interpreter.environment import Env

class EnvironmentTests(TestCase):
    def setUp(self):
        self.lexical = Env(None, None)
        self.dynamic = Env(None, None)
        self.local = Env(self.lexical, self.dynamic)

    def test_local_set(self):
        self.local.set("a", 5)
        self.assertEqual(self.local.active["a"], 5)

    def test_local_lookup(self):
        self.local.set("a", 5)
        self.assertEqual(self.local.lookup("a"), 5)

    def test_leaked_lookup(self):
        self.dynamic.set("a", 6)
        self.local.leak("a")

        self.assertEqual(self.local.lookup("a"), 6)

    def test_leaked_set(self):
        self.dynamic.set("a", 6)
        self.local.leak("a")
        self.local.set("a", 10)

        self.assertEqual(self.dynamic.active["a"], 10)

    def test_lexical_lookup(self):
        self.lexical.set("a", 15)
        self.assertEqual(self.local.lookup("a"), 15)

    def test_alter_set(self):
        self.local.alter("a")
        self.local.set("a", 20)

        self.assertEqual(self.local.lookup("a"), 20)
        self.assertEqual(self.lexical.active["a"], 20)

    def test_default_lookup(self):
        self.dynamic.set("a", 6)
        self.lexical.set("a", 12)

        self.assertEqual(self.local.lookup("a"), 12)
