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
@inproceedings{khan-etal-2025-quench,
    title = "{QUENCH}: Measuring the gap between {I}ndic and Non-{I}ndic Contextual General Reasoning in {LLM}s",
    author = "Khan, Mohammad Aflah  and
      Yadav, Neemesh  and
      Masud, Sarah  and
      Akhtar, Md. Shad",
    editor = "Rambow, Owen  and
      Wanner, Leo  and
      Apidianaki, Marianna  and
      Al-Khalifa, Hend  and
      Eugenio, Barbara Di  and
      Schockaert, Steven",
    booktitle = "Proceedings of the 31st International Conference on Computational Linguistics",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.coling-main.303/",
    pages = "4493--4509",
    abstract = "The rise of large language models (LLMs) has created a need for advanced benchmarking systems beyond traditional setups. To this end, we introduce QUENCH, a novel text-based English Quizzing Benchmark manually curated and transcribed from YouTube quiz videos. QUENCH possesses masked entities and rationales for the LLMs to predict via generation. At the intersection of world knowledge, geographical context, and common sense reasoning, QUENCH helps assess world knowledge and deduction capabilities of LLMs via a zero-shot, open-domain quizzing setup. We perform an extensive evaluation on 7 LLMs and 4 metrics, investigating the influence of model size, prompting style, geographical context, and gold-labeled rationale generation. The benchmarking concludes with an error analysis of various types of generative errors to which the LLMs are prone."
}
```
