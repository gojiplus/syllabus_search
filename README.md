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

reveal table of courses that are in the specified range of time

	Table of course results should have sort and filter functionality for "Course name", "Year", "Term", "Credits", "Faculty Tags", "Course Instructor(s)", and "Teaching Assistants" columns
	
	offer option to enter keywords using "and" "or" operators as a basis to further filter courses
	
	where the keywords or combination of keywords are present in any of the course, nested session, or nested assessment fields

	keywords should be highlighted where they occur in course fields
	
	users can download a csv or pdf of final results
	
	after course filters are selected users can select to reveal the sessions and assessments that contain any of the keywords

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

	Short Name: course short name (unique course id common in all three files)
	Full Name: course full name (unique course id common in all three files)
	Year: numeric
	Term: Fall, Winter, Spring, or Summer
	Faculty: ignore
	Course Types: comma separated course tags (e.g. program the course is in (BScPharm, PharmD, PPPharmD), year of program (1st, 2nd, 3rd), category of course content (pharm sci, practice skills, etc.))
	Credits: number of course credits
	Instructors: comma separated list of instructor names (names can contain special characters for accents that produce errors, names should also be checked to find and replace similar repeats with standardized consistent results)
	TAs: comma separated list of course TAs
	Assessment: number of graded assessments
	Session count: number of sessions (lectures, labs, seminars)
	Course outcomes: all: multiple columns for each instructor written course outcome attached to a course (output could produce separate rows for each outcome if getting results in one column is difficult) 

Session CSV:

	Short Name: course short name (unique course id common in all three files)
	Full Name: course full name (unique course id common in all three files)
	Faculty: ignore
	Category: same as data in course file - comma separated course tags (e.g. program the course is in (BScPharm, PharmD, PPPharmD), year of program (1st, 2nd, 3rd), category of course content (pharm sci, practice skills, etc.))
	Instructors: same as data in course file - repeated for each session with a common Short or Full name - comma separated list of instructor names (names can contain special characters for accents, etc that produce errors, names should also be checked to find and replace similar repeats with standardized consistent results)
	TAs: same as data in course file - repeated for each session with a common Short or Full name - comma separated list of course TAs
	Session title: title of lecture lab or seminar
	Section: ignore
	Location: room location
	Guest teacher: name(s) of guest lecturers (names can contain special characters for accents, etc that produce errors, names should also be checked to find and replace similar repeats with standardized consistent results)
	Type: session type Lec (lecture), Lab, Seminar
	Length: session length in mins
	Date: date session occurs (this data is very error prone - the dates will always be in the right sequence but the actual dates are not reliable. use the Year and Term fields as the initial basis to sort results, then sort by this Date field).
	Teaching strategies: comma separated list of teaching strategies employed
	Instruction type: face-to-face or distance
	topics: comma separated list of topics covered in the session
	Specific objectives: comma separated list of session learning outcomes
	Course outcomes: all: multiple columns for each course outcome attached to this sessions
	
Assessment CSV:

	Short Name: course short name (unique course id common in all three files)
	Full Name: course full name (unique course id common in all three files)
	Faculty: ignore
	Category: same as data in course file - repeated for each assessment with a common Short or Full name - comma separated course tags (e.g. program the course is in (BScPharm, PharmD, PPPharmD), year of program (1st, 2nd, 3rd), category of course content (pharm sci, practice skills, etc.))
	Instructors: same as data in course file - repeated for each assessment with a common Short or Full name - comma separated list of instructor names (names can contain special characters for accents, etc that produce errors, names should also be checked to find and replace similar repeats with standardized consistent results)
	TAs: same as data in course file - repeated for each session with a common Short or Full name - comma separated list of course TAs
	Assessment title: title of assessment
	Assessment type: label for type of assessment (exam, assignment, quiz)
	Section: label for lecture, lab or seminar section e.g. A1, B2
	Format: exam format choice (multiple choice, written response, etc.)
	weight: assessment weight in percent
	cumulative: y/n variable indicating if exam is cumulative
	due date: date assessment is due or happens (data also unreliable - see description under session for this field)
	Specific objectives: comma separated list of session learning outcomes assessed
	Course outcomes: all: multiple columns for each course outcome attached to this session

2. Search interface with results on the same page

