import openai
from config import config

openai.api_key =  config.gpt_api_key

def send_request_gpt(text, annotationLength: int, articleLength: int):
    response1 = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Напиши аннотацию для следующего текста, длина текста должна быть {annotationLength}: {text}"
    )
    
    response2 = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Напиши укороченную версию следующего текста, длина текста должна быть {articleLength}: {text}"
    )

    return response1, response2



if __name__ == '__main__':
    with open('text.txt', 'rb') as file:
        text = file.read()

    annotationLength = 600
    articleLength = 6000

    send_request_gpt(text, annotationLength, articleLength)