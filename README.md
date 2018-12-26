## Search Syllabus

Many higher level educational programs in the West provide a fair bit of flexibility to the instructors around how to structure the courses. But we still want students to have certain basic skills when they graduate. To accomplish that, certifying boards mandate that educational programs teach and assess a broad set of core skills in a systematic manner.

To help administrators easily find out gaps in instruction and assessment of various skills, this tool provides a quick way to search and sift through lectures, labs, seminars, and assessments. 

The tool is powered by three joinable datasets: a [course level dataset](data/courses.csv), which contains metadata on each course, a [session level dataset](data/sessions.csv), which contains metadata on all the sessions in each course, and [assessments level dataset](data/assessments.csv), which contains metadata on all the assessments in each course. The schema and details about the column names for each of the files is posted [here](raw_data_schema.md).

### Functionality

* Database: Swap out the database with a new set of CSVs.

* Interface:

See [wire_diagram.pdf](wire_diagram.pdf) for the proposed UI.

Here's the workflow:

1. Users enter keyword(s) and year/term range. We left_join course, session, and assessments data and report **back all courses** where one or more of the keywords match in session, assessments or course level data.

2. If the keyword(s) is in the course level data, we highlight the keyword(s) in the table.

3. Users can then sort or filter the columns "Course name", "Year", "Term", "Credits", "Faculty Tags", "Course Instructor(s)", and "Teaching Assistants" columns. 

4. They can also export as CSV or pdf the final table.

5. They can also see all the sessions and assessments related to the final filtered table from #3. The sessions and assessments will come out as separate tables on the same page. Both of these tables will support #2, #3, and #4.
	* Table of session/assessments results should have sort and filter functionality for "Course name", "Type", "Date", "Length", "Course Instructor", "Lecturer", "Teaching Strategies", and "Delivery Mode" columns

## Deliverables

* Deployed application without errors
* Documented scripts in clean style
* A readme that lays out how the code is organized
* A config file that has details of the database, etc.
