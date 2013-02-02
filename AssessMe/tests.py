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
    
    def get_test_assessment_types(self):
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
        [type.save() for type in types]
        return types

    def get_test_student(self):
        student = Student()
        student.first_name = "angelo"
        student.last_name = "marano"
        student.birthdate = date.today()
        student.foreign_id = "12345678"
        student.save()
        return student

    def populate_student_scores(self, student, types):
        for i, t in enumerate(types): #I'm going to make the first type the best score
            for j in range(5):
                a = Assessment()
                a.type = t
                a.save()

                score = AssessmentScore()
                score.assessment = a
                score.value = 100.0 - i # subtract the index from the score, lame, right?
                score.student = student
                score.save()
        return a

    def clean_test(self, a, student, types):
        a.delete()
        [s.delete() for s in student.assessmentscore_set.all()]
        student.delete()
        [t.delete() for t in types]

    def test_best_average_score(self):

        types = self.get_test_assessment_types()

        student = self.get_test_student()

        a = self.populate_student_scores(student, types)

        most_eff_a_t = student.most_effective_assessment_type()
        self.assertEqual(types[0], most_eff_a_t)
        self.assertNotEqual(types[1], most_eff_a_t)

        self.clean_test(a, student, types)

    def test_worst_average_score(self):
        types = self.get_test_assessment_types()

        student = self.get_test_student()

        a = self.populate_student_scores(student, types)

        most_eff_a_t = student.most_effective_assessment_type()
        self.assertEqual(types[len(types) - 1], most_eff_a_t)
        self.assertNotEqual(types[0], most_eff_a_t)

        self.clean_test(a, student, types)