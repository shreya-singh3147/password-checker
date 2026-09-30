# Tests for password_checker.py
# Run these with:  python -m unittest test_password_checker.py

import unittest
from password_checker import check_password, get_rating, make_strong_password


class TestCheckPassword(unittest.TestCase):

    def test_common_password_scores_zero(self):
        score, tips = check_password("password")
        self.assertEqual(score, 0)
        self.assertTrue(len(tips) > 0)

    def test_short_password_gets_low_score(self):
        score, tips = check_password("ab1!")
        self.assertTrue(score <= 3)

    def test_strong_password_gets_high_score(self):
        score, tips = check_password("Xk9!mQ2p@Lw7T")
        self.assertTrue(score >= 5)

    def test_missing_uppercase_gives_tip(self):
        score, tips = check_password("lowercase123!")
        joined_tips = " ".join(tips)
        self.assertIn("UPPERCASE", joined_tips)

    def test_missing_special_character_gives_tip(self):
        score, tips = check_password("NoSymbolsHere123")
        joined_tips = " ".join(tips)
        self.assertIn("special character", joined_tips)

    def test_repeated_characters_lower_score(self):
        score_repeated, tips_repeated = check_password("Aaa12345!")
        score_normal, tips_normal = check_password("Abc12345!")
        self.assertTrue(score_repeated <= score_normal)

    def test_easy_pattern_lowers_score(self):
        score_pattern, tips_pattern = check_password("Xk9!mQabc2p@Lw7T")
        score_no_pattern, tips_no_pattern = check_password("Xk9!mQzzz2p@Lw7T")
        self.assertTrue(score_pattern <= score_no_pattern)

    def test_score_never_goes_below_zero(self):
        score, tips = check_password("aaa")
        self.assertTrue(score >= 0)


class TestGetRating(unittest.TestCase):

    def test_zero_is_weak(self):
        self.assertEqual(get_rating(0), "WEAK")

    def test_two_is_weak(self):
        self.assertEqual(get_rating(2), "WEAK")

    def test_three_is_medium(self):
        self.assertEqual(get_rating(3), "MEDIUM")

    def test_four_is_medium(self):
        self.assertEqual(get_rating(4), "MEDIUM")

    def test_five_is_strong(self):
        self.assertEqual(get_rating(5), "STRONG")

    def test_six_is_very_strong(self):
        self.assertEqual(get_rating(6), "VERY STRONG")


class TestMakeStrongPassword(unittest.TestCase):

    def test_default_length_is_14(self):
        password = make_strong_password()
        self.assertEqual(len(password), 14)

    def test_custom_length_is_respected(self):
        password = make_strong_password(20)
        self.assertEqual(len(password), 20)

    def test_two_generated_passwords_are_different(self):
        password_one = make_strong_password()
        password_two = make_strong_password()
        self.assertNotEqual(password_one, password_two)

    def test_generated_password_scores_well(self):
        password = make_strong_password()
        score, tips = check_password(password)
        self.assertTrue(score >= 5)


if __name__ == "__main__":
    unittest.main()