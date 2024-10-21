import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
##########################################ADMIN####################################
from myapp.models import *


def login(request):
    return render(request,'login.html')
def login_post(request):
    user=request.POST['user']
    pasw=request.POST['psw']
    lobj = Login.objects.filter(username=user,password=pasw)
    if lobj.exists():
        log=Login.objects.get(username=user,password=pasw)
        request.session['lid']=log.id
        if log.type=='admin':
            return HttpResponse('''<script>alert('Login Successfully');window.location='/myapp/AdminHome/'</script>''')
        elif log.type == 'teacher':
           return  HttpResponse('''<script>alert('logined');window.location='/myapp/Teacher_home/'</script>''')
        elif log.type == 'student':
           return  HttpResponse('''<script>alert('logined');window.location='/myapp/S_student_home/'</script>''')
        else:
            return HttpResponse('''<script>alert('invalid password or username');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert('invalid password or username');window.location='/myapp/login/'</script>''')



def logout(request):
    request.session['lid']=""
    return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')


def Add_cousre(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Department.objects.all()
    return render(request,'Admin/Add Course.html',{'data':res})
def Add_course_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    dep=request.POST['select']
    cname=request.POST['select2']
    sem=request.POST['select3']
    obj=Course()
    obj.coursename=cname
    obj.totalsem=sem
    obj.DEPARTMENT_id=dep
    obj.save()
    return HttpResponse('''<script>alert("Added");window.location='/myapp/Add_cousre/#abc'</script>''')


def Add_Department(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    return render(request,'Admin/Add Department.html')
def Add_department_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    dep=request.POST["textfield"]
    if Department.objects.filter(departmentname=dep).exists():
        return HttpResponse(
            '''<script>alert("Department already exists");window.location='/myapp/Add_Department/#abc'</script>''')
    else:

        obj=Department()
        obj.departmentname=dep
        obj.save()
        return HttpResponse('''<script>alert("Added");window.location='/myapp/Add_Department/#abc'</script>''')
def Add_Subject(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Course.objects.all()
    return render(request,'Admin/Add subject.html',{'data':res})
def Add_subject_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    course=request.POST['select']
    subname=request.POST['textfield']
    sem=request.POST['textfield2']
    obj=Subject()
    obj.COURSE_id=course
    obj.Subname=subname
    obj.semester=sem
    obj.save()

    return HttpResponse('''<script>alert("Added");window.location='/myapp/Add_Subject/#abc'</script>''')
def Add_syllabus(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Subject.objects.all()
    return render(request,'Admin/Add Syllabus.html',{'data':res})
def Add_syllabus_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    sub=request.POST['select']
    pic=request.FILES['fileField']
    year=request.POST['textfield2']
    from datetime import datetime
    date = datetime.now().strftime('Y%m%d-%H%M%S') + ".pdf"
    fs = FileSystemStorage()
    fs.save(date, pic)
    path = fs.url(date)
    obj=Syllabus()
    obj.syllabus=path
    obj.year=year
    obj.SUBJECT_id=sub
    obj.save()
    return HttpResponse('''<script>alert("Added");window.location='/myapp/Add_syllabus/#abc'</script>''')
def AdminHome(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    return render(request,'Admin/AdminHome.html')
def Approved_teachers(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Teacher.objects.filter(status='approved')

    return render(request,'Admin/Approved Teacher.html',{'data':res})
def Approve_techr(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Teacher.objects.filter(id=id).update(status='approved')
    tlid = Teacher.objects.get(id=id).LOGIN_id
    res1=Login.objects.filter(id=tlid).update(type='teacher')

    return HttpResponse('''<script>alert("Approved");window.location='/myapp/View_teachers/#abc'</script>''')

def Approved_teacher_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']
    res = Teacher.objects.filter(status='approved', tname__icontains=srch)
    return render(request,'Admin/Approved Teacher.html',{'data':res})
def Change_password(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    return render(request,'Admin/change password.html')
def change_pass_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']

    log = Login.objects.filter(id=request.session['lid'], password=currentpassword)
    if log.exists():
        if newpassword == confirmpassword:
            log1 = Login.objects.filter(id=request.session['lid'], password=currentpassword).update(
                password=newpassword)

            return HttpResponse('''<script>alert('password change success');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert('password not change ');window.location='/myapp/Change_password/#abc'</script>''')
    else:
        return HttpResponse(
            '''<script>alert('password not change ');window.location='/myapp/Change_password/#abc'</script>''')


def Edit_course(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Department.objects.all()
    res1=Course.objects.get(id=id)
    return render(request,'Admin/Edit Course.html',{'data':res,'data1':res1})
def edit_course_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    dep = request.POST['select']
    cname = request.POST['cource']
    sem = request.POST['nos']
    did=request.POST['did']
    obj = Course.objects.get(id=did)
    obj.coursename = cname
    obj.totalsem = sem
    obj.DEPARTMENT_id = dep
    obj.save()
    return HttpResponse('''<script>alert("Updated");window.location='/myapp/View_course/#abc'</script>''')
def delete_cour(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Course.objects.filter(id=id).delete()

    return HttpResponse('''<script>alert("Deleted");window.location='/myapp/View_course/#abc'</script>''')
def Edit_department(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res1=Department.objects.get(id=id)

    return render(request,'Admin/Edit Department.html',{'data':res1})
def edit_department_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    dep = request.POST["textfield"]
    id=request.POST['id']
    obj = Department.objects.get(id=id)
    obj.departmentname = dep
    obj.save()
    return HttpResponse('''<script>alert("Updated");window.location='/myapp/View_department/#abc'</script>''')
def delete_dep(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Department.objects.filter(id=id).delete()

    return HttpResponse('''<script>alert("Deleted");window.location='/myapp/View_department/#abc'</script>''')
def Edit_subject(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Course.objects.all()
    res1=Subject.objects.get(id=id)
    return render(request,'Admin/Edit subject.html',{'data':res,'data1':res1})
def edit_subject_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    course = request.POST['select']
    subname = request.POST['textfield']
    sem = request.POST['textfield2']
    id = request.POST['id1']
    obj = Subject.objects.get(id=id)
    obj.COURSE_id = course
    obj.Subname = subname
    obj.semester = sem
    obj.save()

    return HttpResponse('''<script>alert("Updated");window.location='/myapp/View_subject/#abc'</script>''')
def delete_subject(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Subject.objects.filter(id=id).delete()

    return HttpResponse('''<script>alert("Deleted");window.location='/myapp/View_subject/#abc'</script>''')

def Edit_syllabus(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Subject.objects.all()
    res1=Syllabus.objects.get(id=id)
    return render(request,'Admin/Edit Syllabus.html',{'data':res,'data1':res1})
def edit_syllabus_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    sub = request.POST['select']
    year = request.POST['textfield2']
    did=request.POST['id1']
    if 'fileField' in request.FILES:
        pic = request.FILES['fileField']

        from datetime import datetime
        date = datetime.now().strftime('Y%m%d-%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, pic)
        path = fs.url(date)
        obj = Syllabus.objects.get(id=did)
        obj.syllabus = path
        obj.year = year
        obj.SUBJECT_id = sub
        obj.save()
        return HttpResponse('''<script>alert("Updated");window.location='/myapp/View__syllabus/#abc'</script>''')
    else:
        obj = Syllabus.objects.get(id=did)
        obj.year = year
        obj.SUBJECT_id = sub
        obj.save()
        return HttpResponse('''<script>alert("Updated");window.location='/myapp/View__syllabus/#abc'</script>''')
def delete_syllabus(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Syllabus.objects.filter(id=id).delete()

    return HttpResponse('''<script>alert("Deleted");window.location='/myapp/View__syllabus/#abc'</script>''')

def Rejected_teachers(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Teacher.objects.filter(status='rejected')
    return render(request,'Admin/Rejected Teacher.html',{'data':res})
def rejected_teacher_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']
    res = Teacher.objects.filter(status='rejected', tname__icontains=srch)
    return render(request,'Admin/Rejected Teacher.html',{'data':res})
def Reject_techr(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Teacher.objects.filter(id=id).update(status='rejected')

    return HttpResponse('''<script>alert("Rejected");window.location='/myapp/View_teachers/#abc'</script>''')
def View_course(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Course.objects.all()
    return render(request,'Admin/View Course.html',{'data':res})
def view_course_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch=request.POST['textfield']

    res = Course.objects.filter(coursename__icontains=srch)
    return render(request, 'Admin/View Course.html', {'data': res})
def View_department(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Department.objects.all()
    return render(request,'Admin/View department.html',{'data':res})
def view_depatment_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch=request.POST['textfield']

    res = Department.objects.filter(departmentname__icontains=srch)
    return render(request, 'Admin/View department.html', {'data': res})
def View_students(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Student.objects.all()
    c=Course.objects.all()
    return render(request,'Admin/View Students.html',{'data':res,'c':c})
def view_student_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    # btn=request.POST['button']
    if request.POST['button'] == 'Search':
        srch = request.POST['textfield']
        c = Course.objects.all()

        res = Student.objects.filter(sname__icontains=srch)
        return render(request, 'Admin/View Students.html', {'data': res,'c':c})
    else:
        cid= request.POST['cname']
        sem= request.POST['sem']

        c = Course.objects.all()

        res = Student.objects.filter(sem=sem,COURSE_id=cid)
        return render(request, 'Admin/View Students.html', {'data': res,'c':c})

def View_subject(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Subject.objects.all()
    return render(request,'Admin/View Subject.html',{'data':res})
def view_subject_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch=request.POST['textfield']

    res = Subject.objects.filter(Subname__icontains=srch)
    return render(request, 'Admin/View Subject.html', {'data': res})
def View__syllabus(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Syllabus.objects.all()
    return render(request,'Admin/View Syllabus.html',{'data':res})
def view_syllabus_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch=request.POST['textfield']
    res = Syllabus.objects.filter(SUBJECT__Subname__icontains=srch)
    return render(request, 'Admin/View Syllabus.html', {'data': res})
def View_teachers(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Teacher.objects.filter(status='pending')
    return render(request,'Admin/View Teacher.html',{'data':res})
def view_teacher_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch=request.POST['textfield']
    res=Teacher.objects.filter(status='pending',tname__icontains=srch)

    return render(request,'Admin/View Teacher.html',{'data':res})

####################################Teacher##################################################






def Add_Lecture_video(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Selected_Subject.objects.get(SUBJECT_id=id)
    return render(request,'Teacher/Add Lecture video.html',{'data':res,'id':id})
def add_Lecture_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    title=request.POST['textfield']
    vid=request.FILES['fileField']
    did=request.POST['id1']
    id = request.POST['id']

    from datetime import datetime
    date1=datetime.now()

    date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".mp4"
    fs = FileSystemStorage()
    fs.save(date, vid)
    path = fs.url(date)
    obj=Lecture_video()
    obj.videos=path
    obj.title=title
    obj.date=date1
    obj.SELECTED_SUBJECT_id=id
    obj.save()
    return HttpResponse('''<script>alert("Added");window.location='/myapp/Teacher_Selected_subject/#abc'</script>''')

def Add_notes(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Selected_Subject.objects.get(SUBJECT_id=id)


    return render(request,'Teacher/Add Notes.html',{'data':res,'id':id})
def add_note_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    did=request.POST['id1']
    title=request.POST['textfield']
    note=request.FILES['fileField']
    id = request.POST['id']

    from datetime import datetime
    date1 = datetime.now()

    date = datetime.now().strftime('Y%m%d-%H%M%S') + ".pdf"
    fs = FileSystemStorage()
    fs.save(date, note)
    path = fs.url(date)
    obj=Notes()
    obj.title=title
    obj.note=path
    obj.date=date1
    obj.SELECTED_SUBJECT_id=id
    obj.save()

    return HttpResponse('''<script>alert("Added");window.location='/myapp/Teacher_Selected_subject/#abc'</script>''')
def Add_Queustion_bank(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Selected_Subject.objects.get(SUBJECT_id=id)

    return render(request,'Teacher/Add Question Bank.html',{'data':res,'id':id})
def add_question_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    did = request.POST['id1']
    id = request.POST['id']
    title = request.POST['textfield']
    note = request.FILES['fileField']
    from datetime import datetime
    date1 = datetime.now()

    date = datetime.now().strftime('Y%m%d-%H%M%S') + ".pdf"
    fs = FileSystemStorage()
    fs.save(date, note)
    path = fs.url(date)
    obj = QuestionBank()
    obj.title = title
    obj.questions = path
    obj.date = date1
    obj.SELECTED_SUBJECT_id = id
    obj.save()
    return HttpResponse('''<script>alert("Added");window.location='/myapp/Teacher_Selected_subject/#abc'</script>''')

def Teacher_Change_password(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    return render(request,'Teacher/change password.html')
def t_changepassword_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']

    log = Login.objects.filter(id=request.session['lid'], password=currentpassword)
    if log.exists():
        if newpassword == confirmpassword:
            log1 = Login.objects.filter(id=request.session['lid'], password=currentpassword).update(
                password=newpassword)

            return HttpResponse('''<script>alert('password change success');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert('password not change ');window.location='/myapp/Teacher_Change_password/#abc'</script>''')
    else:
        return HttpResponse(
            '''<script>alert('password not change ');window.location='/myapp/Teacher_Change_password/#abc'</script>''')


def Teacher_Register(request):


    return render(request,'Teacher/Register.html')
def T_register_post(request):


    name = request.POST['name']
    gender = request.POST['RadioGroup1']
    dob = request.POST['dob']
    photo = request.FILES['fileField']

    hname = request.POST['hname']
    place = request.POST['place']
    city = request.POST['city']
    email = request.POST['email']
    mobile = request.POST['phone']
    pswd=request.POST['pswd']


    lobj = Login()
    lobj.username =email
    lobj.password = pswd
    lobj.type = 'pending'
    lobj.save()

    stdnt = Teacher()
    stdnt.tname = name
    stdnt.phone = mobile
    stdnt.email = email

    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, photo)
    path = fs.url(date)
    stdnt.photo = path

    stdnt.gender = gender
    stdnt.dob = dob
    stdnt.hname = hname
    stdnt.place = place
    stdnt.city = city
    stdnt.status='pending'
    stdnt.LOGIN = lobj
    stdnt.save()
    return HttpResponse('''<script>alert(' Registered');window.location='/myapp/login/'</script>''')


def Send_Solution(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Doubts.objects.get(id=id)
    return render(request,'Teacher/send_Solution.html',{'data':res})
def T_send_solution_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    sol=request.POST['reply']
    did=request.POST['id']
    obj=Doubts.objects.get(id=did)
    obj.Solution=sol
    obj.Status='replied'
    obj.save()
    return HttpResponse('''<script>alert(' Replied');window.location='/myapp/Teacher__view_doubts/#abc'</script>''')
def Teacher_home(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    return render(request,'Teacher/Teacher Home.html')
def Teacher_View_course(request,did):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Course.objects.filter(DEPARTMENT_id=did)

    return render(request,'Teacher/View Course.html',{'data':res})
def T_view_course_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']

    res = Course.objects.filter(coursename__icontains=srch)
    return render(request,'Teacher/View Course.html',{'data':res})
def Teacher_View_department(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Department.objects.all()

    return render(request,'Teacher/View department.html',{'data':res})
def T_view_department_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']

    res = Department.objects.filter(departmentname__icontains=srch)
    return render(request,'Teacher/View department.html',{'data':res})

def Teacher_view_Lecture_video(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Lecture_video.objects.filter(SELECTED_SUBJECT__SUBJECT_id=id,SELECTED_SUBJECT__TEACHER__LOGIN_id=request.session['lid'])

    return render(request,'Teacher/View Lecturevideo.html',{'data':res,'id':id})
def delete_videos(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Lecture_video.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert(' Deleted');window.location='/myapp/Teacher_Selected_subject/#abc'</script>''')

def T_view_lvideo_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    f = request.POST["f"]
    t = request.POST["t"]
    id = request.POST["sid"]

    var = Lecture_video.objects.filter(date__range=[f, t],SELECTED_SUBJECT__SUBJECT_id=id,SELECTED_SUBJECT__TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/View Lecturevideo.html',{'data':var})

def Teacher_View_Notes(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Notes.objects.filter(SELECTED_SUBJECT__SUBJECT_id=id,SELECTED_SUBJECT__TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/View Notes.html',{'data':res,'id':id})
def T_view_notes_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    f = request.POST["f"]
    t = request.POST["t"]
    id = request.POST["sid"]

    var = Notes.objects.filter(date__range=[f, t],SELECTED_SUBJECT__SUBJECT_id=id,SELECTED_SUBJECT__TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/View Notes.html',{'data':var})

def delete_notes(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Notes.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert(' Deleted');window.location='/myapp/Teacher_Selected_subject/#abc'</script>''')
def Teacher_View_qstn_bank(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=QuestionBank.objects.filter(SELECTED_SUBJECT__SUBJECT_id=id,SELECTED_SUBJECT__TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/View Question Bank.html',{'data':res,'id':id})
def delete_qustn(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=QuestionBank.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert(' Deleted');window.location='/myapp/Teacher_Selected_subject/#abc'</script>''')
def T_view_qstn_bank_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')
    id = request.POST["sid"]

    f = request.POST["f"]
    t = request.POST["t"]
    var = QuestionBank.objects.filter(date__range=[f, t],SELECTED_SUBJECT__SUBJECT_id=id,SELECTED_SUBJECT__TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/View Question Bank.html',{'data':var})

def Teacher_Selected_subject(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Selected_Subject.objects.filter(TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/View Selected Subject.html',{'data':res})
def T_selected_subject_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']
    res = Selected_Subject.objects.filter(SUBJECT__Subname__icontains=srch,TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/View Selected Subject.html',{'data':res})

def T_View_subject_list(request,did):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Subject.objects.filter(COURSE_id=did)
    return render(request,'Teacher/View SubjectList.html',{'data':res})
def select_sub(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    obj=Selected_Subject()
    obj.SUBJECT=Subject.objects.get(id=id)
    obj.TEACHER=Teacher.objects.get(LOGIN_id=request.session['lid'])
    obj.save()

    return HttpResponse('''<script>alert('Selected');window.location='/myapp/Teacher_home/#abc'</script>''')
def T_View_subject_lis_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch=request.POST['textfield']
    res=Subject.objects.filter(Subname__icontains=srch)
    return render(request,'Teacher/View SubjectList.html',{'data':res})

def Teacher__view_doubts(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Doubts.objects.filter(TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/view_Doubts.html',{'data':res})
def TView_doubts_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    f = request.POST["f"]
    t = request.POST["t"]
    var = Doubts.objects.filter(date__range=[f, t],TEACHER__LOGIN_id=request.session['lid'])
    return render(request,'Teacher/view_Doubts.html',{'data':var})


def Teacher_view_profile(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Teacher.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Teacher/view_profile.html',{'data':res})

##########################################Student#################################











def Schange_password(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    return render(request,'Student/change password.html')
def Schange_password_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']

    log = Login.objects.filter(id=request.session['lid'], password=currentpassword)
    if log.exists():
        if newpassword == confirmpassword:
            log1 = Login.objects.filter(id=request.session['lid'], password=currentpassword).update(
                password=newpassword)

            return HttpResponse('''<script>alert('password change success');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert('password not change ');window.location='/myapp/Schange_password/#abc'</script>''')
    else:
        return HttpResponse(
            '''<script>alert('password not change ');window.location='/myapp/Schange_password/#abc'</script>''')


def S_download_syllaabus(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    crs = Syllabus.objects.all()

    return render(request,'Student/Download syllabus.html',{'data':crs})
def S_downloadsyllabus_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']
    res = Syllabus.objects.filter(SUBJECT__Subname__icontains=srch)
    return render(request,'Student/Download syllabus.html',{'data':res})
def S_register(request):
    crs = Course.objects.all()

    return render(request,'Student/Register.html',{'data':crs})
def S_register_post(request):
    name = request.POST['name']
    gender = request.POST['RadioGroup1']
    dob = request.POST['dob']
    photo = request.FILES['fileField']

    hname = request.POST['hname']
    place = request.POST['place']
    city = request.POST['city']
    email = request.POST['email']
    mobile = request.POST['phone']
    sem=request.POST['sem']
    course=request.POST['cname']
    pswd=request.POST['pswd']


    lobj = Login()
    lobj.username = email
    lobj.password = pswd
    lobj.type = 'student'
    lobj.save()

    stdnt = Student()
    stdnt.sname = name
    stdnt.phone = mobile
    stdnt.email = email
    stdnt.COURSE_id=course
    stdnt.sem=sem


    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, photo)
    path = fs.url(date)
    stdnt.photo = path

    stdnt.gender = gender
    stdnt.dob = dob
    stdnt.hname = hname
    stdnt.place = place
    stdnt.city = city
    stdnt.status = 'pending'
    stdnt.LOGIN = lobj
    stdnt.save()
    return HttpResponse('''<script>alert('Registered');window.location='/myapp/login/'</script>''')


def S_send_doubts(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    # res=Selected_Subject.objects.get(TEACHER_id=id)
    return render(request,'Student/send_doubts.html',{'id':id})
def S_send_doubts_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    doubt=request.POST['reply']
    did=request.POST['tid']
    date=datetime.datetime.now()
    obj=Doubts()
    obj.doubt=doubt
    obj.date=date
    obj.Status='pending'
    obj.STUDENT=Student.objects.get(LOGIN=request.session['lid'])
    obj.TEACHER_id=did
    obj.save()
    return HttpResponse('''<script>alert('Added');window.location='/myapp/S_view_teacher/#abc'</script>''')
def S_student_home(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    return render(request,'Student/StudentHome.html')
def S_view_course(request,did):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Course.objects.filter(DEPARTMENT_id=did)

    return render(request,'Student/View Course.html',{'data':res})
def S_View_course_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']

    res = Course.objects.filter(coursename__icontains=srch)
    return render(request,'Student/View Course.html',{'data':res})

def S_View_department(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Department.objects.all()

    return render(request,'Student/View department.html',{'data':res})
def S_Viewdepartment_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']

    res = Department.objects.filter(departmentname__icontains=srch)
    return render(request,'Student/View department.html',{'data':res})

def S_view_lec_video(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Lecture_video.objects.filter(SELECTED_SUBJECT__SUBJECT_id=id)
    return render(request,'Student/View LecVideos.html',{'data':res,'id':id})
def S_View_lecvidoe_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')
    id=request.POST['sid']
    f = request.POST["f"]
    t = request.POST["t"]
    var = Lecture_video.objects.filter(date__range=[f, t],SELECTED_SUBJECT__SUBJECT_id=id)
    return render(request,'Student/View LecVideos.html',{'data':var})
def S_view_notes(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Notes.objects.filter(SELECTED_SUBJECT__SUBJECT_id=id)

    return render(request,'Student/view Notes.html',{'data':res,'id':id})
def S_View_notes_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')
    id=request.POST['sid']

    f = request.POST["f"]
    t = request.POST["t"]
    var = Notes.objects.filter(date__range=[f, t],SELECTED_SUBJECT__SUBJECT_id=id)
    return render(request,'Student/view Notes.html',{'data':var})

def S_view_question_bank(request,id):
    res=QuestionBank.objects.filter(SELECTED_SUBJECT__SUBJECT_id=id)

    return render(request,'Student/View Question Bank.html',{'data':res,'id':id})
def s_View_qustnbank__post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')
    id=request.POST['sid']

    f = request.POST["f"]
    t = request.POST["t"]
    var = QuestionBank.objects.filter(date__range=[f, t],SELECTED_SUBJECT__SUBJECT_id=id)
    return render(request,'Student/View Question Bank.html',{'data':var})
def S_view_subject(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    s=Student.objects.get(LOGIN_id=request.session['lid'])
    res=Subject.objects.filter(COURSE=s.COURSE,semester=s.sem)

    return render(request,'Student/View Subject.html',{'data':res})
def S_View_subject_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']
    res = Subject.objects.filter(Subname__icontains=srch)
    return render(request,'Student/View Subject.html',{'data':res})

def S_view_teacher(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Selected_Subject.objects.filter(TEACHER__status='approved')

    return render(request,'Student/View Teacher.html',{'data':res})
def S_ViewTeachers_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    srch = request.POST['textfield']
    res = Selected_Subject.objects.filter(SUBJECT__Subname__icontains=srch)
    return render(request,'Student/View Teacher.html',{'data':res})

def S_view_profile(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Student.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Student/view_profile.html',{'data':res})
def S_view_Solutions(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    res=Doubts.objects.filter(STUDENT__LOGIN_id=request.session['lid'])
    return render(request,'Student/view_Solutions.html',{'data':res})
def View_solutions_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("You are Logout...");window.location='/myapp/login/'</script>''')

    f = request.POST["f"]
    t = request.POST["t"]
    var = Doubts.objects.filter(date__range=[f, t],STUDENT__LOGIN_id=request.session['lid'])
    return render(request,'Student/view_Solutions.html',{'data':var})
