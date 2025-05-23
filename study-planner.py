import datetime
import pickle

class Assignment:
    def __init__(self, title, deadline, difficulty):
        self.title = title
        self.deadline = deadline
        self.difficulty = difficulty
        self.is_completed = False

class Course:
    def __init__(self, name):
        self.name = name
        self.assignments = []

def days_until_deadline(deadline):
    year, month, day = map(int, deadline.split('-'))
    today = datetime.date.today()
    deadline_date = datetime.date(year, month, day)
    delta = (deadline_date - today).days
    return delta

def get_total_study_hours(difficulty):
    if difficulty == "Easy":
        return 4
    elif difficulty == "Medium":
        return 6
    elif difficulty == "Hard":
        return 9
    return 0

def get_priority(assignment):
    days = days_until_deadline(assignment.deadline)
    difficulty_score = {"Easy": 1, "Medium": 2, "Hard": 3}.get(assignment.difficulty, 0)
    if days <= 0:
        return float('inf')
    return days * difficulty_score

def input_course_data(courses):
    course_name = input("\nEnter course name: ")
    course = Course(course_name)
    num_assignments = int(input("Enter number of assignments: "))
    for i in range(num_assignments):
        print(f"\n--- Assignment {i + 1} ---")
        title = input("Enter assignment title: ")
        deadline = input("Enter assignment deadline (YYYY-MM-DD): ")
        difficulty = input("Enter assignment difficulty (Easy, Medium, Hard): ")
        assignment = Assignment(title, deadline, difficulty)
        course.assignments.append(assignment)
    courses.append(course)

def generate_study_plan(courses):
    print("\n================== STUDY PLAN ==================")
    for course in courses:
        print(f"\nCourse: {course.name}")
        print("------------------------------------------------")
        assignments_sorted = sorted(course.assignments, key=get_priority)
        for assignment in assignments_sorted:
            if assignment.is_completed:
                print(f"Assignment: {assignment.title}")
                print(f" - Status: ✅ Completed")
                print("------------------------------------------------")
                continue

            days_remaining = days_until_deadline(assignment.deadline)
            if days_remaining < 0:
                print(f"Assignment: {assignment.title}")
                print(f" - Deadline: {assignment.deadline} (Past Deadline)")
                print(f" - Status: ❌ Deadline missed.")
                print("------------------------------------------------")
                continue

            total_study_hours = get_total_study_hours(assignment.difficulty)
            required_days = max(1, days_remaining)
            hours_per_day = round(total_study_hours / required_days, 2)

            print(f"Assignment: {assignment.title}")
            print(f" - Deadline: {assignment.deadline}")
            print(f" - Difficulty: {assignment.difficulty}")
            print(f" - Total study time: {total_study_hours} hours")
            print(f" - Suggested: {hours_per_day} hrs/day for next {required_days} days")
            print("------------------------------------------------")
    print("================================================")

def mark_assignment_completed(courses):
    print("\n===== Mark Assignment as Completed =====")
    for i, course in enumerate(courses, 1):
        print(f"{i}. {course.name}")
    course_choice = int(input("Select course number: ")) - 1
    if 0 <= course_choice < len(courses):
        course = courses[course_choice]
        for i, assignment in enumerate(course.assignments, 1):
            status = "Completed" if assignment.is_completed else "Pending"
            print(f"{i}. {assignment.title} - {status}")
        assignment_choice = int(input("Select assignment to mark as completed: ")) - 1
        if 0 <= assignment_choice < len(course.assignments):
            course.assignments[assignment_choice].is_completed = True
            print(f"\n✅ Marked '{course.assignments[assignment_choice].title}' as completed.")
        else:
            print("Invalid assignment number.")
    else:
        print("Invalid course number.")

def show_progress(courses):
    print("\n===== Progress Report =====")
    for course in courses:
        total = len(course.assignments)
        completed = sum(1 for a in course.assignments if a.is_completed)
        percent = (completed / total * 100) if total > 0 else 0
        print(f"{course.name}: {completed}/{total} completed ({percent:.2f}%)")

def show_upcoming_deadlines(courses, days=7):
    print(f"\n===== Assignments Due in Next {days} Days =====")
    today = datetime.date.today()
    for course in courses:
        for a in course.assignments:
            deadline_date = datetime.datetime.strptime(a.deadline, "%Y-%m-%d").date()
            if 0 <= (deadline_date - today).days <= days and not a.is_completed:
                print(f"{a.title} (Course: {course.name}) - Due: {a.deadline}")

def alert_overdue(courses):
    print("\n===== Overdue Assignments =====")
    today = datetime.date.today()
    found = False
    for course in courses:
        for a in course.assignments:
            deadline_date = datetime.datetime.strptime(a.deadline, "%Y-%m-%d").date()
            if deadline_date < today and not a.is_completed:
                print(f"{a.title} (Course: {course.name}) - Missed Deadline: {a.deadline}")
                found = True
    if not found:
        print("No overdue assignments 🎉")

def save_data(courses, filename="study_planner.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(courses, f)

def load_data(filename="study_planner.pkl"):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def main():
    courses = load_data()
    while True:
        print("\n********* PERSONALIZED STUDY PLANNER MENU *********")
        print("1. Add Course and Assignments")
        print("2. Generate Study Plan")
        print("3. Mark Assignment as Completed")
        print("4. Show Progress Report")
        print("5. Show Upcoming Deadlines")
        print("6. Show Overdue Assignments")
        print("7. Save Progress")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            input_course_data(courses)
        elif choice == '2':
            generate_study_plan(courses)
        elif choice == '3':
            mark_assignment_completed(courses)
        elif choice == '4':
            show_progress(courses)
        elif choice == '5':
            show_upcoming_deadlines(courses)
        elif choice == '6':
            alert_overdue(courses)
        elif choice == '7':
            save_data(courses)
            print("✅ Progress saved.")
        elif choice == '8':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
