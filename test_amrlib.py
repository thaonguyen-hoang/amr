import amrlib
# from amrlib.models.parse_xfm.inference import Inference
import sacrebleu
import pandas as pd
import time
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

def bleu(targets, predictions, smooth=1.0):
    """Computes BLEU score.
    
    Args:
    targets: list of strings or list of list of strings if multiple references are present.
    predictions: list of strings
    
    Returns:
    bleu_score across all targets and predictions
    """
    bleu_score = sacrebleu.sentence_bleu(predictions[0], targets,
                                       smooth_method="exp",
                                       smooth_value=smooth,
                                       lowercase=False,
                                       tokenize="intl")
    return {"bleu": bleu_score.score}

# docs example
stog = amrlib.load_stog_model('amrlib/models/parse_xfm_bart_large')
graphs = stog.parse_sents(['He wanted the girl to believe him'])
for graph in graphs:
    print(graph)

gtos = amrlib.load_gtos_model('amrlib/models/generate_t5wtense')
sents, _ = gtos.generate(graphs, use_tense=True)
for sent in sents:
    print(sent)

# test on some sample sentences
now = int(round(time.time()*1000))
now02 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("The start time is: ",now02)

data = []
df = pd.DataFrame(data,columns=['Original_Sentence','Generated_Sentence','BLEU_Score'])

# read samples from file
file = open("data/reclor.csv", 'r', encoding='utf-8')
sentence_list = []
dataframe = pd.read_csv(file)
num_rows = 5
for index, row in tqdm(dataframe.iterrows(), total=num_rows):
    sentence_list.append(row['Sentences'])
    if index == num_rows:
        break
    
# convert sent -> graph
graphs = stog.parse_sents(sentence_list)

# convert graph -> sent
sents, _ = gtos.generate(graphs)

# compute BLEU score and append result to a dataframe
for sent_id in tqdm(range(len(sents))):
    bleu_score = bleu([sentence_list[sent_id]], [sents[sent_id]])
    df.loc[len(df)] = {'Original_Sentence': sentence_list[sent_id], 'Generated_Sentence': sents[sent_id], 'BLEU_Score': bleu_score['bleu']}

df.to_csv("data/reclor_xfm_t5wtense.csv", index = None, encoding = 'utf8')

now = int(round(time.time()*1000))
now02 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("The end time is: ",now02)