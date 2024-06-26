import used_words

import pysrt
import spacy
import aiohttp
import asyncio
import genanki

SRT_FILE = 'subs/extra_1_1.srt'

# Загрузка модели испанского языка для spacy
nlp = spacy.load('es_core_news_sm')

# Асинхронная функция для перевода слова
async def translate_word(session, word: str, context: str):
    full_text = f"{word}. Контекст: {context}"

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "es",
        "tl": "en",
        "dt": "t",
        "q": full_text
    }
    async with session.get(url, params=params) as response:
        result = await response.json()
        return result[0][0][0].split('. ')[0]

# Асинхронная функция для обработки субтитров
async def process_subtitles(file_path):
    processed_tokens = set()

    subs = pysrt.open(file_path)
    word_pairs = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for sub in subs:
            text = sub.text
            doc = nlp(text)
            for token in doc:
                if token.is_alpha:
                    lemma = token.lemma_
                    if lemma.lower() not in used_words.used_words:
                        task = asyncio.ensure_future(translate_word(session, lemma, text))
                        tasks.append((lemma, task, text))
                        used_words.used_words.add(lemma)

        results = await asyncio.gather(*(task for _, task, _ in tasks))
        word_pairs = [(lemma, result, context) for (lemma, _task, context), result in zip(tasks, results)]

    return word_pairs


# Функция для создания Anki колоды
def create_anki_deck(word_pairs, deck_name=SRT_FILE):
    deck_id = 2059400110
    model_id = 1607392319

    model = genanki.Model(
        model_id,
        'Simple Model',
        fields=[
            {'name': 'Spanish'},
            {'name': 'English'},
            {'name': 'Context'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Spanish}}<br><br>{{Context}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{English}}',
            },
        ])

    deck = genanki.Deck(
        deck_id,
        deck_name
    )

    for spanish, english, context in word_pairs:
        note = genanki.Note(
            model=model,
            fields=[spanish, english, context]
        )
        deck.add_note(note)

    genanki.Package(deck).write_to_file(f'{deck_name}.apkg')


# Пример использования
async def main():
    word_pairs = await process_subtitles(SRT_FILE)
    
    for word_pair in word_pairs:
        print(f"{word_pair[0].capitalize()};{word_pair[1].capitalize()} | Context: {word_pair[2]}")

    create_anki_deck(word_pairs)

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
