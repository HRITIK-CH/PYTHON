import streamlit as st
import os
import json

# File paths
TASKS_FILE = "tasks.json"
BIN_FILE = "deleted_tasks.json"

# Load tasks from file
def load_tasks():
    return json.load(open(TASKS_FILE)) if os.path.exists(TASKS_FILE) else []

def load_deleted_tasks():
    return json.load(open(BIN_FILE)) if os.path.exists(BIN_FILE) else []

# Save tasks
def save_tasks():
    with open(TASKS_FILE, "w") as file:
        json.dump(st.session_state.tasks, file, indent=4)

def save_deleted_tasks():
    with open(BIN_FILE, "w") as file:
        json.dump(st.session_state.deleted_tasks, file, indent=4)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "deleted_tasks" not in st.session_state:
    st.session_state.deleted_tasks = load_deleted_tasks()
if "show_bin" not in st.session_state:
    st.session_state.show_bin = False
if "auto_save" not in st.session_state:
    st.session_state.auto_save = False
if "selected_tasks" not in st.session_state:
    st.session_state.selected_tasks = set()

# UI Styling
st.markdown(
    """
    <style>
    .task-text {
        font-size: 22px;
        font-weight: bold;
        text-align: justify;
    }
    .task-completed {
        text-decoration: line-through;
        color: gray;
        font-size: 22px;
        font-weight: bold;
        text-align: justify;
    }
    .bin-container {
        position: fixed;
        top: 10px;
        right: 20px;
        z-index: 1000;
    }
    .popup {
        position: fixed;
        top: 50px;
        right: 20px;
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px gray;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Bin Icon in Right Corner
bin_placeholder = st.empty()
with bin_placeholder:
    if st.button("🗑️", key="open_bin", help="View Deleted Tasks"):
        st.session_state.show_bin = not st.session_state.show_bin

# Bin Pop-up for Deleted Tasks
if st.session_state.show_bin:
    with st.container():
        st.markdown('<div class="popup">', unsafe_allow_html=True)
        st.markdown('<h4>Deleted Tasks 🗑️ </h4>', unsafe_allow_html=True)
        for i, task in enumerate(st.session_state.deleted_tasks):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write("🗑️ " + task["task"])
            with col2:
                if st.button("♻️", key=f"restore_{i}", help="Restore Task"):
                    st.session_state.tasks.append(task)
                    del st.session_state.deleted_tasks[i]
                    if st.session_state.auto_save:
                        save_tasks()
                        save_deleted_tasks()
                    st.session_state.show_bin = False
        st.markdown('</div>', unsafe_allow_html=True)

# Main To-Do List
st.markdown('<h1 style="text-align:center;">To-Do List App 📝 </h1>', unsafe_allow_html=True)

# Add Task Input
new_task = st.text_input("Add a new task ✍️ ", "").strip()

if new_task:
    if new_task.lower() in [task["task"].lower() for task in st.session_state.tasks]:
        st.warning("⚠️ This task already exists!")
    else:
        st.session_state.tasks.append({"task": new_task, "completed": False})
        if st.session_state.auto_save:
            save_tasks()
        else:
            st.warning("Task added! Click 'Save Changes 💾 ' to save.")

# Display Tasks with Selection Feature
if st.session_state.tasks:
    st.markdown('<h3 style="text-align:center;">Tasks 📌 </h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        select_all = st.checkbox("Select All", key="select_all")
    with col2:
        if st.button("Delete Selected 🗑️ "):
            st.session_state.deleted_tasks.extend([st.session_state.tasks[i] for i in st.session_state.selected_tasks])
            st.session_state.tasks = [task for i, task in enumerate(st.session_state.tasks) if i not in st.session_state.selected_tasks]
            st.session_state.selected_tasks.clear()
            if st.session_state.auto_save:
                save_tasks()
                save_deleted_tasks()
            st.success("Selected tasks moved to bin!")

    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4 = st.columns([0.05, 0.6, 0.15, 0.15])
        with col1:
            if select_all:
                st.session_state.selected_tasks.add(i)
            selected = st.checkbox("", value=i in st.session_state.selected_tasks, key=f"select_{i}")
            if selected:
                st.session_state.selected_tasks.add(i)
            elif i in st.session_state.selected_tasks:
                st.session_state.selected_tasks.remove(i)

        with col2:
            task_class = "task-completed" if task["completed"] else "task-text"
            st.markdown(f'<p class="{task_class}">{task["task"]}</p>', unsafe_allow_html=True)

        with col3:
            if st.button("✔️", key=f"complete_{i}", help="Mark as Completed"):
                st.session_state.tasks[i]["completed"] = not st.session_state.tasks[i]["completed"]
                if st.session_state.auto_save:
                    save_tasks()

        with col4:
            if st.button("🗑️", key=f"delete_{i}", help="Move to Bin"):
                st.session_state.deleted_tasks.append(st.session_state.tasks[i])
                del st.session_state.tasks[i]
                if st.session_state.auto_save:
                    save_tasks()
                    save_deleted_tasks()

# Manual Save Button (Only when Auto-Save is OFF)
if not st.session_state.auto_save:
    if st.button("Save Changes 💾 "):
        save_tasks()
        save_deleted_tasks()
        st.success("Tasks saved successfully!")