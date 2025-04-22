import os
import matplotlib.pyplot as plt

# Global variables to store data
students = {}
assignments = {}
submissions = {}

# Function to load students data
def load_students():
    try:
        with open('data/students.txt') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                student_id, student_name = line.split(maxsplit=1)
                students[student_id] = student_name
    except FileNotFoundError:
        print("The file 'students.txt' was not found.")
    except Exception as e:
        print(f"Error loading students: {e}")

def load_assignments():
    global assignments
    try:
        with open(os.path.join('data', 'assignments.txt')) as f:
            lines = [line.strip() for line in f if line.strip()]
            for i in range(0, len(lines), 3):
                if i + 2 < len(lines):
                    name = lines[i]
                    aid = lines[i+1]
                    points = int(lines[i+2])
                    assignments[aid] = {'name': name, 'points': points}
                else:
                    print(f"Skipping incomplete assignment block starting at line {i+1}")
    except FileNotFoundError:
        print("assignments.txt file not found.")

def load_submissions():
    global submissions
    try:
        submissions_dir = os.path.join('data', 'submissions')
        for filename in os.listdir(submissions_dir):
            filepath = os.path.join(submissions_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath) as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) == 3:
                            sid, aid, score = parts
                            if sid not in submissions:
                                submissions[sid] = []
                            submissions[sid].append({
                                'assignment_id': aid,
                                'score': int(score)
                            })
                        else:
                            print(f"Skipping invalid submission line: {line.strip()}")
    except FileNotFoundError:
        print("Submissions folder not found.")

def calculate_grade(student_name):
    total_score = 0
    total_points = 0

    for sid, name in students.items():
        if name == student_name:
            if sid in submissions:
                for submission in submissions[sid]:
                    aid = submission['assignment_id']
                    if aid in assignments:
                        total_score += submission['score']
                        total_points += assignments[aid]['points']
            break

    if total_points == 0:
        return None

    grade_percentage = round((total_score / total_points) * 100)
    return grade_percentage

def assignment_statistics(assignment_name):
    assignment_id = None
    for aid, assignment in assignments.items():
        if assignment['name'] == assignment_name:
            assignment_id = aid
            break

    if not assignment_id:
        print(f"Assignment not found: {assignment_name}")
        return

    scores = []
    for student_submissions in submissions.values():
        for submission in student_submissions:
            if submission['assignment_id'] == assignment_id:
                scores.append(submission['score'])

    if not scores:
        print(f"No submissions found for assignment: {assignment_name}")
        return

    print(f"Min: {min(scores):.0f}%")
    print(f"Avg: {sum(scores)/len(scores):.0f}%")
    print(f"Max: {max(scores):.0f}%")

def assignment_graph(assignment_name):
    assignment_id = None
    for aid, assignment in assignments.items():
        if assignment['name'] == assignment_name:
            assignment_id = aid
            break

    if not assignment_id:
        print(f"Assignment not found: {assignment_name}")
        return

    scores = []
    for student_submissions in submissions.values():
        for submission in student_submissions:
            if submission['assignment_id'] == assignment_id:
                scores.append(submission['score'])

    if not scores:
        print(f"No submissions found for assignment: {assignment_name}")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.xlabel('Scores')
    plt.ylabel('Number of Students')
    plt.title(f"Scores Distribution for {assignment_name}")
    plt.show()

def main():
    load_students()
    load_assignments()
    load_submissions()

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print("Enter your selection: ", end="")
    try:
        choice = int(input())
        if choice == 1:
            print("What is the student's name: ", end="")
            student_name = input()
            grade_percentage = calculate_grade(student_name)
            if grade_percentage is not None:
                print(f"{grade_percentage}%")
            else:
                print("Student or grades not found.")
        elif choice == 2:
            print("What is the assignment name: ", end="")
            assignment_name = input()
            assignment_statistics(assignment_name)
        elif choice == 3:
            print("What is the assignment name: ", end="")
            assignment_name = input()
            assignment_graph(assignment_name)
        else:
            print("Invalid selection, try again.")
    except ValueError:
        print("Please enter a valid option.")

if __name__ == '__main__':
    main()
