import streamlit as st
import pandas as pd


if "students" not in st.session_state:
    st.session_state.students = []


def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


st.title("Student Grade Manager")

with st.form("student_form"):
    name = st.text_input("Name")
    mark = st.number_input("Mark", min_value=0, max_value=100, step=1)
    submitted = st.form_submit_button("Add")

if submitted:
    if name.strip():
        st.session_state.students.append(
            {
                "Name": name.strip(),
                "Mark": mark,
                "Grade": get_grade(mark),
            }
        )
        st.success(f"Added {name.strip()}.")
    else:
        st.error("Please enter a student name.")

if st.session_state.students:
    st.subheader("Students")

    students_df = pd.DataFrame(st.session_state.students)
    st.dataframe(
        students_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Name": st.column_config.TextColumn("Student", width="large"),
            "Mark": st.column_config.NumberColumn(
                "Mark", format="%d", width="small"
            ),
            "Grade": st.column_config.TextColumn("Grade", width="small"),
        },
    )

    marks = students_df["Mark"]

    st.subheader("Class Metrics")
    metric_columns = st.columns(3)
    metric_columns[0].metric("Average", f"{marks.mean():.1f}")
    metric_columns[1].metric("Highest", int(marks.max()))
    metric_columns[2].metric("Lowest", int(marks.min()))
else:
    st.info("Add a student to see the table and metrics.")