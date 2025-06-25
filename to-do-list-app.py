import streamlit as st
import pandas as pd
import speech_recognition as sr

# Background styling
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: url("https://images.unsplash.com/photo-1619532117965-c271b66c9c8d?auto=format&fit=crop&w=1740&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .main {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 16px;
            padding: 30px;
            margin-top: 30px;
            color: white;
        }
        h1 {
            color: #00ffe5;
            text-align: center;
            text-shadow: 0 0 10px #00ffe5;
        }
        .stButton > button {
            background-color: #ff00c8;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            box-shadow: 0 0 10px #ff00c8;
        }
        .stTextInput>div>div>input,
        .stSelectbox>div>div {
            background-color: #222;
            color: white;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Login system
def login():
    st.markdown("## Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "archana123" and password == "125145":
            st.session_state.logged_in = True
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# Initialize task list
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Function to add a task
def add_task(task_name, priority, status):
    new_task = {
        'Task Name': task_name,
        'Priority': priority,
        'Status': status
    }
    st.session_state.tasks.append(new_task)

# Voice input
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
        return ""
    except sr.RequestError:
        st.error("Speech service error")
        return ""

# Title
st.title("TaskFlow: A To-Do List Application")

# Voice task section
st.subheader("Add Task via Voice")
if st.button("🎤 Use Voice to Add Task Name"):
    task_name = recognize_speech()
    if task_name:
        priority = st.selectbox("Select Priority for Voice Task", ["Low", "Medium", "High"], key="voice_priority")
        status = st.selectbox("Select Status for Voice Task", ["To-Do", "In Progress", "Done"], key="voice_status")
        if st.button("Add Voice Task"):
            add_task(task_name, priority, status)
            st.success("Voice task added!")

# Form to manually add task
with st.form("create_task"):
    task_name = st.text_input("Task Name")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["To-Do", "In Progress", "Done"])
    submitted = st.form_submit_button("Add Task")
    if submitted:
        add_task(task_name, priority, status)
        st.success("Task added successfully!")

# Display and manage tasks
if st.session_state.tasks:
    st.write("### Your Tasks:")
    task_df = pd.DataFrame(st.session_state.tasks)
    edited_df = st.data_editor(task_df)

    if st.button("Update Task"):
        updated_task_index = st.number_input("Enter task index to update", min_value=0, max_value=len(st.session_state.tasks) - 1)
        updated_task_name = edited_df.iloc[updated_task_index]['Task Name']
        updated_priority = edited_df.iloc[updated_task_index]['Priority']
        updated_status = edited_df.iloc[updated_task_index]['Status']
        st.session_state.tasks[updated_task_index] = {
            'Task Name': updated_task_name,
            'Priority': updated_priority,
            'Status': updated_status
        }
        st.success("Task updated successfully!")

    task_index_to_delete = st.number_input("Enter task index to delete", min_value=0, max_value=len(st.session_state.tasks) - 1)
    if st.button("Delete Task"):
        del st.session_state.tasks[task_index_to_delete]
        st.success("Task deleted successfully!")

else:
    st.write("No tasks available. Please add a task!")

st.markdown('</div>', unsafe_allow_html=True)
