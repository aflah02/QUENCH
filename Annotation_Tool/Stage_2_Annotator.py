import os
import streamlit as st
import yaml

# Specify the directory path
directory = 'Stage_1_Annotations/'
save_dir = 'Stage_2_Annotations/'

all_files = os.listdir(directory)
handled_files = os.listdir(save_dir)

pending_files = list(set(all_files) - set(handled_files))

idx = 0

print(idx)
print(handled_files)

st.write(f"Number of pending files: {len(pending_files)}")

file = pending_files[idx]
st.write(file)
yaml_file = open(directory + file, 'r')
parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
st.subheader('Question')
st.write(parsed_yaml_file['question'])
# st.subheader('Theme')
st.write(", ".join(parsed_yaml_file['themes']))
variable_specific_rationale = parsed_yaml_file['variable_specific_rationale']
variable_to_answer = parsed_yaml_file['variable_to_answer']
for var in parsed_yaml_file['variables']:
    st.subheader(f"{var} - {variable_to_answer[var]}")
    st.write(variable_specific_rationale[var])

col1, col2 = st.columns(2)

with col1:
    if st.button('Yes'):
        result = {
            'id': file,
            'indic': 'Yes'
        }
        with open(save_dir + file, 'w') as f:
            yaml.dump(result, f)
        st.rerun()

with col2:
    if st.button('No'):
        result = {
            'id': file,
            'indic': 'No'
        }
        with open(save_dir + file, 'w') as f:
            yaml.dump(result, f)
        st.rerun()