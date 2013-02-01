from django.db import models
from itertools import groupby
import operator

class BaseModelObject(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField()
    description = models.CharField()

    def __unicode__(self):
        return self.name

class Assessment(BaseModelObject):
    type = models.ForeignKey(AssessmentType)

class AssessmentType(BaseModelObject):
    pass

class AssessmentScore(BaseModelObject):
    assessment = models.ForeignKey(Assessment)
    value = models.DecimalField()
    student = models.ForeignKey(Student)

class InstructionPeriod(BaseModelObject):
    start_date = models.DateField()
    end_date = models.DateField()
    assessments = models.ManyToManyField(Assessment)

class Classroom(BaseModelObject):
    students = models.ManyToManyField(Student)
    teachers = models.ManyToManyField(Teacher)

#Peoples

class HumanBase(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    birthdate = models.DateField()
    foreign_id = models.CharField()

    def __unicode__(self):
        return self.first_name + " " + self.last_name

class StudentManager(models.Manager):
    pass

class Student(HumanBase):
    current_grade = models.DecimalField()

    def most_effective_assessment_type(self):
        """
        :type : AssessmentType
        """
        best_average_score = max(self.get_assessment_type_score_averages(), key=operator.itemgetter(1))
        assert isinstance(best_average_score, object)
        return best_average_score[0]

    def least_effective_assessment_type(self):
        worst_average_score = min(self.get_assessment_type_score_averages(), key=operator.itemgetter(1))
        assert isinstance(worst_average_score, object)
        return worst_average_score[0]

    def get_assessment_type_score_averages(self):
        """
        :type : Dictionary
        """
        retval = {}

        all_scores = self.scores.all()
        all_scores = sorted(all_scores, key=lambda x : x.assessment.type)

        score_groups = groupby(all_scores, lambda x : x.assessment.type)
        for k, v in score_groups:
            retval[k] = sum(v) / len(v)

        return retval

    objects = StudentManager()


class Teacher(HumanBase):
    assessments = models.ManyToManyField(Assessment)

