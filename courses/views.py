from django.shortcuts import render, redirect
from moodle.models import User
import os, sys, filecmp, subprocess, pathlib, tarfile
from subprocess import call
from io import BytesIO
import base64
from .forms import AssignCreationForm, AssignmentSubmitForm, CourseCreationForm , CourseJoinForm, FeedbackForm, UserAddForm
from .models import Assignment, Course, FileSubmission
from django.utils import timezone

def create(request):
    """ This function is called when the instructor clicks the course create button \n
    This creates a new course with the fields filled in the course creation form. If the 
    filled form is invalid this function returns back to the course create html with form.
    This returns to the home page where we can see all the courses which are taken by user.

    :return: This returns url of coursehomepage  
    :rtype: link

    """
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            course_name = form.cleaned_data['name']
            code = form.cleaned_data['code']

            n = Course.objects.all().filter(joincode = code).count()
            e = Course.objects.all().filter(name = course_name).count()
            if( e != 0 or n != 0): #Name already exists.
                args = {'form': form, 'wrong': True}
                return render(request, 'courses/create.html', args)

            c = Course.objects.create(instructor = request.user)
            c.name = course_name
            c.joincode = code
            c.save()

            return redirect('coursehomepage')

    else:
        form = CourseCreationForm()
    return render(request, 'courses/create.html', {'form': form, 'wrong': False})

def coursesinfo(request):
    """ This function is called when the coursehomepage is called. \n
    This displays all the courses which are taken by the user.This displays the
    pending assignments of the students in their homepage.

    :return: This returns url of homepage
    :rtype: link

    """
    if not request.user.is_authenticated:
        return redirect('login')

    u = User.objects.get(pk = request.user.pk )

    Itodo_List = []
    Stodo_List = []

    PercI_List = []
    PercS_List = []

    now = timezone.now()
    for course in u.ins_courses.all():
        graded_count = 0
        assign_count = 0
        for assign in course.assignment_set.all():
            if now > assign.deadline:
                graded=True
                for sub in assign.filesubmission_set.all():
                    if sub.corrected == 'NO':
                        graded = False
                        break
                if not graded:
                    Itodo_List.append(assign)
                else:
                    graded_count += 1
            assign_count += 1
        if assign_count == 0:
            PercI_List.append(100)
        else:
            PercI_List.append(int((graded_count*100)/assign_count))

    for course in u.stud_courses.all():
        assign_count = 0
        sub_count = 0
        for assign in course.assignment_set.all():
            if now < assign.deadline:
                submitted=False
                for sub in assign.filesubmission_set.all():
                    if sub.user.username == request.user.username:
                        submitted = True
                        break
                if not submitted:
                    Stodo_List.append(assign)
                else:
                    sub_count += 1
            else:
                submitted=False
                for sub in assign.filesubmission_set.all():
                    if sub.user.username == request.user.username:
                        submitted = True
                        break
                if submitted:
                    sub_count += 1
            assign_count += 1
        if assign_count == 0:
            PercS_List.append(100)
        else:
            PercS_List.append(int((sub_count*100)/assign_count))

    for i in range(len(PercS_List)):
        PercS_List[i] = str(PercS_List[i]) + '%'

    for i in range(len(PercI_List)):
        PercI_List[i] = str(PercI_List[i]) + '%'

    args = {
        'scourses': u.stud_courses.all(),
        'icourses': u.ins_courses.all(),
        'Itodo': Itodo_List,
        'Stodo': Stodo_List,
        'Perc_S': PercS_List,
        'Perc_I': PercI_List,
    }
    if request.user.role == 2:
        return render(request,'registration/instructor_home.html',args)
    else:
        return render(request,'registration/student_home.html',args)

def course(request,course_id):
    """ This function is called when the user whats to go to a particular course homepage. \n
    It takes in the course id of that particular course and returns the url to the
    homepage of that particular course.
    
    :param course_id: a number unique to a course 
    :type course_id: int
    :return: This returns url of coursehomepage 
    :rtype: link

    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    c = Course.objects.get(pk = course_id)

    Snames = [ s.username for s in c.students.all() ]

    uname = request.user.username
    if uname not in (Snames) and uname != c.instructor.username:
        return redirect('homepage')

    args = {
        'Instructor': c.instructor,
        'Students': c.students.all(),
        'course': c,
        'assignments': c.assignment_set.all(),
        'nowtime': timezone.now(),
    }
    return render(request,'courses/coursepage.html',args)

def join(request):
    """ This function is called when the student hits the join course button. \n
    This will return to an html page which contains a form to join the course.
    If the form is not valid then this returns again to the same page. Or else 
    it returns to the homepage of the user. Now the home page conatains the course which you added.
    
    :return: This returns url of coursehomepage 
    :rtype: link

    """
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CourseJoinForm(request.POST)
        if form.is_valid():

            code = form.cleaned_data['code']
            e = Course.objects.all().filter(joincode = code).count()

            if( e == 0 ):
                args = {'form': form, 'wrong': True}
                return render(request, 'courses/join.html', args)
            
            else:
                c = Course.objects.get(joincode = code)
                c.students.add(request.user)
                c.save()          

            return redirect('coursehomepage')

    else:
        form = CourseJoinForm()

    return render(request, 'courses/join.html', {'form': form ,'wrong': False })

def assign_create(request,course_id):
    """ This function is called when the instructor clicks the create assignment button. \n
    This will return to an html page which contains a form to create an assignment.
    If the form is not valid then this returns again to the same page. Or else 
    it returns to the coursehomepage of the course. Now the course home page conatains the new assignment.

    :param course_id: a number unique to a course 
    :type course_id: int
    :return: This returns url of coursehomepage 
    :rtype: link

    """
    if not request.user.is_authenticated:
        return redirect('login')
        
    c = Course.objects.get(pk = course_id)
    if c.instructor.username != request.user.username:
        return redirect('homepage')  

    if request.method == 'POST':
        form  = AssignCreationForm(request.POST,request.FILES)
        if form.is_valid():
            assign_name = form.cleaned_data['name']
            ref = form.cleaned_data['weblink']
            msg = form.cleaned_data['statement']
            dedline = form.cleaned_data['deadline']
            weight = form.cleaned_data['weightage']
            a_file = request.FILES.get('file',False)

            a = Assignment.objects.create(name = assign_name,course = c,deadline = dedline,weightage = weight)
            a.statement = msg
            a.link = ref
            a.maxmarks = form.cleaned_data['marks']
            a.extensions = form.cleaned_data['extensions']
            a.text_file = form.cleaned_data['text_file']

            if a_file:
                a.file  = a_file
                a.file_name = a.file.name.split("/")[-1]
            a.save()

            return redirect('coursepage',course_id = c.pk)
    else:
        form = AssignCreationForm()

    args = {
        'Instructor': c.instructor,
        'Students': c.students.all(),
        'course': c,
        'form': form,
        'assignments': c.assignment_set.all()
    }
    return render(request,'courses/assign_create.html',args)

def assign(request,course_id,assign_id):
    """ This function is called when the user wants to go to a particular assignment homepage. \n
    It takes in two parameter namely course id and assign_id of that particular assignment and 
    returns the url to the homepage of that particular assignment. This also returns some arguments
    which can be used in the redirected html.

    :param course_id: a number unique to a course 
    :type course_id: int
    :param assign_id: a number unique to a course 
    :type assign_id: int
    :return: This returns url of coursehomepage 
    :rtype: link

    """
    a = Assignment.objects.get(pk = assign_id)
    c = Course.objects.get(pk = course_id )

    if not request.user.is_authenticated:
        return redirect('login')

    Snames = [ s.username for s in c.students.all() ]
    uname = request.user.username
    if uname not in (Snames ) and uname != c.instructor.username:
        return redirect('homepage')

    if request.method == "POST":
        form = AssignmentSubmitForm(request.POST,request.FILES)
        if form.is_valid():
            s_file = request.FILES.get('file',False)

            file_ext = pathlib.Path(s_file.name).suffix
            if a.extensions == 1:
                if file_ext != ".zip":
                    return redirect('assign_page',course_id = c.pk,assign_id = a.pk)
            elif a.extensions == 2:
                if file_ext != ".cpp":
                    return redirect('assign_page',course_id = c.pk,assign_id = a.pk)
            elif a.extensions == 3:
                if file_ext != ".gz":
                    return redirect('assign_page',course_id = c.pk,assign_id = a.pk)
            elif a.extensions == 4:
                if file_ext != ".py":
                    return redirect('assign_page',course_id = c.pk,assign_id = a.pk)
            else:
                if file_ext != ".tgz":
                    return redirect('assign_page',course_id = c.pk,assign_id = a.pk)               

            if FileSubmission.objects.filter(user = request.user,assignment = a).exists():#resubmission.
                s = FileSubmission.objects.get(user = request.user,assignment = a)
                s.corrected = 'NO'
                s.grade = -1
            else:
                s = FileSubmission.objects.create(user = request.user, assignment = a)
            if s_file:
                s.file = s_file
                s.file_name = s.file.name.split("/")[-1]
            s.save()
            
            if a.text_file.name != "" :
                jeep = a.text_file.name.split("/")
                temp = jeep[1]
                if file_ext == ".zip" or file_ext == ".gz" or file_ext == ".tgz":
                    folder_name = s_file.name
                    #print(folder_name)
                    os.chdir("media/submissions")
                    os.system("pwd")
                    if file_ext == ".zip":
                        call(["unzip", folder_name])
                    elif file_ext == ".gz" or file_ext == ".tgz":
                        file1 = tarfile.open(folder_name)
                        file1.extractall('./')
                        file1.close()

                    #os.chdir("submissions/")
                    dir_name = folder_name.split(".")
                    direct = dir_name[0]
                    os.chdir(direct)
                    out = subprocess.run(["tree"],capture_output=True,text=True, check=True)
                    os.chdir("../")
                    with open("output1.txt","w") as sys.stdout:
                        print(out.stdout)
                    subprocess.run(["rm", "-r", direct])
                    os.chdir("../")
                    if filecmp.cmp(a.text_file.name,"submissions/output1.txt") == False:
                        s.delete()
                    os.chdir("../")
                     
        return redirect('assign_page',course_id = c.pk,assign_id = a.pk)
    else:
        form = AssignmentSubmitForm()

    subms = list(a.filesubmission_set.all())
    temp = ""
    submitted = False
    for sub in subms:
        if request.user.username == sub.user.username:
            submitted = True
            break
    if submitted:
        mysubmission = FileSubmission.objects.get(user = request.user,assignment = a)
    else:
        mysubmission = {'feedback': 'You Did Not Submit'}

    instruct = True
    if c.instructor.username != request.user.username:
        instruct = False

    deadline = a.deadline

    args = {
        'form': form,
        'assign': a,
        'course': c,
        'submissions': list(a.filesubmission_set.all()),
        'submitted': submitted,
        'mysub': mysubmission,
        'instruct': instruct,
        'deadline': deadline,
        'nowtime': timezone.now(),
        'students': c.students.all(),
        'tree_name': temp
    }
    return render(request,'courses/assign_page.html',args)


def submissions(request,course_id,assign_id):
    """ This function is called when the instructor wants see all submissions of an assignment. \n
    It takes in two parameter namely course id and assign_id of that particular assignment and 
    returns the url to the submissions of that particular assignment. This also returns some arguments
    which can be used in the redirected html.

    :param course_id: a number unique to a course 
    :type course_id: int
    :param assign_id: a number unique to an assignment 
    :type assign_id: int
    :return: This returns url of submissions page 
    :rtype: link

    """
    a = Assignment.objects.get(pk = assign_id)
    c = Course.objects.get(pk = course_id )

    if not request.user.is_authenticated:
        return redirect('login')

    uname = request.user.username
    
    Snames = [ s.username for s in c.students.all() ]
    uname = request.user.username
    if uname != c.instructor.username:
        return redirect('homepage')

    if request.method == 'POST':
        form = AssignmentSubmitForm(request.POST,request.FILES)
        if form.is_valid():
            s_file = request.FILES.get('file',False)
            if s_file:
                a.feedfile = s_file
                a.save()
                give_feedback(c,a)
                return redirect('submissions',course_id,assign_id)
    else:
        form = AssignmentSubmitForm()

    grading_done = True
    for sub in a.filesubmission_set.all():
        if sub.corrected == 'NO':
            grading_done = False
            break
             
    args = {
        'assign': a,
        'course': c,
        'submissions': list(a.filesubmission_set.all()),
        'form': form,
        'nowtime': timezone.now(),
        'GRADED': grading_done,
    }
    return render(request,'courses/submissions.html',args)

def feedback(request,course_id,assign_id,sub_id):
    """ This function is called when the instructor wants to submit the marks and give a feedback. \n
    It takes in three parameter namely course id, sub_id and assign_id of that particular submission
    of a student. This returns the url to feedback html which contains a form to be filled by the instructor.
    If this form fails then thid returns back to the feedback html.
    This also returns some arguments which can be used in the redirected html.

    :param course_id: a number unique to a course 
    :type course_id: int
    :param assign_id: a number unique to an assignment 
    :type assign_id: int
    :return: This returns url of feedback page 
    :rtype: link

    """
    a = Assignment.objects.get(pk = assign_id)
    c = Course.objects.get(pk = course_id )
    s = FileSubmission.objects.get(pk = sub_id)

    if not request.user.is_authenticated:
        return redirect('login')

    uname = request.user.username

    Snames = [ s.username for s in c.students.all() ]

    uname = request.user.username
    if uname != c.instructor.username:
        return redirect('homepage')


    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['feedback'])
            s.feedback = form.cleaned_data['feedback']
            s.corrected = 'YES'
            s.grade = form.cleaned_data['grade']
            s.save()

            return redirect('submissions',course_id,assign_id)
    else:
        if s.corrected == "YES":
            form = FeedbackForm({'feedback': s.feedback})
        else:
            form = FeedbackForm()

    args = {
        'assign': a,
        'course': c,
        'submissions': list(a.filesubmission_set.all()),
        'sub': s,
        'form': form
    }
    return render(request,'courses/feedback.html',args)

def give_feedback(course,assign):
    """ This function is called in submissions function. \n
    This is an helper function which takes in two parameters namely course and assign.
    of a student. This function modifies the status of the submission of the student.
    The submission is uniquely defined by the given course and assign.

    :param course: a number unique to a course 
    :type course: int
    :param assign: a number unique to an assignment 
    :type assign: int

    """
    subs = assign.filesubmission_set.all()

    raw = assign.feedfile.read()
    data = raw.decode("utf-8")
    lines = []
    s = ''
    for i in range(len(data)):
        char = data[i]
        if(ord(char) != 10 and ord(char) != 13):
            s += char
        else:
            if len(s) != 0:
                lines.append(s)
            s = ''
    if len(s) != 0:
        lines.append(s)

    for line in lines:
        L = line.split(',',2)
        print(L)
        for sub in subs:
            if L[0] == sub.user.username:
                marks = int(L[1])
                cap = assign.maxmarks
                marks = min(cap,marks)

                sub.corrected = 'YES'
                sub.grade = marks

                sub.feedback = L[2].replace("##","\n")

                sub.save()

def participants(request,course_id):
    """ This function is called when the user wants to see the participants of a course. \n
    This will redirect to participants html where all the participants can be seen. If the 
    user is an instructor for course with the given id then they can even add the
    participants and remove the participants from the course.

    :param course_id: a number unique to a course 
    :type course_id: int
    :return: This returns url of participants page 
    :rtype: link

    """
    c = Course.objects.get(pk = course_id)
    a = 'False'
    Snames = [ s.username for s in c.students.all() ]

    uname = request.user.username
    if uname not in (Snames ) and uname != c.instructor.username:
        return redirect('coursehomepage')

    IsINS = 'NO'
    if uname == c.instructor.username:
        IsINS = 'YES'

    if request.method == 'POST':
        form = UserAddForm(request.POST)

        if form.is_valid():
            uname = form.cleaned_data['username']

            if User.objects.all().filter(username = uname).count() == 0:
                a = 'True'
                args = {
                    'course':   c,
                    'Students': c.students.all(),
                    'Ins':  c.instructor,
                    'IsINS':    IsINS,
                    'form': form,
                    'a': a
                }
                return render(request,'courses/participants.html',args)

            U = User.objects.get(username = uname)
            if not U in c.students.all():
                c.students.add(U)

            return redirect('participants',course_id)
    else:
        form = UserAddForm()

    args = {
        'course':   c,
        'Students': c.students.all(),
        'Ins':  c.instructor,
        'IsINS':    IsINS,
        'form': form,
        'a': a
    }
    return render(request,'courses/participants.html',args)

def remove(request,course_id,user_id):
    """ This function is called when the instructor hits the remove button for a particular participant. \n
    This takes in two parameters namely course_id and user_id.This removes the student with the given user_id
    from the course with cgiven course_id.

    :param course_id: a number unique to a course 
    :type course_id: int
    :param user_id: a number unique to an user
    :type user_id: int
    :return: This returns url of participants page 
    :rtype: link

    """
    C = Course.objects.get(pk = course_id)

    if not request.user.is_authenticated:
        return redirect('login')

    uname = request.user.username
    if uname != C.instructor.username:
        return redirect('coursehomepage')  

    U = User.objects.get(pk = user_id)

    Stds = C.students.all()

    if U in Stds:
        C.students.remove(U)
    
    return redirect('participants',course_id)