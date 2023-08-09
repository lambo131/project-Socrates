import streamlit as st
import time

class WebApp:
    def __init__(self):
        self.a = "a"
        self.b = "b"

@st.cache_data
def func(str):
    time.sleep(2)
    return str+"!"

if "app" not in st.session_state:
        st.session_state.app = WebApp()
        
app = WebApp()



st.title("this is the load document page")
st.write(func(st.text_input("input")))

if st.button("update"):
    pass

if st.button("save app"):
    app.a = 4

if st.button("save session app"):
    st.session_state.app.a = 4

if st.button("clear cache"):
    st.cache_resource.clear()
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()


st.write("app: " + str(app.a))
st.write("sesstion_app: " + str(st.session_state.app.a))


option = st.selectbox(
    'How would you like to be contacted?',
    ('1', '2', '3'))

if option == "1":
    st.text_input("url")
if option == "2":
    uploaded_file = st.file_uploader("Choose a file")
if option == "3":
    st.text_input("text")
st.write('You selected:', option)