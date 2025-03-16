import os
from openai import OpenAI

API_KEY = os.environ['DEEPSEEK_API_KEY']

BASE_URL = 'https://api.deepseek.com'

CLIENT = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def is_primary_source(title: str) -> bool:
    messages = [
            {"role": "system", "content": "You are an expert in historical sources. \
                    When given a title, determine whether it represents a primary source. \
                    Respond only with True or False. \
                    Respond with False if you are unsure."},
            {"role": "user", "content": f"Title: {title}"}
        ]
    try:
        response = CLIENT.chat.completions.create(model="deepseek-chat",
                                                  messages=messages,
                                                  max_tokens=5,
                                                  temperature=1.0)
        answer = response.choices[0].message.content.strip()
        if answer.lower() in ["true", "yes"]:
            return True
        elif answer.lower() in ["false", "no"]:
            return False
        else:
            return False
    except Exception as e:
        print(f'Error: {e}')
        return False


def get_translation(arabic_text: str) -> str:
    messages = [
            {"role": "system", "content": "You are an expert in trsnslating arabic texts to english. \
                    When given a string of arabic text, translate it to english with ALA-LC transliterations where needed. \
                    Do not make any additions or omissions to the text. \
                    Include only the translation and nothing else in your output."},
            {"role": "user", "content": f"Arabic Text: {arabic_text}"}
        ]
    try:
        response = CLIENT.chat.completions.create(model="deepseek-chat",
                                                  messages=messages,
                                                  max_tokens=100,
                                                  temperature=1.3)
        answer = response.choices[0].message.content
        return answer
    except Exceptions as e:
        print(f'Error: {e}')
        return None


if __name__ == '__main__':
    translation = get_translation("٣٣٠٤٥ - حَدَّثَنَا وَكِيعٌ، عَنْ إِسْرَائِيلَ، عَنْ عَبْدِ الْأَعْلَى، عَنِ ابْنِ الْحَنَفِيَّةِ، قَالَ: سَمِعْتُهُ يَقُولُ: «لَا إِيمَانَ لِمَنْ لَا تَقِيَّةَ لَهُ»")
    print(translation)

