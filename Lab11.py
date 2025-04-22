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
                student_id = line[:3]  # Assume student ID is the first 3 characters
                student_name = line[3:].strip()  # The rest is the name
                students[student_id] = student_name
    except FileNotFoundError:
        print("The file 'students.txt' was not found.")
    except Exception as e:
        print(f"Error loading students: {e}")

# Function to load assignments data
def load_assignments():
    assignments = {}
    try:
        with open(os.path.join('data', 'assignments.txt')) as f:
            lines = [line.strip() for line in f if line.strip()]  # Remove blank lines
            for i in range(0, len(lines), 3):  # Step by 3 lines per assignment
                if i + 2 < len(lines):  # Ensure we have a full triplet
                    name = lines[i]
                    aid = lines[i+1]
                    points = int(lines[i+2])
                    assignments[aid] = {
                        'name': name,
                        'points': points
                    }
                else:
                    print(f"Skipping incomplete assignment block starting at line {i+1}")
    except FileNotFoundError:
        print("assignments.txt file not found.")
    return assignments

# Function to load submissions data
def load_submissions():
    submissions = []
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
                            submissions.append({
                                'student_id': sid,
                                'assignment_id': aid,
                                'score': int(score)
                            })
                        else:
                            print(f"Skipping invalid submission line: {line.strip()}")
    except FileNotFoundError:
        print("Submissions folder not found.")
    return submissions

# Function to calculate the grade for a student
def calculate_grade(student_name):
    total_score = 0
    total_points = 0

    # Go through all submissions and assignments
    for student_id, submission_list in submissions.items():
        # Match student_name to stored student name (case insensitive)
        student_name_in_data = students.get(student_id, '').strip()
        if student_name_in_data.lower() == student_name.strip().lower():
            for submission in submission_list:
                assignment_id = submission['assignment_id']
                score = submission['score']
                if assignment_id in assignments:
                    total_score += score
                    total_points += assignments[assignment_id]['points']

    if total_points == 0:
        print("Student or grades not found.")
        return None

    grade_percentage = round((total_score / total_points) * 100)
    return grade_percentage

# Function to display assignment statistics
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

    min_score = min(scores)
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)

    print(f"Min: {min_score:.0f}%")
    print(f"Avg: {avg_score:.0f}%")
    print(f"Max: {max_score:.0f}%")

# Function to display assignment score histogram
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

    # Plotting histogram using matplotlib
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.xlabel('Scores')
    plt.ylabel('Number of Students')
    plt.title(f"Scores Distribution for {assignment_name}")
    plt.show()

# Main function to run the program
def main():
    load_students()
    load_assignments()
    load_submissions()

    while True:
        print("\n1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        try:
            choice = int(input("Enter your selection: "))
            if choice == 1:
                student_name = input("What is the student's name: ")
                grade_percentage = calculate_grade(student_name)
                if grade_percentage is not None:
                    print(f"{grade_percentage}%")
            elif choice == 2:
                assignment_name = input("What is the assignment name: ")
                assignment_statistics(assignment_name)
            elif choice == 3:
                assignment_name = input("What is the assignment name: ")
                assignment_graph(assignment_name)
            else:
                print("Invalid selection, try again.")
        except ValueError:
            print("Please enter a valid option.")

        # Exit after one execution to avoid EOFError in non-interactive environments
        break

if __name__ == '__main__':
    main()
