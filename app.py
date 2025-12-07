import streamlit as st
import uuid

def generate_unique_id():
    return str(uuid.uuid4())

def delete_task(task_id):
    st.session_state.tasks = [task for task in st.session_state.tasks if task["id"] != task_id]

def toggle_complete(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break

def set_edit_mode(task_id, description):
    st.session_state.edit_task_id = task_id
    st.session_state.edit_task_description = description

def update_task_description(task_id):
    new_description = st.session_state[f"edit_input_{task_id}"]
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            break
    st.session_state.edit_task_id = None
    st.session_state.edit_task_description = ""

def main():
    st.title("My To-Do App")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "edit_task_id" not in st.session_state:
        st.session_state.edit_task_id = None
    if "edit_task_description" not in st.session_state:
        st.session_state.edit_task_description = ""

    # UI for adding new tasks
    with st.form("new_task_form", clear_on_submit=True):
        new_task_description = st.text_input("New Task")
        add_task_button = st.form_submit_button("Add Task")

        if add_task_button and new_task_description:
            st.session_state.tasks.append({
                "id": generate_unique_id(),
                "description": new_task_description,
                "completed": False
            })
            st.success("Task added!")

    st.subheader("Your Tasks")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3, col4 = st.columns([0.05, 0.6, 0.15, 0.15])
            
            with col1:
                st.checkbox("", key=f"complete_{task['id']}", value=task['completed'], on_change=toggle_complete, args=(task['id'],))
            with col2:
                if st.session_state.edit_task_id == task['id']:
                    st.text_input("Edit task", value=st.session_state.edit_task_description, key=f"edit_input_{task['id']}", label_visibility="collapsed")
                    st.button("Save", key=f"save_{task['id']}", on_click=update_task_description, args=(task['id'],))
                else:
                    st.markdown(f"<span style='text-decoration: {'line-through' if task['completed'] else 'none'}'>{task['description']}</span>", unsafe_allow_html=True)
            with col3:
                if st.session_state.edit_task_id != task['id']:
                    st.button("Edit", key=f"edit_{task['id']}", on_click=set_edit_mode, args=(task['id'], task['description']))
                else:
                    st.button("Cancel", key=f"cancel_edit_{task['id']}", on_click=set_edit_mode, args=(None, ""))
            with col4:
                st.button("Delete", key=f"delete_{task['id']}", on_click=delete_task, args=(task['id'],))
    else:
        st.info("No tasks yet. Add one above!")


if __name__ == "__main__":
    main()
