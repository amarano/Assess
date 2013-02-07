from django.db import models
from itertools import groupby
import operator

class BaseModelObject(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

#Peoples

class HumanBase(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=25)
    birthdate = models.DateField()
    foreign_id = models.CharField(max_length=50)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

class StudentManager(models.Manager):
    pass

class Student(HumanBase):

    current_grade = models.DecimalField(decimal_places=2, max_digits=5, default=0.00)

    def most_effective_assessment_type(self):
        """
        :type : AssessmentType
        """
        score_avgs = self.get_assessment_type_score_averages()
        best_average_score = max(score_avgs.iteritems(), key=operator.itemgetter(1))[0]
        return best_average_score

    def least_effective_assessment_type(self):

        score_avgs = self.get_assessment_type_score_averages()
        worst_average_score = min(score_avgs.iteritems(), key=operator.itemgetter(1))[0]
        return worst_average_score

    def most_effective_instruction_type(self):

        all_instruction_periods = InstructionPeriod.objects.filter(assessments__assessmentscore__student__id = self.id)

        return all_instruction_periods


    def get_assessment_type_score_averages(self):
        """
        :type : Dictionary
        """
        retval = {}

        all_scores = self.assessmentscore_set.all()
        all_scores = sorted(all_scores, key=lambda x : x.assessment.type)

        score_groups = groupby(all_scores, lambda x : x.assessment.type)
        for k, v in score_groups:
            score_list = list(v)
            retval[k] = sum(map(lambda x: x.value, score_list)) / len(score_list)

        return retval

    objects = StudentManager()

class AssessmentType(BaseModelObject):
    pass

class Assessment(BaseModelObject):

    type = models.ForeignKey(AssessmentType)

class AssessmentScore(BaseModelObject):

    assessment = models.ForeignKey(Assessment)
    value = models.DecimalField(decimal_places=2, max_digits=5)
    student = models.ForeignKey(Student)

class Teacher(HumanBase):

    assessments = models.ManyToManyField(Assessment)

class Classroom(BaseModelObject):

    students = models.ManyToManyField(Student)
    teachers = models.ManyToManyField(Teacher)

class InstructionTypeManager(models.Manager):

    def create_with_automatic_percentage(self):
        percentages = [x.percentage for x in self.all()]
        remaining_percent = 100 - sum(percentages)

        im = InstructionType(percentage=remaining_percent)
        return im

class InstructionType(BaseModelObject):
    percentage = models.PositiveIntegerField()

    objects = InstructionTypeManager()

class InstructionPeriod(BaseModelObject):

    start_date = models.DateField()
    end_date = models.DateField()
    assessments = models.ManyToManyField(Assessment)
    instruction_types = models.ManyToManyField(InstructionType)




