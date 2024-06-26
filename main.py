import pysrt
import spacy
import aiohttp
import asyncio

# Загрузка модели испанского языка для spacy
nlp = spacy.load('es_core_news_sm')

# Асинхронная функция для перевода слова
async def translate_word(session, word):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "es",
        "tl": "en",
        "dt": "t",
        "q": word
    }
    async with session.get(url, params=params) as response:
        result = await response.json()
        return result[0][0][0]

# Асинхронная функция для обработки субтитров
async def process_subtitles(file_path):
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
                    task = asyncio.ensure_future(translate_word(session, lemma))
                    tasks.append((lemma, task, text))

        results = await asyncio.gather(*(task for _, task, _ in tasks))
        word_pairs = [(lemma, result, context) for (lemma, _task, context), result in zip(tasks, results)]

    return word_pairs

# Пример использования
async def main():
    file_path = 'subs/test.srt'
    word_pairs = await process_subtitles(file_path)
    
    for word_pair in word_pairs:
        print(f"Spanish: {word_pair[0]} | English: {word_pair[1]} | Context: {word_pair[2]}")

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
