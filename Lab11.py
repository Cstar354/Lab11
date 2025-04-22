import matplotlib.pyplot as plt

# Load student data
students = {}
with open("data/students.txt") as f:
    for line in f:
        line = line.strip()
        if ',' in line:
            name, sid = line.split(',')
            students[name.strip()] = sid.strip()

# Load assignment data
assignments = {}
assignment_points = {}
with open("data/assignments.txt") as f:
    for line in f:
        line = line.strip()
        if ',' in line:
            parts = line.split(',')
            name = parts[0].strip()
            aid = parts[1].strip()
            points = int(parts[2].strip())
            assignments[name] = aid
            assignment_points[aid] = points

# Load submission data
submissions = {}
with open("data/submissions.txt") as f:
    for line in f:
        line = line.strip()
        if ',' in line:
            parts = line.split(',')
            if len(parts) >= 3:
                sid = parts[0].strip()
                aid = parts[1].strip()
                percent = float(parts[2].strip())
                submissions.setdefault(sid, {})[aid] = percent

# Display menu
print("1. Student grade")
print("2. Assignment statistics")
print("3. Assignment graph")
selection = input("\nEnter your selection: ")

# Option 1: Student grade
if selection == "1":
    student_name = input("What is the student's name: ").strip()
    if student_name not in students:
        print("Student not found")
    else:
        sid = students[student_name]
        total_earned = 0
        total_possible = 1000
        for aid, percent in submissions[sid].items():
            points = assignment_points.get(aid, 0)
            total_earned += percent * points
        final_grade = round((total_earned / total_possible) * 100)
        print(f"{final_grade}%")

# Option 2: Assignment statistics
elif selection == "2":
    assignment_name = input("What is the assignment name: ").strip()
    if assignment_name not in assignments:
        print("Assignment not found")
    else:
        aid = assignments[assignment_name]
        scores = []
        for sid in submissions:
            if aid in submissions[sid]:
                percent = submissions[sid][aid]
                scores.append(round(percent * 100))
        if scores:
            print(f"Min: {min(scores)}%")
            print(f"Avg: {sum(scores) // len(scores)}%")
            print(f"Max: {max(scores)}%")

# Option 3: Assignment graph
elif selection == "3":
    assignment_name = input("What is the assignment name: ").strip()
    if assignment_name not in assignments:
        print("Assignment not found")
    else:
        aid = assignments[assignment_name]
        scores = []
        for sid in submissions:
            if aid in submissions[sid]:
                percent = submissions[sid][aid]
                scores.append(round(percent * 100))
        if scores:
            plt.hist(scores, bins=[0, 25, 50, 75, 100])
            plt.title(f"{assignment_name} Score Distribution")
            plt.xlabel("Score (%)")
            plt.ylabel("Number of Students")
            plt.show()
