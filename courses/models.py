from django.db import models
from django.db.models.signals import post_save
from moodle.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save

class Course(models.Model):
    """ Course model is to store the information of each course \n

    :param instructor: Name of the instructor
    :param name: Name of the course
    :param students: All the students who took the course
    :param joincode: Code to join the course

    """
    instructor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ins_courses') #assuming 1 instructor/course.
    name = models.CharField(max_length=128,default = '')
    students = models.ManyToManyField(User,related_name='stud_courses')
    joincode = models.CharField(max_length=10,default = '')

    def _str_(self):
        return self.name

class Assignment(models.Model):
    """ Assignment model is to store the information of each assignment \n
    
    :param name: Name of the Assignment
    :param file: File related to assignment 
    :param file_name: Name of the problem file
    :param weblink: Website link related to assignment
    :param statement: Problem statement for the assignment
    :param marks: Maximum marks for assignment
    :param weightage: Contribution of this assignment to the course
    :param extensions: Valid extension of the submissions
    :param deadline: Time till which the submissions are accepted

    """
    name = models.CharField(max_length=128,default='')
    link = models.URLField(default='')
    file_name = models.CharField(max_length=100,default='problem_statement')
    file = models.FileField(upload_to='assignments',blank=True)
    statement = models.CharField(max_length=300,default='')
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    maxmarks = models.IntegerField(default=100)
    deadline = models.DateTimeField(blank=False) #need to set while creating assign.
    weightage = models.IntegerField(default=0)
    extensions = models.PositiveSmallIntegerField(default = 0)
    text_file = models.FileField(upload_to='submissions',blank=True)

    def _str_(self):
        return self.name

class FileSubmission(models.Model):
    """ Filesubmission is a model to store the submissions \n

    :param user: Name of the user who submitted the file
    :param file: Submitted file 
    :param file_name: Name of the file submitted 
    :param assignment: Assignment to which the file is submitted
    :param feedback: Feedback for the submission
    :param corrected: Whether the submission is submitted or not
    :param grade: Marks for this submission
    :param sub_time: Time at which the student submitted the file
    :type sub_time: last modified

    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions',blank=True)
    file_name = models.CharField(max_length=100,default='submission')
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    feedback = models.CharField(max_length=500,default='Your Feedback Appears Here')
    corrected = models.CharField(max_length=10,default='NO')
    grade = models.IntegerField(default=-1)
    sub_time = models.DateTimeField(auto_now=True) #last 'MODIFIED' time. // automatically updates itself.


    def _str_(self):
        return self.user.username +''  + self.file_name + '' + self.assignment.name
