# cs251project
# Moodle
**210050095-210050140-210050152**

We created a website ("Moodle") which provides services to its users. Some of it's important features include: 


## Signup:
- Authentication is must for an user to login. When an user visits our website it gets directed to login page.
 If a user visits our website for the very first time and don't have an account then they must use the SignUp option. It redirects us to the **Signup** portal, where user can create an account.
- Here user should fill up some essential details to create an account.
The signup form fails if user don't fill all the required fields.
The signup form contains some required fields like username,password,email and role. Username is of user's interest within 150 characters and can contain letters, digits and @/./+/-/_ .Password for this username follows certain protocols like having atleast 8 characters, not entirely numeric etc for security reasons.
The role has 2 options student and instructor. The user must choose one of the roles based on which the permissions for their account are granted.
Once an account is created, user can use those credentials to login into their account

## Login:
Authentication is must for an user to login. The user should have already been signed up if he/she wants to login.
They must enter valid credentials i.e username and password.
Soon after the user enters the login credentials in the login page he gets redirected to the homepage.
Homepages of the instructors and the students are different.
Once the user is logged in he/she can see the **homepage**.

## Homepage:
After user logged in to the website user can see their dashboard.
On the right corner of the homepage there is a dropdown box which stays throughout our website containing the options profile, edit profile, change password, logout.
On the left corner there is a side navigation bar which stays throughout our website and it contains an option "Homepage",
clicking on which user gets redirected to the homepage ,on whichever page they are in.
- User get the options of **Editing** their profile and changing their password on clicking edit profile and change password respectively.
- We also have links to **Courses** page 

 The homepage mainly contains the courses the user is registered in if he/she is a student and courses they created if he/she is an instructor.

Homepage of Instructor:
contains an option "Create Course" to create course:
 -a link leading in the creation of a course by an instructor (the instructor have to enter a course name and a join code to create the course).
 course name - maxlength=100, it's unique.
 Join code - maxlength=100, it's unique and is required for students to join the course
 If you enter a course name or join code that's already registered, an error message appears "Course name or Join code already exists!"
-courses that are created by the instructor
################################################## 
	
Homepage of Student:
contains an option "Join Course" to join course:
-a link allowing the student to join in a course after the join code of the course is entered.
-Homepage contains the courses that user is registered in

Clicking on the courses that are visible on the homepage:
home page gets redirected to the course page

## Course page of instructor:
 - It contains all the assignments created by instructor in 2 categories **Deadline Up** and **Still running**. 
 The assignments whose deadline is up appears under 1st category else appears in 2nd category.
 At top appears join code of the course and an option "Create Asssignment". Clicking on create assignment redirects you to assignment creation form.
 Clicking on assignment names redirects instructor to **assignment page** 
 Clicking on participants redirects you to **participants page**
   ## Assignment Creation:
 -Clicking on **Create Assignment** redirects you to assignment creation form where you need to enter some details about it.
  Name and **description** of the assignment are required fields, and instructor can add any Problem **files** and/or a **url** reference to the assignment. We can set the **Maximum Marks** in the assignment and assign its **Weightage** in the course. Instructor have to set a **Deadline** to the assignment.
  - Instructor have to select a file extension of file which is needed to be submitted by students in the course for that assignment. The extension fields contains the following choices. 
   .zip, .cpp, .tar.gz, .py, .tgz. The instructor can chose only one valid extension. If he choses .zip or .tar.gz or .tgz as a valid extension he must upload a .txt file containing tree of the    directory that needs to be uploaded by student. Clicking on create button redirects you to course page.
  ## Assignment Page:
  Clicking on the assignment name in course page redirects you to the respective assignments'page. The instructor can see name,description,max_marks weightage and the problem file in this page.
  He/She can also see total number of students and number of submissions. There is a button at the bootom of this page clicking on which redirects us to submissions page.
     ##Submissions Page: The instructor can see name,description,max_marks, weightage and the grading status(i.e graded or not graded) in this page. The instructor can see a table of students

-

 
 
 can correct the submitted assignment
 
student can submit the assignment


