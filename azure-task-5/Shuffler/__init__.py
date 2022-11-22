# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging


def main(mapperlist: list) -> dict:
    output_list = {}
    for k in mapperlist:
        for i in k:
            word= i[0]
            count = i[1]
            word_count = output_list.get(word)
            if word_count is None:  # If the word does not already exist in the output-list... get its previous count
                word_count = [count]
            else:
                word_count.append(count)
            output_list[word] = word_count
    return output_list