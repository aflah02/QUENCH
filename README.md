# QUENCH: Measuring the gap between Indic and Non-Indic Contextual General Reasoning in LLMs

This is the official repository for the paper ["QUENCH: Measuring the gap between Indic and Non-Indic Contextual General Reasoning in LLMs"](https://www.arxiv.org/abs/2412.11763). 

Accepted at `The 31st International Conference on Computational Linguistics (COLING 2025)`

# Data - 

- The Core Data is present under `Data_Store/`
- The Annotations for whether the question requires Indic context or not is present under `isIndicAnnotations/`
- Both folders contain same file names allowing you to easily match across the two folders

# Annotation Tool - 

Instructions to run our 2 stage annotation process alongside the tool are present under `Annotation_Tool/`

# LLM Inference - 

Scripts to rerun the experiments using Groq, OpenAI and Gemini APIs are present under `LLM_Inference/`. The README present in the folder spells out the library requirements for each experiment.

# Evaluation - 

Scripts to perform automatic as well as GEval style evaluations are present under `Evaluation/`.

# Data Leakage Analysis - 

We also extensively evaluate for contamination of our benchmark dataset into public pretraining datasets. You can find our scripts under `Data_Leakage_Analysis`.

# Results for Plots - 

You can find our aggregated results under `Results/`. These results are used in the tables as well as the plots.

---

If you find the dataset or code useful, please don't forget to cite us!

```
@misc{khan2024quenchmeasuringgapindic,
      title={QUENCH: Measuring the gap between Indic and Non-Indic Contextual General Reasoning in LLMs}, 
      author={Mohammad Aflah Khan and Neemesh Yadav and Sarah Masud and Md. Shad Akhtar},
      year={2024},
      eprint={2412.11763},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.11763}, 
}
```