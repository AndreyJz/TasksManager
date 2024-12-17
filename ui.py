import streamlit as st
from controller import add_task, get_all_tasks, update_task, delete_task, export_tasks_to_json, import_tasks_from_json


def render():
    st.title("Task Manager")

    st.write("Welcome to Task Manager! This allows you to create, read, update, and delete tasks.")

    if st.button("Export all Tasks to Json Format"):
        export_tasks_to_json()
        st.success("Tasks exported successfully!")

    if 'file_data' not in st.session_state:
        st.session_state.file_data = None

# ----------------------------------------------------------------

    file = st.file_uploader("Import a Task on Json Format", type="json")

    if file is not None:
        if file is not None:
            st.session_state.file_data = file.getvalue().decode("utf-8")
            st.success("File uploaded successfully!")
        
        if st.session_state.file_data is not None:
            try:
                import_tasks_from_json(st.session_state.file_data)
                st.success("Tasks imported successfully!")
            except Exception as e:
                st.error(f"Error importing tasks: {e}")
        else:
            st.warning("Please upload a file.")

# ----------------------------------------------------------------

    name = st.text_input("Please enter the title of your task")
    dsc = st.text_area("Now enter the description of your task")

    if st.button("Add Task"):
        if name and dsc:
            add_task(name, dsc)
            st.success("Task added successfully!")
        else:
            st.error("Please fill out all fields!")

# ----------------------------------------------------------------

    st.subheader("Your Tasks")
    tasks = get_all_tasks()
    for task in tasks:
        with st.container():
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 15px; margin: 1vi; border-radius: 10px; background-color: #f9f9f9;">
                    <h3 style="margin: 0; color: #333;">Task Title: {task.name}</h3>
                    <p style="margin: 5px 0; color: #555;">{task.description}</p>
                    <p style="margin: 5px 0; color: #777;">Completed: {'Yes' if task.completed else 'No'}</p>
                    <p style="margin: 5px 0; color: #999;">Date: {task.date}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mark as Completed", key=f"complete_{task.id}"):
                    update_task(task.id, completed=True)
                    st.success("Now your task has been completed")
                    st.button("Okay!")
            with col2:
                if st.button("Delete", key=f"delete_{task.id}"):
                    delete_task(task.id)
                    st.success("This task has been deleted")
                    st.button("Okay!")

