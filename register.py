
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd 

st.title("CAD Registration form")
st.markdown("Enter Your Details Below")

conn = st.connection("gsheets",type=GSheetsConnection)

existing_data=conn.read(worksheet="Cad-form",usecols=list(range(9)),ttl=5)
existing_data=existing_data.dropna(how="all")


GENDER_TYPES ={
    "MALE",
    "FEMALE",
}

with st.form(key="Register-form"):
    Studentname=st.text_input(label="Student Name*",)
    Rollno=st.text_input(label="Rollno*")
    Gender=st.selectbox("Gender",options=GENDER_TYPES,index=None)
    Dob=st.date_input(label="DOB")
    cgpa=st.slider("CGPA Obtained",0.0,5.0,10.0)
    Rollno1=st.text_input(label="10th Rollno*")
    Rollno2=st.text_input(label="Inter Rollno*")
    abcid=st.text_input(label="ABC id")
    phno=st.text_input(label="Ph No")

    st.markdown("**Required*")

    submit_button=st.form_submit_button(label="submit")


    if submit_button:
        if not Studentname or not Rollno:
            st.warning("ensure all mandetory field are filled")
            st.stop()
        elif existing_data["Name"].str.contains(Studentname).any():
            st.warning("A student with this name already exist")
            st.stop()
        else:
            student_data=pd.DataFrame(
                [
                    {
                        "Name":Studentname,
                        "Roll No":Rollno,
                        "Gender":Gender,
                        "CGPA":cgpa,
                        "DOB":Dob,
                        "10th Rollno":Rollno1,
                        "Inter Rollno":Rollno2,
                        "ABC Id":abcid,
                        "Ph No":phno,

                    }
                ]
            )

            updated_df=pd.concat([existing_data,student_data],ignore_index=True)

            conn.update(worksheet="Cad-form",data=updated_df)

            st.success("YOUR DETAILS HAVE BEEN SUCCESSFULLY REGITERED")

            

            