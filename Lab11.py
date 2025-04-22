import os
import matplotlib.pyplot as plt

# Store data for students and submissions
students = {}
submissions = {}

# Read the students.txt file
with open('data/students.txt') as f:
    for line in f:
        name, sid = line.strip().split(', ')  # Split by comma
        students[sid] = name  # Store the student ID and name in a dictionary

# Process the submissions folder (assumes the folder contains files for each student's assignment submissions)
submissions_folder = 'data/submissions'

# Iterate through each file in the folder
for filename in os.listdir(submissions_folder):
    student_id = filename.split('.')[0]  # Assume filename is the student ID (e.g., 12345.txt)
    submissions[student_id] = []
    
    with open(os.path.join(submissions_folder, filename)) as f:
        for line in f:
            aid, score = line.strip().split(', ')  # Split by comma
            score = float(score)  # Convert score to float
            submissions[student_id].append((aid, score))  # Store each assignment and score

# Function to calculate a student's grade
def calculate_student_grade(sid):
    if sid not in submissions:
        return "Student not found"
    
    total_score = sum(score for _, score in submissions[sid])
    return round(total_score)

# Function to get assignment statistics
def assignment_statistics(aid):
    scores = []
    
    for sid in submissions:
        for submission in submissions[sid]:
            if submission[0] == aid:
                scores.append(submission[1])
    
    if not scores:
        return "Assignment not found"
    
    min_score = min(scores)
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)
    
    return f"Min: {min_score}%\nAvg: {avg_score:.2f}%\nMax: {max_score}%"

# Function to plot a histogram of assignment scores
def plot_assignment_graph(aid):
    scores = []
    
    for sid in submissions:
        for submission in submissions[sid]:
            if submission[0] == aid:
                scores.append(submission[1])
    
    if not scores:
        return "Assignment not found"
    
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Scores for {aid}")
    plt.xlabel("Score Percentage")
    plt.ylabel("Frequency")
    plt.show()

# Main program loop
def main():
    while True:
        print("\n1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        print("4. Exit")

        try:
            selection = int(input("Enter your selection: "))

            if selection == 1:
                student_name = input("What is the student's name: ")
                student_found = False
                for sid, name in students.items():
                    if name.lower() == student_name.lower():
                        print(f"{name}'s grade: {calculate_student_grade(sid)}%")
                        student_found = True
                        break
                if not student_found:
                    print("Student not found")

            elif selection == 2:
                assignment_name = input("What is the assignment name: ")
                print(assignment_statistics(assignment_name))

            elif selection == 3:
                assignment_name = input("What is the assignment name: ")
                plot_assignment_graph(assignment_name)

            elif selection == 4:
                print("Exiting the program.")
                break

            else:
                print("Invalid selection, please try again.")
        
        except ValueError:
            print("Please enter a valid number.")

# Run the main program
if __name__ == "__main__":
    main()
