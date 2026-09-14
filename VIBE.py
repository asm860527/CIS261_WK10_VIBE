#Amanda Mockbee
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator."""

FILE_NAME = "student_grades.txt"


def calculate_grade(average):
	"""Return the letter grade for an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def get_score(test_number):
	"""Prompt until a valid score from 0 through 100 is entered."""
	while True:
		try:
			score = float(input(f"Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Please enter a score between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	"""Prompt for and add one student record."""
	name = input("Student name: ").strip()
	while not name:
		print("Student name cannot be empty.")
		name = input("Student name: ").strip()

	student_id = input("Student ID: ").strip()
	while not student_id:
		print("Student ID cannot be empty.")
		student_id = input("Student ID: ").strip()

	test1 = get_score(1)
	test2 = get_score(2)
	test3 = get_score(3)
	average = (test1 + test2 + test3) / 3

	students.append({
		"name": name,
		"id": student_id,
		"test1": test1,
		"test2": test2,
		"test3": test3,
		"average": average,
		"grade": calculate_grade(average),
	})
	print(f"Added {name} with an average of {average:.2f} ({calculate_grade(average)}).")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print("No student records available.")
		return

	headings = ["Name", "ID", "Test 1", "Test 2", "Test 3", "Average", "Grade"]
	rows = [
		[
			student["name"],
			student["id"],
			f"{student['test1']:.2f}",
			f"{student['test2']:.2f}",
			f"{student['test3']:.2f}",
			f"{student['average']:.2f}",
			student["grade"],
		]
		for student in students
	]
	widths = [max(len(headings[index]), *(len(row[index]) for row in rows))
			  for index in range(len(headings))]
	separator = "-+-".join("-" * width for width in widths)
	print(" | ".join(headings[index].ljust(widths[index]) for index in range(len(headings))))
	print(separator)
	for row in rows:
		print(" | ".join(row[index].ljust(widths[index]) for index in range(len(row))))


def display_statistics(students):
	"""Display highest, lowest, and class average scores."""
	if not students:
		print("No student records available for statistics.")
		return

	averages = [student["average"] for student in students]
	highest = max(students, key=lambda student: student["average"])
	lowest = min(students, key=lambda student: student["average"])
	print(f"Highest average: {highest['average']:.2f} ({highest['name']})")
	print(f"Lowest average: {lowest['average']:.2f} ({lowest['name']})")
	print(f"Class average: {sum(averages) / len(averages):.2f}")


def search_students(students):
	"""Display records whose names contain the search text."""
	search_name = input("Enter a student name to search for: ").strip().lower()
	matches = [student for student in students if search_name in student["name"].lower()]
	if matches:
		display_students(matches)
	else:
		print("No students found.")


def save_students(students, file_name=FILE_NAME):
	"""Save student records using the required pipe-delimited format."""
	try:
		with open(file_name, "w", encoding="utf-8") as file:
			for student in students:
				file.write(
					f"{student['name']}|{student['id']}|{student['test1']:.2f}|"
					f"{student['test2']:.2f}|{student['test3']:.2f}|"
					f"{student['average']:.2f}|{student['grade']}\n"
				)
		print(f"Saved {len(students)} student record(s) to {file_name}.")
	except OSError as error:
		print(f"Could not save student records: {error}")


def load_students(file_name=FILE_NAME):
	"""Load student records, returning an empty list when no file exists."""
	students = []
	try:
		with open(file_name, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					test1, test2, test3, average = (float(value) for value in fields[2:6])
				except ValueError:
					print(f"Skipping invalid scores on line {line_number}.")
					continue
				students.append({
					"name": fields[0],
					"id": fields[1],
					"test1": test1,
					"test2": test2,
					"test3": test3,
					"average": average,
					"grade": fields[6],
				})
		print(f"Loaded {len(students)} student record(s) from {file_name}.")
	except FileNotFoundError:
		print(f"No existing {file_name} file found. Starting with no records.")
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def display_menu():
	"""Display the main menu."""
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("ESC. Save and exit")


def main():
	"""Run the student grade calculator."""
	students = load_students()
	while True:
		display_menu()
		choice = input("Select an option: ").strip()
		if choice == "\x1b" or choice.upper() == "ESC":
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_students(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid option. Please choose 1-5 or ESC.")


if __name__ == "__main__":
	main()

