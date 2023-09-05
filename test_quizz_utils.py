import unittest
from quizz_utils import answer_check

# Your answer_check function here...

class TestAnswerCheck(unittest.TestCase):

    def test_answer_in_choices(self):
        quizz = {
            'question': 'Who are the instructors for MIT 6S191 introduction to deep learning?',
            'choice_a': 'Alexander Amini',
            'choice_b': 'Alva Solimani',
            'choice_c': 'Both Alexander Amini and Alva Solimani',
            'choice_d': 'None of the above',
            'answer': 'Both Alexander Amini and Alva Solimani'
        }

        modified_quizz = answer_check(quizz)
        self.assertEqual(modified_quizz['answer'], 'choice_c')

    def test_answer_not_in_choices(self):
        quizz = {
            'question': 'What is the capital of France?',
            'choice_a': 'Paris',
            'choice_b': 'Berlin',
            'choice_c': 'London',
            'choice_d': 'Madrid',
            'answer': 'Moscow'
        }

        modified_quizz = answer_check(quizz)
        self.assertEqual(modified_quizz['answer'], 'Moscow')


    def test_answer_is_a_choices(self):
        quizz = {
            'question': 'What is the capital of France?',
            'choice_a': 'Paris',
            'choice_b': 'Berlin',
            'choice_c': 'London',
            'choice_d': 'Madrid',
            'answer': 'choice_a'
        }

        modified_quizz = answer_check(quizz)
        self.assertEqual(modified_quizz['answer'], 'choice_a')

if __name__ == '__main__':
    unittest.main()
