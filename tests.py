import unittest
from bot.respondent import make_answer


class TestIn(unittest.TestCase):

    def test_templates(self):
        a = make_answer("In which date were $50?", "Test")
        self.assertEqual(a, "In 24.05.14.")
        a = make_answer("How much integer was in the 25.05.14?", "Test")
        self.assertEqual(a, "The 5.")
        a = make_answer("What currency there is in 12%?", "Test")
        self.assertEqual(a, "The $250.")
        a = make_answer("Where number of float is 12%?", "Test")
        self.assertEqual(a, "The 5.5.")

    def test_intervals(self):
        a = make_answer("In which date were more 3?", "Test")
        self.assertEqual(a, "In 24.05.14, 25.05.14, 26.05.14.")
        a = make_answer("In which date were less 3?", "Test")
        self.assertEqual(a, "In 28.05.14, 29.05.14, 30.05.14.")
        a = make_answer("In which date were after 3?", "Test")
        self.assertEqual(a, "In 24.05.14, 25.05.14, 26.05.14.")
        a = make_answer("In which date were before 3?", "Test")
        self.assertEqual(a, "In 28.05.14, 29.05.14, 30.05.14.")

    def test_connectors(self):
        a = make_answer("In which date and float were 3?", "Test")
        self.assertEqual(a, "In 27.05.14 8.5.")
        a = make_answer("In which date were 2 and 28%?", "Test")
        self.assertEqual(a, "In 30.05.14.")
        a = make_answer("In which date or float were 3?", "Test")
        self.assertEqual(a, "In 27.05.14 or 8.5.")
        a = make_answer("In which date were 2 or 24%?", "Test")
        self.assertEqual(a, "In 28.05.14, 29.05.14, 30.05.14.")

    def test_errors(self):
        a = make_answer("In which date were 100?", "Test")
        self.assertEqual(a, "There is no such data")
        a = make_answer("None Template?", "Test")
        self.assertEqual(a, "Have no suitable template (can't understand your question)")
        a = make_answer("In which date were 100?", "dsfasdfadfadsfasdfasdfdsafadsfdasfadsfaetewd")
        self.assertEqual(a, "Wrong dataset. There is no dataset with this name.")
        a = make_answer("", "Test")
        self.assertEqual(a, "Void question")
        a = make_answer("fdsafsadfasdfsdafasdfsdfdsafdas dfadsfdsfdsfadsfdsfadsfasdfadsfsd", "")
        self.assertEqual(a, "No suitable dataset. Please, remake your question by the rules (use \"/rules\" command)")


if __name__ == '__main__':
    unittest.main()
