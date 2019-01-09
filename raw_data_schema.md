## Raw Data Schema and Details

* [course level dataset](data/courses.csv): metadata on each course

	* Short Name: course short name (unique course id common in all three files) 
	* Full Name: course full name (unique course id common in all three files) --- **Primary Key**
	* Year: numeric
	* Term: Fall, Winter, Spring, or Summer
	* Faculty: ignore
	* Course Types: comma separated course tags (e.g. program the course is in (BScPharm, PharmD, PPPharmD), year of program (1st, 2nd, 3rd), category of course content (pharm sci, practice skills, etc.))
	* Credits: number of course credits
	* Instructors: comma separated list of instructor names (names can contain special characters for accents that produce errors)
	* TAs: comma separated list of course Teaching Assistants
	* Assessment: number of graded assessments
	* Session count: number of sessions (lectures, labs, seminars)
	* Course outcomes: all: multiple columns for each instructor written course outcome attached to a course (output could produce separate rows for each outcome if getting results in one column is difficult) 

* [session level dataset](data/sessions.csv): metadata on all the sessions in each course
	* Short Name: course short name (unique course id common in all three files) 
	* Full Name: course full name (unique course id common in all three files) --- **Primary Key**
	* Faculty: ignore
	* Course Types: same as data in course file - repeated for each session with a common Short or Full name - comma separated course tags (e.g. program the course is in (BScPharm, PharmD, PPPharmD), year of program (1st, 2nd, 3rd), category of course content (pharm sci, practice skills, etc.))
	* Instructors: same as data in course file - repeated for each session with a common Short or Full name - comma separated list of instructor names (names can contain special characters for accents, etc that produce errors, names should also be checked to find and replace similar repeats with standardized consistent results)
	* TAs: same as data in course file - repeated for each session with a common Short or Full name - comma separated list of course TAs
	* Session title: title of lecture lab or seminar
	* Section: ignore
	* Location: room location
	* Guest teacher: name(s) of guest lecturers (names can contain special characters for accents, etc that produce errors, names should also be checked to find and replace similar repeats with standardized consistent results)
	* Type: session type Lec (lecture), Lab, Seminar
	* Length: session length in mins
	* Date: date session occurs (this data is very error prone - the dates will always be in the right sequence but the actual dates are not reliable. use the Year and Term fields as the initial basis to sort results, then sort by this Date field).
	* Teaching strategies: comma separated list of teaching strategies employed
	* Instruction type: face-to-face or distance
	* topics: comma separated list of topics covered in the session
	* Specific objectives: comma separated list of session learning outcomes
	* Course outcomes: all: multiple columns for each course outcome attached to this sessions
	
* [assessments level dataset](data/assessments.csv): metadata on all the assessments in each course. 

	* Short Name: course short name (unique course id common in all three files) 
	* Full Name: course full name (unique course id common in all three files) --- **Primary Key**
	* Faculty: ignore
	* Course Types: same as data in course file - repeated for each assessment with a common Short or Full name - comma separated course tags (e.g. program the course is in (BScPharm, PharmD, PPPharmD), year of program (1st, 2nd, 3rd), category of course content (pharm sci, practice skills, etc.))
	* Instructors: same as data in course file - repeated for each assessment with a common Short or Full name - comma separated list of instructor names (names can contain special characters for accents, etc that produce errors)
	* TAs: same as data in course file - repeated for each session with a common Short or Full name - comma separated list of course TAs
	* Assessment title: title of assessment
	* Assessment type: label for type of assessment (exam, assignment, quiz)
	* Section: label for lecture, lab or seminar section e.g. A1, B2
	* Format: exam format choice (multiple choice, written response, etc.)
	* weight: assessment weight in percent
	* cumulative: y/n variable indicating if exam is cumulative
	* due date: date assessment is due or happens (data also unreliable - see description under session for this field)
	* Specific objectives: comma separated list of session learning outcomes assessed
	* Course outcomes: all: multiple columns for each course outcome attached to this session
