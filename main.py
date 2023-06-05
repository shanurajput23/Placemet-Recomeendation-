# <==== Importing Dependencies ====>

import os
import pickle
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

# <==== Code starts here ====>

# class course:
#     def __init__(self, name, url):
#         self.name = name
#         self.url = url

courses_list = pickle.load(open('./courses.pkl', 'rb'))
similarity = pickle.load(open('./similarity.pkl', 'rb'))

menu = ["Course Recommendation", "Placement Recommendation"]
choice = st.sidebar.selectbox("Menu", menu)

def recommend_course(course):
    index = courses_list[courses_list['course_name'] == course].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    course_names = []
    course_urls = []
    cos_similarity = []
    # print(distances)
    for i in distances[1:21]:
        course_name = courses_list.iloc[i[0]].course_name
        course_url = courses_list.iloc[i[0]]['Course URL']
        course_names.append(course_name)
        course_urls.append(course_url)
        cos_similarity.append(i[1])
        # recommended_course_names.append(course(course_name, course_url))

    recommended_courses = pd.DataFrame({
        "Course Name": course_names,
        "Course URL": course_urls,
        "Cosine Similarity": cos_similarity
    })
    return recommended_courses

def highlight_cols(x):
    #copy df to new - original data are not changed
    df = x.copy()
    #select all values to default value - red color
    df.loc[:,:] = 'background-color: white'
    return df
from PIL import Image

if choice == 'Course Recommendation':
    st.markdown(
        f"""
             <style>
             .stApp {{
                 background-image: url("https://images.shiksha.com/mediadata/images/1590388345phpAtPITp.png");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
        unsafe_allow_html=True
    )
    st.markdown("<h2 style='text-align: center; color: blue;'>Course Recommendation System</h2>",
                unsafe_allow_html=True)
    st.markdown(
        "<h4 style='text-align: center; color: black;'>Find similar courses </h4>",
        unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: black;'></h4>",
                unsafe_allow_html=True)

    course_list = courses_list['course_name'].values
    selected_course = st.selectbox(
        "Type or select a course you like :",
        courses_list
    )

    if st.button('Show Recommended Courses'):
        st.write("Recommended Courses based on your interests are :")
        recommended_course_names = recommend_course(selected_course)
        st.table(recommended_course_names.style.apply(highlight_cols, axis=None))
        # st.text(recommended_course_names[0].name)
        # st.text(recommended_course_names[1])
        # st.text(recommended_course_names[2])
        # st.text(recommended_course_names[3])
        # st.text(recommended_course_names[4])
        # st.text(recommended_course_names[5])
        # st.text(" ")
        st.markdown(
            "<h6 style='text-align: center; color: red;'></h6>",
            unsafe_allow_html=True)
else:
    jobs_list = pd.read_hdf('models/jobs.hdf5', 'jobs', 'r')
    # similarity = pickle.load(open('./models/jobs-similarity.pkl', 'rb'))
    import h5py

    with h5py.File('models/jobs.hdf5', 'r') as f:
        dset = f['similarity']
        similarity = dset


        def recommend_job(job):
            index = jobs_list[jobs_list['job_post'] == job].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            job_names = []
            company_names = []
            cos_similarity = []
            posted_on = []
            # print(distances)
            for i in distances[1:21]:
                job_name = jobs_list.iloc[i[0]]['job_post']
                company = jobs_list.iloc[i[0]]['company']
                posted = jobs_list.iloc[i[0]]['posted_on']
                job_names.append(job_name)
                company_names.append(company)
                cos_similarity.append(i[1])
                posted_on.append(posted)
                # recommended_course_names.append(course(course_name, course_url))

            recommended_courses = pd.DataFrame({
                "Job": job_names,
                "Company": company_names,
                "Posted On": posted_on,
                "Cosine Similarity": cos_similarity,
            })
            return recommended_courses


        st.markdown(
            f"""
                     <style>
                     .stApp {{
                         background-image: url("https://images.shiksha.com/mediadata/images/1590388345phpAtPITp.png");
                         background-attachment: fixed;
                         background-size: cover
                     }}
                     </style>
                     """,
            unsafe_allow_html=True
        )
        st.markdown("<h2 style='text-align: center; color: blue;'>Placement Recommendation System</h2>",
                    unsafe_allow_html=True)
        st.markdown(
            "<h4 style='text-align: center; color: black;'>Find similar placements </h4>",
            unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: black;'></h4>",
                    unsafe_allow_html=True)

        job_list = jobs_list['job_post'].values
        selected_course = st.selectbox(
            "Type or select a job you like :",
            jobs_list
        )

        if st.button('Show Recommended Placements'):
            st.write("Recommended Placement based on your interests are :")
            recommended_course_names = recommend_job(selected_course)
            st.table(recommended_course_names.style.apply(highlight_cols, axis=None))
            # st.text(recommended_course_names[0].name)
            # st.text(recommended_course_names[1])
            # st.text(recommended_course_names[2])
            # st.text(recommended_course_names[3])
            # st.text(recommended_course_names[4])
            # st.text(recommended_course_names[5])
            # st.text(" ")

# <==== Code ends here ====>
