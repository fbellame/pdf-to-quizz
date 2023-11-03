import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True
    
def transform(input_list):
    new_list = []
    for item in input_list:
        for key in item:
            if 'question' in key:
                question_dict = {}
                question_dict['question'] = item[key]
                question_dict['A'] = item['A']
                question_dict['B'] = item['B']
                question_dict['C'] = item['C']
                question_dict['D'] = item['D']
                question_dict['reponse'] = item['reponse']
                new_list.append(question_dict)
    return new_list      