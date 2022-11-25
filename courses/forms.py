from django import forms

class DateTimeInput(forms.DateTimeInput):
    """Form for the deadline of the new assignment \n
    
    :param input_type: This takes in date in dd-mm-yyyy format and time in 12 hr format

    """
    input_type = 'datetime-local'

class CourseCreationForm(forms.Form):
    """Form for creating a course (by the instructor). \n
    Both the parameters are unique to a particular course.
    
    :param name: name of the course
    :param code: code for joining the course

    """
    name = forms.CharField(
        label='Course name',
        max_length=100,
        widget = forms.TextInput(attrs = {'class' : 'textareaform'})
    )
    code = forms.CharField(
        label='Join code',
        max_length=100,
        widget = forms.TextInput(attrs = {'class' : 'textareaform'})
    )

class CourseJoinForm(forms.Form):
    """Form for the student to join in a course via join code. \n
    The parameter is the code given by the instructor to a particular course.
    
    :param code: code which is giving by the instructor to join the course

    """
    code = forms.CharField(label='Enter Course Code', max_length=10)


EXTEN = (
    (1, '.zip'),
    (2, '.cpp'),
    (3, '.tar.gz'),
    (4, '.py'),
    (5, '.tgz'),
)
class AssignCreationForm(forms.Form):
    """Form asking the instructor for some details like deadline,total marks and the assignment's weightage in the course and so on \n
    
    :param name: Name of the Assignment
    :param file: File related to assignment 
    :type file: optional
    :param weblink: Website link related to assignment
    :type weblink: optional
    :param statement: Problem statement for the assignment
    :param marks: Maximum marks for assignment
    :param weightage: Contribution of this assignment to the course
    :param extensions: Valid extension of the submissions
    :param deadline: Time till which the submissions are accepted

    """
    name = forms.CharField(label='Assignment name', max_length=50,required=True)
    file = forms.FileField(label='Problem File',required=False)
    weblink = forms.URLField(label='URL link',required=False)
    statement = forms.CharField(
            widget= forms.Textarea(
                attrs={'style': 'border-color: orange;' 'width: 80%' 'height: 250px' 'padding: 12px 20px;' 'border: 2px solid #ccc;' 'border-radius: 15px;''background-color: #f8f8f8;' }
            ),
            label='Description',
            required=True,
            max_length=300
    )
    marks = forms.IntegerField(label='Max Marks',required=True)
    weightage = forms.IntegerField(label='Weightage',required=True)
    extensions = forms.ChoiceField(
            choices = EXTEN,
            label='Extensions',
            required=True,
    )
    text_file = forms.FileField(label='Text File',required=False,help_text='*Upload a .txt file generated after running "tree" command on the directory')
    deadline = forms.DateTimeField( #using the calender-time selection field of HTML.
            widget= DateTimeInput(),
            label='Deadline',
            required=True
    )


class AssignmentSubmitForm(forms.Form):
    """Form for collecting the submitted assignments by the students \n

    :param file: File you need to submit

    """
    file = forms.FileField(label='Submission File',required=True)

class FeedbackForm(forms.Form):
    """Instructor gives his feedback after correcting the assignment submitted by the student \n

    :param feedback: Feed back to the submission
    :param grade: Marks for the submission

    """
    feedback = forms.CharField(
        widget= forms.Textarea(
            attrs={'style': 'border-color: orange;' 'width: 80%;' 'height: 400px' 'padding: 12px 20px;' 'border: 2px solid #ccc;' 'border-radius: 15px;''background-color: #f8f8f8;' }
        ),
        label='Feedback',
        required=True,
        max_length=300
    )
    grade = forms.IntegerField(label='Grade',required=True)

class UserAddForm(forms.Form):
    """Instructor can add the students using this form \n

    :param Username: Username of the student 

    """
    username = forms.CharField(
        widget = forms.TextInput(
            attrs= {'style': 'border-color: orange;' 'width: 50%;' 'height: 20%' 'padding: 10px 20px;' 'border: 2px solid #ccc;' 'border-radius: 15px;''background-color: #81b0e0;' }
        ),
        label = 'username',
        required=True,
        max_length=50
    )