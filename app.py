"""

"""
from processing import Resume_aid, convert_pdf2docx
import streamlit as st
import base64
import os
import logging
import fitz
import pandas as pd
from PIL import Image



df = pd.read_csv('2019_free_title_data.csv')


st.set_page_config(
   page_title="Resume Architect",
   page_icon="✅",
   layout="wide",
)
st.title("Resume Architect")



def st_display_pdf(pdf_file, col):

    with open(pdf_file,"rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="500" height="500" type="application/pdf"></iframe>'
        col.markdown(pdf_display, unsafe_allow_html=True)


def save_uploadedfile(uploadedfile):
    
     with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     #return cv_score.success("File Saved: {} to tempDir".format(uploadedfile.name))



def file_check(file_uploaded, col):

    if file_uploaded is not None:
        file_details = {"FileName":file_uploaded.name,"FileType":file_uploaded.type}

        file_path = os.path.join("tempDir",file_uploaded.name)

        save_uploadedfile(file_uploaded)

        if file_details["FileType"]!="application/pdf":
            st.error("Please enter correct file type.")
    else:
        st.error("Upload your resume")

def highlighted_pdf(file_path, terms, resume_col):
    """
    Highlights marked keywords from Job description to your CV.
    """
    doc_highlight = fitz.open(file_path)

    for high_word in terms:
        for page in doc_highlight:
            ### SEARCH
            text_hi = high_word
            text_instances = page.searchFor(text_hi)

            ### HIGHLIGHT
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
                highlight.update()

    doc_highlight.save("./" + file_path, garbage=4, deflate=True, clean=True)
    st_display_pdf("./" + file_path, resume_col)




def on_process(job_c, file_uploaded, resume_col, title):
    """
    Handles the backend processing of the file.
    """
    for i in range(len(df)):
        if df['title'][i]== title:
            related_titles= df.values.tolist()[i][10:20]
            st.info("Related Jobs (Top 8)")
            st.write(related_titles)
    try:
        if job_c is not None and file_uploaded is not None:
            

            file_path = os.path.join("tempDir",file_uploaded.name)
            convert_pdf2docx(file_path, file_path.replace(".pdf",".docx"))

            res_uploaded = Resume_aid()
            res_uploaded.resume_processing(file_path.replace(".pdf",".docx"))

            res_uploaded.job_desc_processing(job_c)

            cv_score.success(f"Resume match = {str(res_uploaded.cosine_score())}%")

            res_uploaded.phrase_matching()
            terms_highlight = res_uploaded.count_match()

            highlighted_pdf(file_path, terms_highlight, resume_col)

            job_score.table(res_uploaded.display_match())
            cv_score.warning("Phrases and Scores from Job Description (Top 10)")
            cv_score.write(res_uploaded.keyword_score_job())
            job_score.warning("Phrases and Scores from your Resume (Top 10)")
            job_score.write(res_uploaded.keyword_score_cv())
            st.info("Importance and Similarity Scores match (Top 20)")
            st.table(res_uploaded.importance_score())


           

    except Exception as ex:
        logging.error(ex)


x = open('job.txt','r')
text = x.read()
titles = text.split(',')

title = st.selectbox('Your current/potential job title:',(titles))
st.write('You selected:', title)

Resume_user = st.file_uploader('Upload your resume:', type=["pdf"])


job_des_col, resume_col = st.columns(2)

job_score, cv_score = st.columns(2)

job_content = job_des_col.text_area("Enter the job description:", height=400)

if job_des_col.button("Analyse"):
    if job_content!="":
        file_check(Resume_user, resume_col)
        on_process(job_content, Resume_user, resume_col, title)
        
    else:
        st.error("Please enter job description.")

try:
    dir = "./tempDir/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
except Exception:
    logging.warning("Not able to delete the files.")
