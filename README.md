# Search Syllabus

## Deliverables

* Deployed application without errors
* Documented scripts in clean style
* A readme that lays out how the code is organized
* A config file that has details of the database etc.

## Search a database of information about each lecture, lab, and seminar taught in a given year of our program

[https://xxxx.pharmacy.ualberta.ca](http://xxxx.pharmacy.ualberta.ca) search syllabus information for content in the curriculum

select the academic year you want to search within

select which type of data you want to search - course, session (lectures, labs, and seminars), or assessments

enter keywords using "and" "or" operators to reveal courses or sessions in the fall, winter, and spring/summer sessions that contain the information you are looking for

download a csv or print off search results

## Main Parts

1. [update_dbs.py](scrips/update_dbs.py) will take three CSVs with the following fields and update the database.

Course CSV:

	Short Name: course short name
	Full Name: course full name
	Term: Fall, Winter, Spring, or Summer
	Faculty: faculty where course is listed
	Course Types: comma separated tags for courses (e.g. program the course is in, year of program, category of content)
	Credits: number of course credits
	Instructors: comma separated list of instructor names
	TAs: comma separated list of course TAs
	Assessment: number of graded assessments
	Session count: number of sessions (lectures, labs, seminars)
	Course outcomes: all: multiple columns for each course outcome listed for a course

Session CSV:

	Short Name: course short name
	Full Name: course full name
	Faculty: faculty where course is listed
	Course Types: comma separated tags for courses (e.g. program the course is in, year of program, category of content)
	Instructors: comma separated list of instructor names
	TAs: comma separated list of course TAs
	Session title: title of lecture lab or seminar
	Section: label for lecture, lab or seminar section e.g. A1, B2
	Location: room location
	Guest teacher: names of guest lecturers
	Type: Lec, Lab, Seminar
	Length: session length
	Date: date session occurs
	Teaching strategies: comma separated list of teaching strategies employed
	Instruction type: face-to-face or distance
	Specific objectives: comma separated list of session learning outcomes
	Course outcomes: all: multiple columns for each course outcome listed for a course
	
Assessment CSV:

	Short Name: course short name
	Full Name: course full name
	Faculty: faculty where course is listed
	Course Types: comma separated tags for courses (e.g. program the course is in, year of program, category of content)
	Instructors: comma separated list of instructor names
	TAs: comma separated list of course TAs
	Assessment title: title of lecture lab or seminar
	Assessment type: label for type of assessment
	Section: label for lecture, lab or seminar section e.g. A1, B2
	Format: exam format
	weight: assessment weight
	due date: date assessment is due or happens
	Specific objectives: comma separated list of session learning outcomes
	Course outcomes: all: multiple columns for each course outcome listed for a course

2. Search interface with results on the same page

