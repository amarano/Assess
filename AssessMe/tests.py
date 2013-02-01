"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from AssessMe.models import *
from datetime import date

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class AverageScoreTest(TestCase):
    def test_best_average_score(self):

        multiple_choice = AssessmentType()
        multiple_choice.name = "Multiple Choice"
        multiple_choice.description = "Multiple Choice"

        short_answer = AssessmentType()
        short_answer.name = "Short Answer"
        short_answer.description = "Short Answer"

        essay = AssessmentType()
        essay.name = "Essay"
        essay.description = "Essay"

        types = [multiple_choice, short_answer, essay]
        student = Student()
        student.first_name = "angelo"
        student.last_name = "marano"
        student.birthdate = date.today()
        student.foreign_id = "12345678"

        for i, t in enumerate(types): #I'm going to make the first type the best score
            for i in range(5):
                a = Assessment()
                a.type = t
                score = AssessmentScore()
                score.assessment = a
                score.value = 100.0 - i # subtract the index from the score, lame, right?
                score.student = student

        self.assertEqual(types[0], student.most_effective_assessment_type())
        self.assertNotEqual(types[1], student.most_effective_assessment_type())