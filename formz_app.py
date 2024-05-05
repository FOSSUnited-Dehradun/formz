import streamlit as st
from supabase import create_client, Client


# Page Configurations
st.set_page_config(
        page_title="FOSS United Dehradun",
        page_icon="assets/foss-ddn.png",
        # layout="wide"
        
    )


###################### SUPABASE CONFIGURATION ######################

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()



def upload_details_to_supabase(details):
    table_name = "Volunteers"
    response = supabase.table(table_name).insert(details).execute()
    if response.data is None:
        st.error(f'Error: {response.error}')
    else:
        st.success('Details uploaded successfully')

# Outer Form Congiguration
st.image('assets/foss-ddn.png')
st.header('FOSS United Dehradun Volunteer Form')


# Initialize the session state variable
if 'page' not in st.session_state:
    st.session_state['page'] = 'form'

# Show the form page
if st.session_state['page'] == 'form':
    form=st.form(key='my_form')
    
    
    form_name=form.text_input('What should we call you? *')
    
    form_college=form.text_input('Which University are you currently enrolled in? *')
    
    form_userBio=form.text_area('Tell us about yourself and why you want to Volunteer with us? *')
    
    form_roleOptions =form.multiselect(
        "What Positions would you like to Volunteer for? *",
        ["Tech", "Social Media", "Designing", "Editing "],
        default=None)
    
    txt=form.write('Schedule a meeting with us')
    form_embed=form.markdown("""
    <iframe src="https://cal.com/infamous/foss-united-dehradun-volunteer" width="670" height="600"></iframe>
    """, unsafe_allow_html=True)

    if form.form_submit_button('Submit'):
        if form_name and form_college and form_userBio and form_roleOptions:
            data={
                "name":form_name,
                "university":form_college,
                "description":form_userBio,
                "positions":form_roleOptions
            }
            st.success("Form submitted successfully.")
           
            st.session_state['page'] = 'success'
            upload_details_to_supabase(data)
            st.rerun()
           
        else:
            # One or more fields are empty, show an error message
            st.error("Please fill in all fields before submitting.")

# Show the success page
elif st.session_state['page'] == 'success':
    st.write("Thank you for your submission!")
