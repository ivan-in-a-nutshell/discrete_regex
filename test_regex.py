from regex import RegexFSM
import unittest

class TestRegexFSM(unittest.TestCase):
    def test_accepts_string_matching_simple_pattern(self):
        regex = RegexFSM("a*")
        self.assertTrue(regex.check_string("aaaa"))
        self.assertTrue(regex.check_string(""))
        self.assertFalse(regex.check_string("b"))

    def test_accepts_string_matching_dot_pattern(self):
        regex = RegexFSM(".")
        self.assertTrue(regex.check_string("a"))
        self.assertTrue(regex.check_string("1"))
        self.assertFalse(regex.check_string(""))

    def test_star(self):
        regex = RegexFSM("a*b*c*d*")
        self.assertTrue(regex.check_string('aaaaddd'))
        self.assertTrue(regex.check_string('aaaa'))

    def test_accepts_string_matching_plus_pattern(self):
        regex = RegexFSM("a+")
        self.assertTrue(regex.check_string("a"))
        self.assertTrue(regex.check_string("aaaa"))
        self.assertFalse(regex.check_string(""))

    def test_rejects_string_with_unsupported_characters(self):
        with self.assertRaises(AttributeError):
            RegexFSM("a#")

    def test_accepts_string_matching_combined_pattern(self):
        regex = RegexFSM("a*4.+hi")
        self.assertTrue(regex.check_string("aaaa4uhi"))
        self.assertTrue(regex.check_string("4uhi"))
        self.assertFalse(regex.check_string("4u"))
        self.assertFalse(regex.check_string("aaaa4uhiX"))

    def test_accepts_empty_string_for_empty_pattern(self):
        regex = RegexFSM("")
        self.assertTrue(regex.check_string(""))

    def test_rejects_string_not_matching_termination_state(self):
        regex = RegexFSM("a")
        self.assertFalse(regex.check_string("aa"))

    def test_accepts_string_matching_ascii_class_pattern(self):
        regex = RegexFSM("[a-zA-Z0-9]")
        self.assertTrue(regex.check_string("a"))
        self.assertTrue(regex.check_string("Z"))
        self.assertTrue(regex.check_string("5"))
        self.assertFalse(regex.check_string("!"))
        self.assertFalse(regex.check_string(""))

    def test_accepts_string_matching_combined_ascii_class_and_literal(self):
        regex = RegexFSM("[a-z]4+")
        self.assertTrue(regex.check_string("a444"))
        self.assertTrue(regex.check_string("z4"))
        self.assertFalse(regex.check_string("44"))
        self.assertFalse(regex.check_string("a"))

    def test_accepts_string_matching_nested_star_and_ascii_class(self):
        regex = RegexFSM("[a-z]*4*")
        self.assertTrue(regex.check_string("aaaa444"))
        self.assertTrue(regex.check_string("4"))
        self.assertTrue(regex.check_string(""))
        self.assertFalse(regex.check_string("A4"))
