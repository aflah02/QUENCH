from argparse import ArgumentParser
import yaml
from time import sleep
from tqdm import tqdm
import os
import google.generativeai as genai
from openai import OpenAI
import json

def query_gemini(prompt, preprompt=''):
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = preprompt + "\n" + prompt

    response = gemini_model.generate_content(prompt, safety_settings={
        'HARASSMENT': 'block_none', 'dangerous': 'block_none', 'SEXUALLY_EXPLICIT': 'block_none', 'HATE_SPEECH': 'block_none'
    })

    return response.text

def query_gpt(prompt, preprompt='', model="gpt-3.5-turbo"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    prompt = preprompt + "\n" + prompt

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model=model,
    )

    return completion.choices[0].message.content


endpoints = ['openai', 'gemini']
exp_types = ['normal', 'cot']

parser = ArgumentParser()
parser.add_argument('--endpoint', type=str, default='openai')
parser.add_argument('--exp_type', type=str, default='normal')
parser.add_argument('--model_type', type=str, default='gpt3.5')
parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo')

def run_exp(endpoint, model_name, exp_type='normal'):
    print(f"Running with model {model_name} on endpoint {endpoint}")

    if not os.path.exists('Saves/'):
        print("Creating Saves directory")
        os.makedirs('Saves/')

    preprompt = ''

    ls_preds = []
    ls_var_ans_preds = []
    ls_var_rationale = []
    ls_var_gold_rationales = []

    for file in tqdm(os.listdir('../Data_Store/')):

        with open(f'../Data_Store/{file}', 'r') as f:
            data = yaml.safe_load(f)

        question = data['question']
        variables = data['variables']
        gold_answers = data['variable_to_answer']

        var_ans_preds = {}
        var_rationales = {}
        var_gold_rationales = {}

        for variable in variables:
            preprompt = "Consider yourself a participant in a quiz show where I am the quizmaster. I will ask you a question that can be from any general theme. You need to provide me with the correct answer. "
            answer_pred_preprompt = "The question can have multiple variables to answer, and you need to provide me with the answer for variable {}. Hence, use the following format strictly in your response: `The answer is <X answer>`. You lose points if you fail to follow the format."
            pred_rationale_preprompt = "The prediction for variable {} is {}, provide me with the rationale followed for your answer. Use the following format in your response: `The rationale is <rationale>`. You lose points if you fail to follow the format."
            gold_rationale_preprompt = "The correct answer for the variable {} is {}, provide me with the rationale that can be followed to arrive at the answer. Use the following format in your response: `The rationale is <rationale>`. You lose points if you fail to follow the format."
        
            if exp_type == 'cot':
                preprompt += " Let's think step by step."

            if endpoint == 'openai':
                answer_pred = query_gpt(question, preprompt + answer_pred_preprompt.format(variable), model_name)
                # answer_pred = answer_pred.replace('The answer is ', '')
                sleep(1)
                pred_rationale = query_gpt(question, preprompt + pred_rationale_preprompt.format(variable, answer_pred), model_name)
                sleep(1)
                gold_rationale = query_gpt(question, preprompt + gold_rationale_preprompt.format(variable, gold_answers[variable]), model_name)
                sleep(1)
            
            if endpoint == 'gemini':
                answer_pred = query_gemini(question, preprompt + answer_pred_preprompt.format(variable))
                sleep(5) # Long sleep to avoid rate limiting in Gemini
                # answer_pred = answer_pred.replace('The answer is ', '')
                pred_rationale = query_gemini(question, preprompt + pred_rationale_preprompt.format(variable, answer_pred))
                sleep(5)
                gold_rationale = query_gemini(question, preprompt + gold_rationale_preprompt.format(variable, gold_answers[variable]))
                sleep(5)

            var_ans_preds[variable] = answer_pred
            var_rationales[variable] = pred_rationale
            var_gold_rationales[variable] = gold_rationale
    
        ls_var_ans_preds.append(var_ans_preds)
        ls_var_rationale.append(var_rationales)
        ls_var_gold_rationales.append(var_gold_rationales)

        ls_preds.append({
            file: {
                'ls_var_ans_preds': var_ans_preds,
                'ls_var_rationale': var_rationales,
                'ls_var_gold_rationales': var_gold_rationales
            }
        })

    with open(f'Saves/ls_preds_{model_name}_{exp_type}.yaml', 'w') as f:
        for pred in ls_preds:
            f.write(json.dumps(pred) + '\n')
        
if __name__ == '__main__':
    args = parser.parse_args()
    
    if args.endpoint not in endpoints:
        raise ValueError(f"Invalid endpoint {args.endpoint}. Must be one of {endpoints}")
    
    if args.exp_type not in exp_types:
        raise ValueError(f"Invalid experiment {args.exp_type}. Must be one of {exp_types}")
    
    run_exp(args.endpoint, args.model_name, exp_type=args.exp_type)
