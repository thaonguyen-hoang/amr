import pandas as pd
import penman.transform

file = 'data/reclor_data.csv'
df = pd.read_csv(file)

def to_list(words_list):
    res = [i.strip() for i in words_list[1:-1].replace("'", "").split(',')]
    return res

df['Logic-words'] = df['Logic-words'].apply(to_list)

logic_words = []
for w in df['Logic-words'].to_list():
    logic_words += w 
logic_words = sorted(list(set(logic_words)))
logic_words

with open('data/logic_words.txt', 'w') as f:
    for w in logic_words:
        f.write(w + '\n')

output = 'D:/python/pyforthesis/recreate/output_result/ReClor_xfm_t5wtense.csv'
df = pd.read_csv(output)
pd.set_option("max_")
df

file = open('D:/python/pyforthesis/recreate/output_result/viamr/graphs.txt', 'r', encoding='utf-8')
data = file.read().split('\n\n')
len(data)

import os
paths = ['D:/python/pyforthesis/recreate/data/viamr/viamr.txt',
 'D:/python/pyforthesis/recreate/data/viamr/user10_v3__user8_v2.txt',
 'D:/python/pyforthesis/recreate/data/viamr/user11_v3.txt',
 'D:/python/pyforthesis/recreate/data/viamr/user10_v3__user9_v2.txt',
 'D:/python/pyforthesis/recreate/data/viamr/user9_v3.txt',
 'D:/python/pyforthesis/recreate/data/viamr/user8_v3.txt']
for path in paths[1:]:
    f = open(path, 'r', encoding='utf-8')
    print(len(f.read().split('\n\n')))

import os
path = 'data/the_little_prince.txt'
texts = []
graphs = []
with open(path, encoding='utf8') as f:
        data = f.read().split('\n\n')
        for sample in data[1:]:
            idx = sample.find('(')
            texts.append(sample[:idx])
            graphs.append(sample[idx:].strip())

texts[0]
print(graphs[0])
print(graphs[-1])
assert len(texts) == len(graphs)
len(texts)

# vi-wordnet
import os
import copy
import re
dir = 'data/corpus/vi-wordnet'
files = [f for f in os.listdir(dir) if f.startswith(('adj', 'noun', 'verb'))]
paths = [os.path.join(dir, file) for file in files]
paths

def add_underscore(word):
    if ' ' in word:
        word = re.sub(r'\s+', '_', word.strip())
    return word

wordnet = {'A': {}, 'N': {}, 'V': {}}
for path in paths:
    if 'noun' in path:
        type = 'N'
    elif 'verb' in path:
        type = 'V'
    else:
        type = 'A'
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
        for line in data:
            if len(line.strip()) == 0:
                continue
            if ',' in line:
                words = [add_underscore(w) for w in line.split(',') if len(w.strip()) != 0]
                for w in words:
                    temp = copy.deepcopy(words)
                    temp.remove(w)
                    if w not in wordnet[type]:
                        wordnet[type][w] = temp
                    else:
                        wordnet[type][w] += temp
            else:
                word = add_underscore(line)
                if word not in wordnet[type]:
                    wordnet[type][word] = []            
    wordnet[type] = dict(sorted(wordnet[type].items(), key=lambda x: x[0]))
wordnet
len(wordnet)

# remove words with no synonyms (deprecated)
delete_w = []
for type in wordnet:
    for w in wordnet[type]:
        if len(wordnet[type][w]) == 0:
            delete_w.append((type, w))
        # wordnet['A'][w] = list(set(wordnet[type][w]))
delete_w
for w in delete_w:
    del wordnet[w[0]][w[1]]
wordnet



import json
file = 'D:\python\pyforthesis\\recreate\data\word_net_vi.json'
with open(file, encoding='utf-8') as f:
    viwordnet = json.load(f)
len(viwordnet)

output_file = 'data/viwordnet_.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(wordnet, f, indent=4, sort_keys=True, ensure_ascii=False)

file = 'data/viwordnet-by-type.json'
with open(file, encoding='utf-8') as f:
    viwordnet = json.load(f)
viwordnet

output_file = 'data/viwordnet-by-type.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(viwordnet, f, indent=4, sort_keys=True, ensure_ascii=False)

viwordnet_dict = dict(viwordnet)
new_dict = {'A': {}, 'N': {}, 'V':{}}
for pos in viwordnet_dict:
    pos_dict = viwordnet_dict[pos]
    for word in pos_dict:
        new_dict[pos][add_underscore(word)] = list(set([add_underscore(s) for s in pos_dict[word]]))
new_dict

output_file = 'data/viwordnet-dash-by-type.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(wordnet, f, indent=4, sort_keys=True, ensure_ascii=False)

gen_sent_file = 'data/viamr/augmented/augmented_gen_sent_level.json'
with open(gen_sent_file, encoding='utf-8') as f:
    gen_sents = json.load(f)
gen_sents

original = 'data/viamr/augmented/original.txt'
modified = 'data/viamr/augmented/modified.txt'
with open(original, 'w', encoding='utf-8') as f1:
    with open(modified, 'w', encoding='utf-8') as f2:
        for item in gen_sents:
            f1.write('#::tag ' + item['tag'] + '\n')
            f1.write(item['source'] + '\n')
            f1.write(item['original_graph'] + '\n\n')
            f2.write('#::tag ' + item['tag'] + '\n')
            f2.write('#::gen_snt ' + item['gen_sent'] + '\n')
            f2.write(item['modified_graph'] + '\n\n')

import os

original = 'data/viamr/original/user9_v3_1.txt'
preprocess = 'data/viamr/preprocess/graphs_user9_v3_1.txt'

fn = original.split('/')[3]
print(os.path.exists(original))
print(os.path.exists(preprocess))
print(fn)

texts = []
graphs = []
with open(original, encoding='utf8') as f1:
    with open(preprocess, encoding='utf-8') as f2:
        data1 = f1.read().split('\n\n\n')
        data2 = f2.read().split('\n\n')
        assert len(data1) == len(data2)
        for i in range(len(data1)):
            idx = data1[i].find('\n')
            texts.append(data1[i][:idx])
            graphs.append(data2[i])
        assert len(graphs) == len(texts)

import random
i = random.randint(0, len(graphs))
print(texts[i])
print(graphs[i])

new_fn = f'data/viamr/final/full_{fn}'
with open(new_fn, 'w', encoding='utf-8') as f:
    for i in range(len(texts)):
        f.write(texts[i] + '\n')
        f.write(graphs[i] + '\n\n')

# reformat
# dir = 'data/viamr/final/'
# fn = 'user10_v3__user9_v2.txt'
# path = dir + f'full_{fn}'
path = 'D:/document/zalo/gold_private_test.txt'

texts = []
graphs = []
with open(path, encoding='utf8') as f:
    data = f.read().split('\n\n')
    for sample in data[:]:
        idx = sample.find('\n')
        texts.append(sample[:idx])
        graphs.append(sample[idx:].strip())
        assert len(texts) == len(graphs)

test = '''(ax / multi-sentence
    :snt1(x / xin
        :compound(c / chào)
        :polarity -)
        :beneficiary (e
            :prep (d / do))
    :snt2(c2 / cho
        :mode interrogative
        :topic-of(h / hỏi
            :time(wz1 / x)
            :agent(m / mình)
            :modality(wz1 / -)
            :modality(wz2 / +)
            :theme(c3 / câu
                :wiki(wz1 / -)))))'''

dec_g = penman.decode(test)
enc_g = penman.encode(dec_g, indent=3)
print(enc_g)

import penman
import re
def reformat(g):
    pat1 = r':mode[_\s]*expressive\([^)]*\)'
    pat2 = r':mode[_\s]*imperative\([^)]*\)'
    pat3 = r':mode[_\s]*interrogative\([^)]*\)'
    pat4 = r':polarity\(.* \/ ((?!amr-unknown)[^\)]*)\)'
    pat5 = r'(:quant\(wz\d?\s*\/\s*)(\d+)\)'
    pat6 = r'(:value\(wz\d?\s*\/\s*)(\d+)\)'
    pat7 = r'(:wiki\(wz\d?\s*\/\s*)(-)\)'
    pat8 = r'(:modality\(wz\d?\s*\/\s*)([-+])\)'
    res = re.sub(pat1, ':mode expressive', g)
    res = re.sub(pat2, ':mode imperative', res)
    res = re.sub(pat3, ':mode interrogative', res)
    res = re.sub(pat4, ':polarity -', res)
    res = re.sub(pat5, r':quant \2', res)
    res = re.sub(pat6, r':value \2', res)
    res = re.sub(pat7, r':wiki \2', res)
    res = re.sub(pat8, r':modality \2', res)
    return res

def reformat_2(g):
    try:
        dec_g = penman.decode(g)
    except Exception as e:
        print(g)
        print(e)
    else:
        var = dec_g.variables()
        for v in var:
            if v.startswith('wz'):
                inst = [t for t in dec_g.instances() if t.source == v][0]
                if inst.target in var:
                    edge = dec_g.edges(target=v)[0]
                    dec_g.triples.remove(edge)
                    dec_g.triples.remove(inst)
                    dec_g.triples.append((edge.source, edge.role, inst.target))
        enc_g = penman.encode(dec_g, indent=4)
        return enc_g

test_r = reformat(test)
# test_r = reformat_2(test_r)
print(test_r)

reformat_g = []
for graph in graphs:
    tmp = reformat(graph)
    reformat_g.append(tmp)

reformat_g

# reformat_g2 = []
# for graph in reformat_g:
#     tmp = reformat_2(graph)
#     reformat_g2.append(tmp)
# reformat_g2

new_fn = 'D:/document/zalo/reformat_gold_test.txt'
# new_fn = new_dir + f'reformat_{fn}'
with open(new_fn, 'w', encoding='utf-8') as f:
    for i in range(len(texts)):
        f.write(texts[i] + '\n')
        f.write(reformat_g[i] + '\n\n')

import json
news = 'data/test/news_dataset.json'
with open(news, 'r', encoding='utf-8') as f:
    news_dataset = json.load(f)

news_dataset
len(news_dataset)

texts = []
for item in news_dataset:
    content = item['content'].split('.')
    texts += [sent.strip() for sent in content if len(sent) >= 30 and len(sent) <= 70]

texts
with open('data/test/news.txt', 'x', encoding='utf-8') as f:
    for t in texts:
        f.write(t + '\n')

texts[5000:]

import json
file = 'data/viamr/augmented/augmented_sent_level.json'
with open(file, 'r', encoding='utf-8') as f:
    augmented = json.load(f)

import penman
from penman.transform import dereify_edges
from penman import model
g = augmented[18]['modified_graph']
print(g)
dec_g = penman.decode(g)
trans_g = dereify_edges(dec_g, model)
enc_g = penman.encode(trans_g, indent=3)
print(enc_g)


# swap/delete/insert
dir = 'data/viamr/reformat/'
fn = 'reformat_user8_v3.txt'
path = dir + fn

texts = []
graphs = []
with open(path, encoding='utf8') as f:
    data = f.read().split('\n\n')
    for sample in data[:]:
        idx = sample.find('\n')
        texts.append(sample[:idx])
        graphs.append(sample[idx:].strip())
        assert len(texts) == len(graphs)

import penman
import re
g = penman.decode(graphs[0])
enc_g = penman.encode(g, indent=None)
print(enc_g)

def convert_polarity(line):
    neg = ':polarity - :'
    if re.findall(r':polarity -', line):  # delete polarity - in the original sentences
        new_line = re.sub(r':polarity - ', '', line, 1)
    elif re.findall(r'^\( multi-sentence', line):  # multiple sentences
        if re.findall(r'(:snt\d+ \( and ):', line):
            new_line = re.sub(r'(:snt\d+ \( and :op1 \( \S+ ):', r'\\1' + neg, line)
        else:
            new_line = re.sub(r'(:snt\d+ \( \S+ ):', r'\\1' + neg, line)
    elif re.findall(r'^(\( \S+ ):', line):
        if re.findall(r'^(\( and ):', line):  # if begin with and
            new_line = re.sub(r'^(\( and :op1 \( \S+ ):', r'\\1' + neg, line)
        else:
            new_line = re.sub(r'^(\( \S+ ):', r'\\1' + neg, line)  # add negative after main predicate
    else:
        new_line = re.sub(r'\)\n', r':polarity - \)\n', line)
        # print(new_line)

    return new_line

new_g = convert_polarity(enc_g)
print(enc_g)
print(new_g)

test = '''(v / vẽ
    :manner(t1 / theo
        :source(c / chỉ_dẫn
            :quant (1
                :classifier(s / sự))
            :poss(ô / ông_hoàng
                :mod(n / nhỏ))))
    :agent(t2 / tôi)
    :tense(đ / đã)
    :theme(t3 / tinh_cầu
        :mod(đ1 / đó)))'''

g = penman.decode(test)
triples = g.triples
removed = g.edges(role=':source')[0]
removed
filtered_triples = [t for t in triples if t != removed and t[0] != removed.target]
filtered_triples
new_graph = penman.Graph(filtered_triples, top=g.top)
enc_g = penman.encode(new_graph, indent=3)
print(enc_g)
g.edges()