
import streamlit as st
import yaml
import os

st.set_page_config(
    page_title="Main",
    page_icon="🎯",
    initial_sidebar_state='collapsed'
)

def saveResults(question, themes, question_source, question_title, variable_specific_rationale, variables, metadata, variable_to_answer):
    print(question)
    print(themes)
    print(question_source)
    print(question_title)
    print(variable_specific_rationale)
    print(variables)
    print(metadata)
    print(variable_to_answer)
    # Save Results to a json file named after the question title
    savingJson = {
        "question": question,
        "themes": themes,
        "question_source": question_source,
        "question_title": question_title,
        "variable_specific_rationale": variable_specific_rationale,
        "variables": variables,
        "metadata": metadata,
        "variable_to_answer": variable_to_answer
    }
    with open(f"Stage_1_Annotations/{question_title}.yml", "w") as f:
        yaml.dump(savingJson, f, default_flow_style=False)
    
# read themes.txt
with open("themes.txt", "r") as f:
    themes = f.readlines()

themes = list(set(themes))

# Sort themes
themes.sort()

st.title("Annotation Tool")

question_source = st.text_input("Enter the source of the question:")

question_title = st.text_input("Enter the title of the question:")

current_questions = os.listdir("Stage_1_Annotations")
if question_title + ".yml" in current_questions:
    st.warning("Question title already in use. Please check the Stage_1_Annotations folder for the question.")

metadata = st.text_input("Enter the metadata of the question (if any):")

# Create a text input field and store the user's input in a variable
user_input = st.text_area("Enter The Question:", height=100)

# Choose themes
# themes = st.multiselect("Choose Themes:", themes)
#checkbox for each theme divide into 3 columns
st.write("Choose Themes:")
col1, col2, col3 = st.columns(3)
selection_tracker = {}
for i, theme in enumerate(themes):
    if i % 3 == 0:
        cb = col1.checkbox(theme)
        selection_tracker[theme] = cb
    elif i % 3 == 1:
        cb = col2.checkbox(theme)
        selection_tracker[theme] = cb
    else:
        cb = col3.checkbox(theme)
        selection_tracker[theme] = cb

variables_to_id = st.text_input("Enter comma separated variables (e.g. X, Y, Z)")

variables = variables_to_id.split(",")

if len(variables) > 0 and variables[0] != "":

    # remove spaces from variable names
    variables = [var.strip() for var in variables]

    variable_to_answer = {}

    if variables:
        # Enter correct answers for the variables
        for var in variables:
            ans = st.text_input(f"Enter correct answer for {var}:")
            variable_to_answer[var] = ans

    # Write Rationale

    variable_specific_rationale = {}

    for var in variables:
        variable_specific_rationale[var] = st.text_area(f"Enter Rationale for {var}:", height=100)

    themes_selected = [theme for theme in selection_tracker if selection_tracker[theme]]

    enable_submit = question_title + ".yml" not in current_questions and len(themes_selected) != 0
    for var in variables:
        enable_submit = enable_submit and variable_to_answer[var] != "" and variable_specific_rationale[var] != "" 

    # Submit Button
    st.button("Submit", on_click=lambda: saveResults(user_input, themes_selected, question_source, question_title, variable_specific_rationale, variables, metadata, variable_to_answer),
                disabled=not enable_submit)
