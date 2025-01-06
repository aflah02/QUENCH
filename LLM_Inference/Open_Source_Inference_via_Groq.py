import os
from groq import Groq
import yaml
from tqdm import tqdm
import argparse
import random
import json
from dotenv import load_dotenv
load_dotenv()

argparser = argparse.ArgumentParser()
argparser.add_argument('--model_name', type=str, default='')
argparser.add_argument('--mode', type=str, default='')

MODEL_NAME = argparser.parse_args().model_name
MODE = argparser.parse_args().mode

print(f"model_name: {MODEL_NAME}")
print(f"mode: {MODE}")

if MODEL_NAME not in ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']:
    raise ValueError(f"model_name {MODEL_NAME} not supported, choose one of ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']")

if MODE not in ['normal', 'cot']:
    raise ValueError(f"mode {MODE} not supported, choose one of ['normal', 'cot']")

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

data_path = "../Data_Store"

question_files = os.listdir(data_path)

print(question_files[:5])

sys_prompt = "Consider yourself a participant in a quiz show where I am the quizmaster. I will ask you a question that can be from any general theme. You need to provide me with the correct answer."
cot_addition = " Let's think step by step."

if MODE == 'cot':
    if cot_addition not in sys_prompt:
        sys_prompt += cot_addition

system_prompt = {
    "role": "system",
    "content": sys_prompt,
}

answer_pred_preprompt = """The question can have multiple variables to answer, and you need to provide me with the answer for variable {}. Hence, use the following format strictly in your response: `The answer is <X answer>`. You lose points if you fail to follow the format."""
pred_rationale_preprompt = "The prediction for variable {} is {}, provide me with the rationale followed for your answer. Use the following format in your response: `The rationale is <rationale>`. You lose points if you fail to follow the format."
gold_rationale_preprompt = "The correct answer for the variable {} is {}, provide me with the rationale that can be followed to arrive at the answer. Use the following format in your response: `The rationale is <rationale>`. You lose points if you fail to follow the format."

ls_preds = []

ls_var_ans_preds = []
ls_var_rationale = []
ls_var_gold_rationales = []

for q_f in tqdm(question_files):
    with open(os.path.join(data_path, q_f), 'r') as f:
        data = yaml.safe_load(f)
        question = data['question']
        variables = data['variables']
        question_title = data['question_title']
        variable_to_answer = data['variable_to_answer']
        variable_specific_rationale = data['variable_specific_rationale']
        var_ans_preds = {}
        var_rationales = {}
        var_gold_rationales = {}
        for var in variables:
            var_ans_prompt = answer_pred_preprompt.format(var)
            var_ans_prompt += " " + question

            # Hit the API to get the prediction
            chat_history_for_variable_prediction = [system_prompt, {"role": "user", "content": var_ans_prompt}]

            api_response = client.chat.completions.create(
                messages=chat_history_for_variable_prediction,
                model=MODEL_NAME,
            )

            variable_prediction = api_response.choices[0].message.content


            var_pred_prompt = pred_rationale_preprompt.format(var, variable_prediction)
            var_pred_prompt += " " + question

            # Hit the API to get the gold answer
            chat_history_for_normal_rationale_prediction = [system_prompt, {"role": "user", "content": var_pred_prompt}]

            api_response = client.chat.completions.create(
                messages=chat_history_for_normal_rationale_prediction,
                model=MODEL_NAME,
            )

            normal_variable_rationale_prediction = api_response.choices[0].message.content

            var_gold_prompt = gold_rationale_preprompt.format(var, variable_to_answer[var])
            var_gold_prompt += " " + question

            # Hit the API to get the gold rationale
            chat_history_for_gold_rationale_prediction = [system_prompt, {"role": "user", "content": var_gold_prompt}]

            api_response = client.chat.completions.create(
                messages=chat_history_for_gold_rationale_prediction,
                model=MODEL_NAME,
            )

            gold_variable_rationale_prediction = api_response.choices[0].message.content

            # Uncomment for Debugging
            # print("VARIABLE ANSWER PROMPT")
            # print(var_ans_prompt)
            # print("-------------------")
            # print("VARIABLE PREDICTION")
            # print(variable_prediction)
            # print("-------------------")
            # print("VARIABLE RATIONALE PROMPT")
            # print(var_pred_prompt)
            # print("-------------------")
            # print("NORMAL VARIABLE RATIONALE PREDICTION")
            # print(normal_variable_rationale_prediction)
            # print("-------------------")
            # print("GOLD VARIABLE RATIONALE PROMPT")
            # print(var_gold_prompt)
            # print("-------------------")
            # print("GOLD VARIABLE RATIONALE PREDICTION")
            # print(gold_variable_rationale_prediction)

            var_ans_preds[var] = variable_prediction
            var_rationales[var] = normal_variable_rationale_prediction
            var_gold_rationales[var] = gold_variable_rationale_prediction

        ls_var_ans_preds.append(var_ans_preds)
        ls_var_rationale.append(var_rationales)
        ls_var_gold_rationales.append(var_gold_rationales)

        ls_preds.append({q_f: {'ls_var_ans_preds': var_ans_preds, 'ls_var_rationale': var_rationales, 'ls_var_gold_rationales': var_gold_rationales}})

# write ls_preds to a jsonl file

with open(f'Saves/ls_preds_{MODEL_NAME}_{MODE}.jsonl', 'w') as f:
    for item in ls_preds:
        f.write(json.dumps(item) + "\n")