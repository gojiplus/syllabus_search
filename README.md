# Search Syllabus

## Deliverables

* Deployed application without errors
* Documented scripts in clean style
* A readme that lays out how the code is organized
* A config file that has details of the database etc.

## Search a database of information about lectures, labs, seminars, and assessments nested in courses based on a user provided time frame
## produce results as interactive tables (sort and filter functionality for specified columns) 

[https://xxxx.pharmacy.ualberta.ca](http://xxxx.pharmacy.ualberta.ca) search syllabus information for content in the curriculum

select the starting year (drop down of options included in the database) and term (Fall, Winter, or Spring/Summer)

select ending year and term

enter keywords using "and" "or" operators 

reveal table of courses where the keywords or combination of keywords are present in any of the course, nested session fields, or nested assessment fields

	keywords should be highlighted where they occur in course fields
	
	Table of course results should have sort and filter functionality for "Course name", "Year", "Term", "Credits", "Faculty Tags", "Course Instructor(s)", and "Teaching Assistants" columns

	users can download a csv or pdf of final results
	
	after course filters are selected users can select to reveal the sessions and assessments that containing any of the keywords

reveal a table of sessions where the keywords or combination of keywords are present in any session fields

	keywords should be highlighted where they occur in session fields
	
	Table of session results should have sort and filter functionality for "Course name", "Type", "Date", "Length", "Course Instructor", "Lecturer", "Teaching Strategies", and "Delivery Mode" columns

	users can download a csv or pdf of final results

reveal a table of assessments where the keywords or combination of keywords are present in any assessment fields

	keywords should be highlighted where they occur in session fields
	
	Table of sessions results should have sort and filter functionality for "Course name", "Course Instructor", "Type", "Exam Format", "Weight", "Cumulative", "Teaching Strategies", and "Date" columns

	users can download a csv or pdf of final results	
	
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

