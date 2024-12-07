# Data Leakage Testing (Appendix E)

This document outlines the two-phase approach used to test for potential data leakage from source datasets into popular pretraining datasets.

## Phase 1: Checking for presence of data sources in pretraining corpora

We leverage the user interface available at [`https://wimbd.apps.allenai.org/`](https://wimbd.apps.allenai.org/) to analyze whether the sources of the data were present in widely used pretraining datasets. This phase focuses on identifying the origins of data rather than checking individual samples for contamination.

## Phase 2: Checking for exact match count in pretraining corpora

Using the Infinigram API, we perform automated checks to identify contamination between the source datasets and popular pretraining datasets. You can execute this phase using the `Phase_2.ipynb` notebook. 

## Pretraining Datasets Tested

We perform data leakage testing against the following pretraining datasets:

- **Dolma**
- **RedPajama**
- **Pile**
- **C4**

