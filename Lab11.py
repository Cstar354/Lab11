import os

# Data storage
students = {}
assignments = {}
submissions = {}

# Function to read and parse students
def load_students():
    try:
        with open('data/students.txt') as f:
            for line in f:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                # Split by comma and space, handle variations in the format
                parts = line.split(',')  # Adjust split logic based on how the file is structured
                if len(parts) == 2:  # Ensure line has exactly 2 parts: name and student ID
                    name, sid = parts
                    students[sid.strip()] = name.strip()
                else:
                    print(f"Skipping invalid line in students file: {line}")
    except FileNotFoundError:
        print("The file 'students.txt' was not found.")
    except Exception as e:
        print(f"Error loading students: {e}")

# Function to read and parse assignments
def load_assignments():
    try:
        with open('data/assignments.txt') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')  # Adjust split logic based on how the file is structured
                if len(parts) == 3:
                    aname, points, aid = parts
                    assignments[aid.strip()] = {'name': aname.strip(), 'points': int(points.strip())}
                else:
                    print(f"Skipping invalid line in assignments file: {line}")
    except FileNotFoundError:
        print("The file 'assignments.txt' was not found.")
    except Exception as e:
        print(f"Error loading assignments: {e}")

# Function to read and parse submissions
def load_submissions():
    try:
        for filename in os.listdir('data/submissions/'):
            file_path = os.path.join('data/submissions', filename)
            if os.path.isfile(file_path):
                with open(file_path) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split(',')  # Assuming comma-separated values
                        if len(parts) == 3:
                            sid, aid, percentage = parts
                            if sid in students and aid in assignments:
                                if aid not in submissions:
                                    submissions[aid] = []
                                submissions[aid].append({'sid': sid, 'percentage': float(percentage)})
                        else:
                            print(f"Skipping invalid line in submissions file: {line}")
    except FileNotFoundError:
        print("The 'submissions' folder was not found.")
    except Exception as e:
        print(f"Error loading submissions: {e}")

# Main program
def main():
    # Load all data
    load_students()
    load_assignments()
    load_submissions()

    # Print menu and handle user input
    while True:
        print("1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        try:
            choice = int(input("Enter your selection: "))
            if choice == 1:
                student_name = input("What is the student's name: ")
                # Find student by name
                student_id = None
                for sid, name in students.items():
                    if name.lower() == student_name.lower():
                        student_id = sid
                        break
                if student_id:
                    total_score = 0
                    total_points = 0
                    for aid, submissions_list in submissions.items():
                        for submission in submissions_list:
                            if submission['sid'] == student_id:
                                total_score += (submission['percentage'] / 100) * assignments[aid]['points']
                                total_points += assignments[aid]['points']
                    grade_percentage = round((total_score / total_points) * 100)
                    print(f"{grade_percentage}%")
                else:
                    print("Student not found")
            
            elif choice == 2:
                assignment_name = input("What is the assignment name: ")
                assignment_id = None
                for aid, details in assignments.items():
                    if details['name'].lower() == assignment_name.lower():
                        assignment_id = aid
                        break
                if assignment_id:
                    scores = [submission['percentage'] for submission in submissions.get(assignment_id, [])]
                    if scores:
                        min_score = min(scores)
                        max_score = max(scores)
                        avg_score = sum(scores) / len(scores)
                        print(f"Min: {min_score}%")
                        print(f"Avg: {avg_score:.2f}%")
                        print(f"Max: {max_score}%")
                    else:
                        print("No submissions found for this assignment.")
                else:
                    print("Assignment not found")

            elif choice == 3:
                assignment_name = input("What is the assignment name: ")
                assignment_id = None
                for aid, details in assignments.items():
                    if details['name'].lower() == assignment_name.lower():
                        assignment_id = aid
                        break
                if assignment_id:
                    scores = [submission['percentage'] for submission in submissions.get(assignment_id, [])]
                    if scores:
                        import matplotlib.pyplot as plt
                        plt.hist(scores, bins=[0, 25, 50, 75, 100])
                        plt.title(f"Scores for {assignment_name}")
                        plt.xlabel("Percentage")
                        plt.ylabel("Number of Students")
                        plt.show()
                    else:
                        print("No submissions found for this assignment.")
                else:
                    print("Assignment not found")

            else:
                print("Invalid choice. Please try again.")

            break  # Exit the loop after one operation
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")

# Run the main program
if __name__ == "__main__":
    main()
