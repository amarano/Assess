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

class AssessmentScore(BaseModelObject):
    assessment = models.ForeignKey(Assessment)
    score = models.DecimalField()

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

    def most_effective_assessment_type(self):
        all_scores = self.assessment_set.all()
        return max(groupby(all_scores, lambda x : x.type), key=sum(operator.itemgetter(1)) / len(operator.itemgetter(1)))[0]

    def least_effective_assessment_type(self):
        all_scores = self.assessment_set.all()
        return min(groupby(all_scores, lambda x : x.type), key=sum(operator.itemgetter(1)) / len(operator.itemgetter(1)))[0]

class Student(HumanBase):
    current_grade = models.DecimalField()
    scores = models.ManyToManyField(AssessmentScore)

    objects = StudentManager()


class Teacher(HumanBase):
    assessments = models.ManyToManyField(Assessment)

