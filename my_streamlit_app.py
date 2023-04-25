import streamlit as st
from langchain import LLMChain, OpenAI, PromptTemplate
from PyPDF2 import PdfReader



# Set up OpenAI API key
# 
openai_api_key_toml = st.secrets["secrets"]["api_key"]



# Set up LangChain model
model = OpenAI(openai_api_key=openai_api_key_toml, temperature=0)


template = """
As a cv censor AI, my task is to censor a cv wit regards to different personal endicatiors. As an example I will censor gender, age, sexual orientation, ethnicity or otherwise revealing things that could make the reader descriminate the person writing the application including name and email
As an example you do like this: "test@email.com" to "********"

CV Context ---
{application}
-----

Redacted CV: 
"""

prompt = PromptTemplate(input_variables=["application"], template=template)
chain = LLMChain(llm=model, prompt=prompt)

# Set up app layout
st.set_page_config(page_title="A fair chance", page_icon=":guardsman:", layout="wide")
st.title("A fair chance")

st.write(
    """
    Our application filters out personal information such as age, sex, gender, and religion, allowing for a fair and unbiased assessment of each candidate's qualifications. By removing these potentially discriminatory factors, employers can focus solely on a candidate's skills and experience, resulting in a more diverse and inclusive workforce. With our application, we are committed to creating equal opportunities for all individuals, regardless of their personal background.
    """
)

col1, col2 = st.columns(2)

# Get user input
with col1:
    st.header("Your resume")
    input_text = st.text_area("Enter your resume here")

    uploaded_file = st.file_uploader("Or upload your resume (PDF only)", type="pdf")

    if uploaded_file is not None:
        pdf_file = PdfReader(uploaded_file)
        input_text = "\n".join([page.extract_text() for page in pdf_file.pages])

    if input_text == "":
        st.warning("Please enter or upload your resume")

    if st.button("Submit"):
        if input_text:
            # Call LangChain model
            with st.spinner("Processing your resume..."):
                res = chain.run(application=input_text)

            # Display filtered text
            with col2:
                st.header("The filtered resume")
                st.text_area("The outcome", value=res, height=600)
