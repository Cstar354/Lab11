import os
import matplotlib.pyplot as plt

students = {}
assignments = {}
submissions = []

with open('data/students.txt') as f:
    for line in f:
        parts = line.strip().split(',')
        name = ','.join(parts[:-1])  # name can have commas if needed
        sid = parts[-1]

with open('data/assignments.txt') as f:
    for line in f:
        parts = line.strip().rsplit(' ', 2)
        name = parts[0]
        point_value = int(parts[1])
        aid = parts[2]
        assignments[aid] = {'name': name, 'points': point_value}

submission_dir = 'data/submissions'
for file in os.listdir(submission_dir):
    with open(os.path.join(submission_dir, file)) as f:
        for line in f:
            sid,aid,percent = line.strip().split()
            submissions.append({'sid': sid, 'aid': aid, 'percent': float(percent)})

student_name_to_id = {name: sid for sid, name in students.items()}
assignment_name_to_id = {info['name']: aid for aid, info in assignments.items()}

print("1. Student grade\n2. Assignment statistics\n3. Assignment graph\n")
choice = input("Enter your selection:")

if choice == '1':
    name = input("What is the student's name: ")
    sid = student_name_to_id.get(name)
    if not sid:
        print("Student not found")
    else:
        total = 0
        for s in submissions:
            if s['sid'] == sid:
                assignment = assignments[s['aid']]
                total += assignment['points'] * (s['percent'] / 100)
        grade = round((total / 1000) * 100)
        print(f"{grade}%")

elif choice == 2:
    aname = input("What is the assignment name: ")
    aid = assignment_name_to_id.get(aname)
    if not aid:
        print("Assignment not found")
    else:
        scores = [s['percent'] for s in submissions if s['aid'] == aid]
        print(f"Min: {int(min(scores))}%")
        print(f"Avg: {int(sum(scores) / len(scores))}%")
        print(f"Max: {int(max(scores))}%")

elif choice == '3':
    aname = input("What is the assignment name: ")
    aid = assignment_name_to_id.get(aname)
    if not aid:
        print("Assignment not found")
    else:
        scores = [s['percent'] for s in submissions if s['aid'] == aid]
        plt.hist(scores, bins=[0, 25, 50, 75, 100])
        plt.title(f"Score Distribution: {aname}")
        plt.xlabel("Percent")
        plt.ylabel("Number of Students")
        plt.show()

else:
    print("Invalid selection.")

