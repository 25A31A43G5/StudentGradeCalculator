import streamlit as st
import pandas as pd
from datetime import date

# Page settings
st.set_page_config(
    page_title="Student Grade Calculator",
    page_icon="🎓",
    layout="wide"
)

# Custom designpy
st.markdown("""
<style>
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

h1, h2, h3, p, label {
    color: var(--text-color);
}

[data-testid="stMetric"] {
    background-color: var(--secondary-background-color);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid var(--text-color);
}

[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
}

</style>
""", unsafe_allow_html=True)
# Heading
st.title("🎓 Student Grade Calculator")
st.write("Calculate marks, analyze performance and generate your report card.")

st.divider()

# Sidebar
st.sidebar.header("Student Details")
name = st.sidebar.text_input("Student Name", placeholder="Enter your name")
roll_no = st.sidebar.text_input("Roll Number", placeholder="Enter roll number")
class_name = st.sidebar.text_input("Class / Year", placeholder="e.g. B.Tech 2nd Year")

st.sidebar.info("Enter marks out of 100 for each subject.")

# Subjects
subjects = [
    "Mathematics",
    "Python Programming",
    "Java Programming",
    "Data Structures",
    "English"
]

st.subheader("📝 Enter Subject Marks")
st.caption("Each subject is out of 100 marks.")

marks = {}

columns = st.columns(2)

for i, subject in enumerate(subjects):
    with columns[i % 2]:
        marks[subject] = st.number_input(
            subject,
            min_value=0,
            max_value=100,
            value=75,
            step=1,
            key=subject
        )

# Calculate results
total = sum(marks.values())
maximum = len(subjects) * 100
percentage = (total / maximum) * 100
average = total / len(subjects)

# Pass condition: at least 35 in every subject
passed = all(mark >= 35 for mark in marks.values())

# Grade calculation
if not passed:
    grade = "F"
    result = "Fail"
elif percentage >= 90:
    grade = "A+"
    result = "Pass"
elif percentage >= 80:
    grade = "A"
    result = "Pass"
elif percentage >= 70:
    grade = "B"
    result = "Pass"
elif percentage >= 60:
    grade = "C"
    result = "Pass"
elif percentage >= 50:
    grade = "D"
    result = "Pass"
else:
    grade = "E"
    result = "Pass"

# Dashboard
st.divider()
st.subheader("📊 Performance Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Marks", f"{total} / {maximum}")
c2.metric("Percentage", f"{percentage:.2f}%")
c3.metric("Average", f"{average:.2f}")
c4.metric("Grade", grade)

if passed:
    st.success(f"Result: {result} 🎉")
else:
    st.error("Result: Fail. At least one subject is below 35 marks.")

# Charts
st.subheader("📈 Subject-wise Performance")

chart_data = pd.DataFrame({
    "Subject": list(marks.keys()),
    "Marks": list(marks.values())
})

st.bar_chart(
    chart_data,
    x="Subject",
    y="Marks",
    color="#3978d4"
)

# Subject table
st.subheader("📚 Detailed Marks")

chart_data["Maximum Marks"] = 100
chart_data["Status"] = chart_data["Marks"].apply(
    lambda mark: "Pass" if mark >= 35 else "Fail"
)

st.dataframe(chart_data, use_container_width=True, hide_index=True)

# Study suggestions
st.subheader("💡 Study Suggestions")

weak_subjects = [
    subject for subject, mark in marks.items() if mark < 50
]

if weak_subjects:
    st.warning(
        "Give extra practice to: " + ", ".join(weak_subjects)
    )
else:
    st.info("Good work! Keep practising all subjects consistently.")

# Report card
st.divider()
st.subheader("📄 Student Report Card")

if name.strip():
    st.write(f"**Student Name:** {name}")
else:
    st.write("**Student Name:** Not entered")

st.write(f"**Roll Number:** {roll_no or 'Not entered'}")
st.write(f"**Class / Year:** {class_name or 'Not entered'}")
st.write(f"**Report Date:** {date.today().strftime('%d-%m-%Y')}")

st.write(f"**Total:** {total} / {maximum}")
st.write(f"**Percentage:** {percentage:.2f}%")
st.write(f"**Grade:** {grade}")
st.write(f"**Final Result:** {result}")

# Downloadable report
report_data = pd.DataFrame({
    "Subject": list(marks.keys()),
    "Marks": list(marks.values()),
    "Maximum Marks": [100] * len(subjects),
    "Status": [
        "Pass" if mark >= 35 else "Fail"
        for mark in marks.values()
    ]
})

csv_data = report_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Marks Report (CSV)",
    data=csv_data,
    file_name="student_marks_report.csv",
    mime="text/csv"
)

st.caption("Student Grade Calculator | Built with python and Streamlit")
 
