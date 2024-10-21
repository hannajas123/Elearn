from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
class Department(models.Model):
    departmentname=models.CharField(max_length=50)
class Course(models.Model):
    coursename=models.CharField(max_length=50)
    totalsem=models.CharField(max_length=50)
    DEPARTMENT=models.ForeignKey(Department,on_delete=models.CASCADE)
class Subject(models.Model):
    Subname=models.CharField(max_length=50)
    semester=models.CharField(max_length=50)
    COURSE=models.ForeignKey(Course,on_delete=models.CASCADE)
class Teacher(models.Model):
    tname=models.CharField(max_length=50)
    dob=models.DateField()
    gender=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    hname=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    photo=models.CharField(max_length=550)
    status=models.CharField(max_length=50)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
class Student(models.Model):
    sname=models.CharField(max_length=50)
    dob=models.DateField()
    gender=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    hname=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    photo=models.CharField(max_length=550)
    status=models.CharField(max_length=50)
    sem=models.CharField(max_length=50)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    COURSE=models.ForeignKey(Course,on_delete=models.CASCADE)
class Syllabus(models.Model):
    syllabus=models.CharField(max_length=500)
    year=models.CharField(max_length=50)
    SUBJECT=models.ForeignKey(Subject,on_delete=models.CASCADE)
class Selected_Subject(models.Model):
    SUBJECT=models.ForeignKey(Subject,on_delete=models.CASCADE)
    TEACHER=models.ForeignKey(Teacher,on_delete=models.CASCADE)
class Notes(models.Model):
    note=models.CharField(max_length=500)
    title=models.CharField(max_length=100)
    date=models.DateField()
    SELECTED_SUBJECT=models.ForeignKey(Selected_Subject,on_delete=models.CASCADE)
class QuestionBank(models.Model):
    questions=models.CharField(max_length=500)
    title=models.CharField(max_length=100)
    date=models.DateField()
    SELECTED_SUBJECT=models.ForeignKey(Selected_Subject,on_delete=models.CASCADE)
class Lecture_video(models.Model):
    videos=models.CharField(max_length=500)
    title=models.CharField(max_length=100)
    date=models.DateField()
    SELECTED_SUBJECT=models.ForeignKey(Selected_Subject,on_delete=models.CASCADE)
class Doubts(models.Model):
    date=models.DateField()
    doubt=models.CharField(max_length=300)
    Solution=models.CharField(max_length=300)
    Status=models.CharField(max_length=300)
    TEACHER = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)





