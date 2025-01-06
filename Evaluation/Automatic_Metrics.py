from nltk.translate.bleu_score import corpus_bleu, sentence_bleu
from rouge import Rouge
from datasets import load_metric
import numpy as np

def get_bleu_score(references, hypotheses, return_all_scores=False):
    bleu = np.empty((len(hypotheses), 2))
    for i,hyp in enumerate(hypotheses):
        bleu_ref = np.empty(len(references[i]))
        for j,ref in enumerate(references[i]):
            if len(ref) == 0 and len(hyp) == 0:
                bleu_ref[j] = 1.0
            elif len(ref) == 0 and len(hyp) != 0:
                bleu_ref[j] = 0.0
            elif len(ref) != 0 and len(hyp) == 0:
                bleu_ref[j] = 0.0
            else:
                bleu_ref[j] = sentence_bleu([ref], hyp, weights=(0.5, 0.5))
        bleu[i] = [np.max(bleu_ref), np.average(bleu_ref)]

    if return_all_scores:
        return bleu
    else:
        return np.average(bleu, axis=0)

def get_rouge_scores(references, hypotheses, return_all_scores=False):
    rouge_scores = np.empty((len(hypotheses), 2, 3))
    rouge = Rouge(metrics=['rouge-l'])

    for i, hyp in enumerate(hypotheses):
        ref_scores = np.empty((len(references[i]), 3))
        for j, ref in enumerate(references[i]):
            if len(ref) == 0 and len(hyp) == 0:
                scores = [{'rouge-l': {'f': 1.0, 'p': 1.0, 'r': 1.0}}]
            elif len(ref) == 0 and len(hyp) != 0:
                scores = [{'rouge-l': {'f': 0.0, 'p': 0.0, 'r': 0.0}}]
            elif len(ref) != 0 and len(hyp) == 0:
                scores = [{'rouge-l': {'f': 0.0, 'p': 0.0, 'r': 0.0}}]
            else:
                scores = rouge.get_scores(hyp, ref)
            ref_scores[j, 0] = scores[0]['rouge-l']['p']
            ref_scores[j, 1] = scores[0]['rouge-l']['r']

            if ref_scores[j, 0] + ref_scores[j, 1] == 0.0:
                ref_scores[j, 2] = 0.0
            elif np.isnan(ref_scores[j, 0]):
                ref_scores[j, 2] = np.nan
            else:
                ref_scores[j, 2] = 2 * ((ref_scores[j, 0] * ref_scores[j, 1]) / \
                                        (ref_scores[j, 0] + ref_scores[j, 1]))

        max_j = np.argmax(ref_scores, axis=0)[2]
        rouge_scores[i,0,:] = ref_scores[max_j]
        rouge_scores[i,1,:] = np.average(ref_scores, axis=0)

    if return_all_scores:
        return rouge_scores
    else:
        return np.average(rouge_scores, axis=0)

def get_bert_score(bert_scores, hypotheses, references, return_all_scores=False):
    for i,_ in enumerate(hypotheses):
        if len(hypotheses[i]) == 0:
                if len(references[i]) == 1:
                    if len(references[i][0]) == 0:
                        bert_scores['precision'][i] = 1.0
                        bert_scores['recall'][i] = 1.0
                        bert_scores['f1'][i] = 1.0
                    else:
                        bert_scores['precision'][i] = 0.0
                        bert_scores['recall'][i] = 0.0
                        bert_scores['f1'][i] = 0.0
                else:
                    bert_scores['precision'][i] = 0.0
                    bert_scores['recall'][i] = 0.0
                    bert_scores['f1'][i] = 0.0
        elif len(references[i]) == 1:
            if len(references[i][0]) == 0:
                bert_scores['precision'][i] = 0.0
                bert_scores['recall'][i] = 0.0
                bert_scores['f1'][i] = 0.0

    precision = np.average(bert_scores['precision'])
    recall = np.average(bert_scores['recall'])
    f1 = np.average(bert_scores['f1'])
    #f1 = 2 * (precision * recall) / (precision + recall)
    if return_all_scores:
        return bert_scores
    else:
        return precision, recall, f1

def generate_scores(references, hypotheses):
    bleu_score_max, bleu_score_avg = get_bleu_score(references, hypotheses)
    rouge_scores_max, rouge_scores_avg = get_rouge_scores(references, hypotheses)

    metric = load_metric('bertscore')
    bert_scores = metric.compute(predictions=hypotheses, references=references, lang='en')
    bert_score = get_bert_score(bert_scores, hypotheses, references)

    print("Bleu Score (Avg): ", bleu_score_avg)
    print("Bleu Score (Max): ", bleu_score_max)
    print("Rouge Score (Avg) (Precision, Recall, F1): ", rouge_scores_avg)
    print("Rouge Score (Max) (Precision, Recall, F1): ", rouge_scores_max)
    print('BERT Score (Max) (Precision, Recall, F1): ', bert_score)

    return {
        'bleu_score_max': bleu_score_max,
        'bleu_score_avg': bleu_score_avg,
        'rouge_scores_max': rouge_scores_max,
        'rouge_scores_avg': rouge_scores_avg,
        'bert_score': bert_score
    }