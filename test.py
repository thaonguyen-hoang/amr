from gensim.models import KeyedVectors # type: ignore
import json

# Đường dẫn tới file .txt chứa mô hình PhoW2V
model_path = 'word2vec_vi_words_100dims.txt'
file_name = "amr_output.json"
# Tải mô hình PhoW2V từ file .txt



with open(file_name, "r", encoding="utf-8") as f:
    data = json.load(f)

# print(len(data))
# print(data[0])

model = KeyedVectors.load_word2vec_format(model_path, binary=False)

substitute_list = []


def simple_substitute(sample_test):
  list_word = sample_test["word"]
  amr = sample_test["amr"]

  if len(list_word) == 0:
    sample_test["new_word"] = ""
    sample_test["new_amr"] = ""
    substitute_list.append(sample_test)
    return
  
  #find the similar word
  for word in list_word:
    #A set to check if new word is used
    checked = set()
    try:
      similar_words = model.most_similar(positive = [word], topn = 5)
    except KeyError:
      print(f"Từ '{word}' không có trong vocabulary, bỏ qua.")
      continue
    print(similar_words)
    #swap the similar with the original
    if word == 'ví_dụ':
      original_word = 'example'
    else :
      original_word = word

    for sim_word, sim_score in similar_words:
      if not original_word[0].isupper():
        sim_word = sim_word.lower()
      if sim_word == word or sim_word in checked:
        continue

      new_dict = sample_test.copy()
      # if the original doesn't have upper character, the similar will be lowered

      checked.add(sim_word)
      new_amr = amr.replace(original_word,sim_word)
      new_dict["new_word"] = sim_word
      new_dict["new_amr"] = new_amr

      substitute_list.append(new_dict)

    
count = 0
for sample in data:
  print(count)
  simple_substitute(sample)
  count+=1

print(len(substitute_list))

with open('new_data.json', "w", encoding='utf-8') as f:
  json.dump(substitute_list, f, ensure_ascii=False, indent = 2)

  



# # Tìm từ tương tự nhất
# for word in sample_sen:
#     synonym_dict[word] = []
#     similar_words2 = model.most_similar(positive = [word], topn=5)
#     synonym_dict[word].extend(similar_words2)

# with open('text.txt','w', encoding='utf-8') as f:
#     for key, value in synonym_dict.items():
#       f.write(f"{key}:\n")  # Ghi key trước
#       for item in value:
#           f.write(f"{item}\n")  
#       f.write("\n") 