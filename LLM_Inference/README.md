# LLM Inference

This folder contains scripts to perform inference with various models on the QUENCH dataset.

We support two types of models: **open-weight** and **closed-source**.  
- For **closed-source models**, we conduct experiments with Gemini (`Gemini-1.5-Flash`) and OpenAI (`GPT-3.5-Turbo` & `GPT-4-Turbo`).  
- For **open-weight models**, we use `Meta-Llama-3-70B-Instruct`, `Meta-Llama-3-8B-Instruct`, `Mixtral-8x7B-Instruct-v0.1`, and `Gemma-1.1-7B-Instruct` via the Groq API.

### Note:
The experiments in this paper were conducted in early 2024, using the best models available at the time. Since then, newer models have been released, but this codebase should require minimal or no modifications to support them. If you encounter any issues, feel free to raise an issue.  
Keep in mind that `GPT-3.5-Turbo` and `GPT-4-Turbo` are continually updated. At the time of these experiments:  
- `GPT-4-Turbo` referred to `gpt-4-turbo-2024-04-09`.  
- `GPT-3.5-Turbo` referred to `gpt-3.5-turbo-0125`.  

---

## Installation

Install the required dependencies using pip:

```bash
pip install google-generativeai PyYAML openai groq
```

---

## Usage

### Inference for Open-Weight Models

1. Set the `GROQ_API_KEY` environment variable using an API Key from [groq.com](https://groq.com).
2. Run the following command:

   ```bash
   python Open_Weight_Inference_via_Groq.py --model_name MODEL_NAME --mode MODE
   ```

   **Parameters**:  
   - `MODEL_NAME`: Choose from:  
     `['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']`  
   - `MODE`: Choose from:  
     `['normal', 'cot']`

   **Adding New Models**:  
   To add support for new Groq-compatible models, include them in the condition check at **Line 21** of the script.

---

### Inference for Closed-Source Models

1. Set the `GEMINI_API_KEY` and `OPENAI_API_KEY` environment variables.
2. Run the following command:

   ```bash
   python Closed_Source_Inference.py --endpoint ENDPOINT --model_name MODEL_NAME --mode MODE
   ```

   **Parameters**:  
   - `MODEL_NAME`: Choose from:  
     `['gemini-1.5-flash', 'gpt-3.5-turbo', 'gpt-4-turbo']`  
   - `MODE`: Choose from:  
     `['normal', 'cot']`  
   - `ENDPOINT`: Choose from:  
     `['openai', 'gemini']`

   **Note**: You can also use other models supported by the respective Python SDKs of these libraries.