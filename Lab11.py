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
                # Split by space to separate ID and name
                student_id, student_name = line.split(maxsplit=1)
                students[student_id] = student_name
    except FileNotFoundError:
        print("The file 'students.txt' was not found.")
    except Exception as e:
        print(f"Error loading students: {e}")


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
    try:
        for filename in os.listdir('data/submissions'):
            if filename.endswith('.txt'):
                with open(f'data/submissions/{filename}') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split(', ')
                        if len(parts) == 3:
                            student_id = parts[0].strip()
                            assignment_id = parts[1].strip()
                            score = float(parts[2].strip())
                            submissions.setdefault(student_id, []).append({'assignment_id': assignment_id, 'score': score})
                        else:
                            print(f"Skipping invalid line in submissions file: {line}")
    except FileNotFoundError:
        print("The 'submissions' folder was not found.")
    except Exception as e:
        print(f"Error loading submissions: {e}")

# Function to calculate the grade for a student
def calculate_grade(student_name):
    total_score = 0
    total_points = 0

    # Go through all submissions and assignments
    for student_id, submission_list in submissions.items():
        if students.get(student_id) == student_name:
            for submission in submission_list:
                assignment_id = submission['assignment_id']
                score = submission['score']
                if assignment_id in assignments:
                    total_score += score
                    total_points += assignments[assignment_id]['points']

    if total_points == 0:
        print(f"Error: No valid assignments found for {student_name}")
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
