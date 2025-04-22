import os
import matplotlib.pyplot as plt

def load_students():
    students = {}
    try:
        with open('data/students.txt') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(', ')
                if len(parts) == 2:
                    name, student_id = parts
                    students[student_id] = name
                else:
                    print(f"Skipping invalid line in students file: {line}")
    except FileNotFoundError:
        print("Error: students file not found!")
    return students

def load_assignments():
    assignments = {}
    try:
        with open('data/assignments.txt') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 3):
                if i + 2 < len(lines):
                    assignment_name = lines[i].strip()
                    assignment_id = lines[i + 1].strip()
                    points = int(lines[i + 2].strip())
                    assignments[assignment_name] = {'id': assignment_id, 'points': points}
                else:
                    print(f"Skipping invalid lines in assignments file.")
    except FileNotFoundError:
        print("Error: assignments file not found!")
    return assignments

def load_submissions():
    submissions = []
    try:
        with open('data/submissions.txt') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(', ')
                if len(parts) == 3:
                    student_id, assignment_id, percentage = parts
                    submissions.append((student_id, assignment_id, float(percentage)))
                else:
                    print(f"Skipping invalid line in submissions file: {line}")
    except FileNotFoundError:
        print("Error: submissions file not found!")
    return submissions

def calculate_student_grade(student_name, students, submissions, assignments):
    total_points = 0
    total_score = 0

    student_id = None
    for sid, name in students.items():
        if name == student_name:
            student_id = sid
            break

    if not student_id:
        print("Student not found.")
        return

    for submission in submissions:
        if submission[0] == student_id:
            assignment_name = next((name for name, data in assignments.items() if data['id'] == submission[1]), None)
            if assignment_name:
                total_points += assignments[assignment_name]['points']
                total_score += (submission[2] / 100) * assignments[assignment_name]['points']

    if total_points == 0:
        print(f"No valid assignments found for {student_name}.")
    else:
        grade_percentage = round((total_score / total_points) * 100)
        print(f"{student_name}'s grade: {grade_percentage}%")

def assignment_statistics(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found.")
        return

    assignment_id = assignments[assignment_name]['id']
    scores = []

    for submission in submissions:
        if submission[1] == assignment_id:
            scores.append(submission[2])

    if not scores:
        print("No submissions found for this assignment.")
        return

    min_score = min(scores)
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)

    print(f"Min: {min_score}%")
    print(f"Avg: {avg_score:.2f}%")
    print(f"Max: {max_score}%")

def assignment_graph(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found.")
        return

    assignment_id = assignments[assignment_name]['id']
    scores = []

    for submission in submissions:
        if submission[1] == assignment_id:
            scores.append(submission[2])

    if not scores:
        print("No submissions found for this assignment.")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Distribution of scores for {assignment_name}")
    plt.xlabel('Score Percentage')
    plt.ylabel('Number of Students')
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    while True:
        print("1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        selection = input("Enter your selection: ")

        if selection == '1':
            student_name = input("What is the student's name: ")
            calculate_student_grade(student_name, students, submissions, assignments)
        elif selection == '2':
            assignment_name = input("What is the assignment name: ")
            assignment_statistics(assignment_name, assignments, submissions)
        elif selection == '3':
            assignment_name = input("What is the assignment name: ")
            assignment_graph(assignment_name, assignments, submissions)
        else:
            print("Invalid selection. Please try again.")

        exit_choice = input("Would you like to perform another action? (y/n): ").lower()
        if exit_choice != 'y':
            break

if __name__ == "__main__":
    main()
