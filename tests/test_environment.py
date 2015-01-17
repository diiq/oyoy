from test_case import TestCase
from interpreter.environment import Env

class EnvironmentTests(TestCase):
    def setUp(self):
        self.lexical_environment = Env(None, None)
        self.calling_environment = Env(None, None)
        self.local = Env(self.lexical_environment,
                         self.calling_environment)

    def test_local_set(self):
        self.local.set("a", 5)
        self.assertEqual(self.local.this_environment["a"], 5)

    def test_local_lookup(self):
        self.local.set("a", 5)
        self.assertEqual(self.local.lookup("a"), 5)

    def test_leaked_lookup(self):
        self.calling_environment.set("a", 6)
        self.local.leak("a")

        self.assertEqual(self.local.lookup("a"), 6)

    def test_leaked_set(self):
        self.calling_environment.set("a", 6)
        self.local.leak("a")
        self.local.set("a", 10)

        self.assertEqual(self.calling_environment.this_environment["a"], 10)

    def test_lexical_environment_lookup(self):
        self.lexical_environment.set("a", 15)
        self.assertEqual(self.local.lookup("a"), 15)

    def test_alter_set(self):
        self.local.alter("a")
        self.local.set("a", 20)

        self.assertEqual(self.local.lookup("a"), 20)
        self.assertEqual(self.lexical_environment.this_environment["a"], 20)

    def test_default_lookup(self):
        self.calling_environment.set("a", 6)
        self.lexical_environment.set("a", 12)

        self.assertEqual(self.local.lookup("a"), 12)
