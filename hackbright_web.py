"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, session, redirect

import hackbright

app = Flask(__name__)


# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

@app.route("/student-search")
def get_student_form():
	"""Show form for searching for a student."""

	return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    rows = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
    						first=first,
    						last=last,
    						github=github,
    						rows=rows)

    return html

@app.route("/student-add", methods=['POST', 'GET'])
def student_add():
	"""Add a student."""

	if request.method == 'POST':

		first_name = request.form['first_name']
		last_name = request.form['last_name']
		github = request.form['github']

		hackbright.make_new_student(first_name, last_name, github)

		return redirect("/student-add-success")

	else:

	# flash("Student successfully added")

	# return html
		return render_template("student_add.html")

@app.route("/student-add-success")
def student_add_success():
	"""Give user link to student page."""

	return render_template("student_add_success.html")


@app.route("/project/<project_title>")
def get_project(project_title):
	""" Provides the project title, description & maximum grade """

	title, description, grade = hackbright.get_project_by_title(project_title)


	return render_template("project.html",
							title=title,
							description=description,
							grade=grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
