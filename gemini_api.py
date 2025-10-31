import google.generativeai as genai
import json
import time

file_path = 'new_data.json'
API_KEY = "AIzaSyAQKGAkaJ50MKpuMX94c0ztn0YQTJt4DYo"

def ask_gemini(question, api_key):
    """Send a question to Gemini API and get the response."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    response = model.generate_content(question)
    return response.text if response else "No response received."

def read_data(file_name):
    data = []
    with open(file_name, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    data = read_data(file_path)
    #Generate the sentence 
    for i in range(len(data)):
        # if i == 2:
        #     break
        amr = data[i]['new_amr']
        prompt = f"""You will be provided with an AMR (Abstract Meaning Representation) graph. Your task is to convert this AMR graph into a clear and grammatically correct sentence in Vietnamese. Please strictly follow these requirements:

            1. Do not modify or change the structure of the AMR.
            2. The answer **should only include** the Vietnamese sentence generated from the AMR—no additional comments, explanations, or extra text.
            3. The sentence must make sense, be grammatically correct, and accurately reflect the content of the AMR.
            4. The words must be logically arranged, closely following the relationships in the AMR structure.
            For example: 
            AMR structure: {data[i]['amr']}
            A possible sentence generated from the AMR structure: {data[i]['snt']}
            Here is the AMR graph you need to create a sentence from:
            {amr}
        """
        answer = ask_gemini(prompt, API_KEY)
        data[i]['new_sen'] = answer 
        print(i)
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write(answer + "\n")
        time.sleep(3)
    with open('final_test.json', 'w', encoding='utf-8') as f:
          json.dump(data, f, ensure_ascii=False, indent = 2)
