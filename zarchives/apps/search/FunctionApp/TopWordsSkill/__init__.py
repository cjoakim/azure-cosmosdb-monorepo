
import azure.functions as func
import json
import logging
import string  

from collections import Counter

# This Python script is the implementation of the Azure Function for the Custom Skill
# referenced in the following Skillset schema.  The 'uri' in the Skillset schema should be
# populated with the URL of the deployed Azure Function.  This Function will be invoked with
# the mergedText for each indexed document, and will return the top words within the merged text.
# Chris Joakim, Microsoft, 2020/09/26

# {
#     "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
#     "name": "WebApiSkill",
#     "description": "Custom Skill implemented as an Azure Function",
#     "context": "/document",
#     "uri": "... populate me ...",
#     "httpMethod": "POST",
#     "timeout": "PT30S",
#     "batchSize": 100,
#     "degreeOfParallelism": null,
#     "inputs": [
#         {
#             "name": "text",
#             "source": "/document/mergedText"
#         }
#     ],
#     "outputs": [
#         {
#             "name": "text",
#             "targetName": "topwords"
#         }
#     ],
#     "httpHeaders": {}
# }

# TODO - enhance this list of stopwords
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = json.dumps(req.get_json())
        #logging.info(body)
        if body:
            result = compose_response(body)
            return func.HttpResponse(result, mimetype="application/json")
        else:
            return func.HttpResponse("Invalid body", status_code=400)
    except:
        return func.HttpResponse("Invalid body", status_code=400)

def compose_response(body):
    results = {}
    results["values"] = []
    input_values = json.loads(body)['values']

    for input_value in input_values:
        output_value = transform_value(input_value)
        if output_value != None:
            results['values'].append(output_value)
    return json.dumps(results, ensure_ascii=False)

def transform_value(value):
    try:
        recordId = value['recordId']
        text = value['data']['text']
        topWordsString = getTopWords(text)
        logging.info('topWordsString: ' + topWordsString) 
    except:
        return unsuccessful_transformation_result(recordId)
    return successful_transformation_result(recordId, topWordsString)

def successful_transformation_result(rec_id, topWordsString):
    result = dict()
    result['recordId'] = rec_id
    result['data'] = { "text": topWordsString }
    return (result)

def unsuccessful_transformation_result(rec_id):
    result = dict()
    result['recordId'] = rec_id
    result['errors'] = [{ "message": "Could not complete operation for record." }]
    return (result)

def getTopWords(input_text):
    max_words = 2000
    words_list, top_words_list = list(), list()
    scrubbed_text = input_text.replace("\n",' ')\
        .replace("\t",' ').replace("\'",'').replace("\"",'')\
        .replace('.', ' ').replace('(', '').replace(')', '')\
        .replace('[', '').replace(']', '')

    #logging.info('scrubbed_text: ' + scrubbed_text)
    for input_word in scrubbed_text.split(' '):
        tword = translate_word(input_word).strip()
        if len(tword) > 2:
            if len(words_list) < max_words:
                #logging.info('word: {} -> {}'.format(input_word, tword))
                words_list.append(tword)

    #logging.info('words_list: {}\nwords_list_count: {}'.format(words_list, len(words_list)))

    c = Counter(words_list[0:max_words])
    for tw_tup in c.most_common(20):  # [('web', 5), ('', 1), ('flask', 1), ('development', 1), ...]
        if len(tw_tup[0]) > 1:
            word = tw_tup[0]
            if word in stopwords:
                pass
            else:
                top_words_list.append(word)
    return json.dumps(top_words_list)

def translate_word(w):
    return w.replace('.','').replace(',','').replace('!','').replace('?','').lower().strip()
