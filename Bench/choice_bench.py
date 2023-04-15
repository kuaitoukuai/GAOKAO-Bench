from bench_function import choice_test, get_api_key, export_distribute_json_v2, export_union_json
import os
import json
import time

if __name__ == "__main__":
    with open("选择题prompt.json", "r") as f:
        data = json.load(f)
    f.close()
    for i in range(len(data['examples'])):

        api_key_filename = ""
        api_key_list = get_api_key(api_key_filename, start_num=0, end_num = 1)
        model_name = 'text-davinci-003'
        temperature = 0.3
        directory = ""
        keyword = data['examples'][i]['keyword']
        question_type = data['examples'][i]['type']
        zero_shot_prompt_text = data['examples'][i]['prefix_prompt']
        print(keyword)
        print(question_type)

        export_distribute_json_v2(
            api_key_list, 
            model_name, 
            temperature, 
            directory, 
            keyword, 
            zero_shot_prompt_text, 
            question_type
        )


        export_union_json(
            directory, 
            model_name, 
            keyword,
            zero_shot_prompt_text,
            question_type
        )
        

