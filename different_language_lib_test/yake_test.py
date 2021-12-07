import yake

kw_extractor = yake.KeywordExtractor()
text = """spaCy is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython. The library is published under the MIT license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion."""
text = "«Некрономико́н» (англ. Necronomicon), также «Книга Мертвых» или «Аль-Азиф» — вымышленная книга-гримуар (учебник магии), придуманная американским писателем ужасов Говардом Филлипсом Лавкрафтом. Другие авторы, такие как Август Дерлет и Кларк Эштон Смит первыми начали цитировать строки из «Некрономикона» в своих произведениях. Позже книга стала часто упоминаться в произведениях последователей «Мифов Ктулху». Сам Лавкрафт одобрял этот прием от других писателей, опирающихся на его книги в «Мифах Ктулху», полагая, что такие общие намеки создают «фон дурного правдоподобия»."
text = "Когда я только начинал работать удаленно, то целые месяцы приводил в порядок свое рабочее место, стараясь довести всё до совершенства. Стол, кронштейны для монитора, веб-камера – просто остановиться не мог. Моя работа напрямую связана с тем, чтобы повышать людям производительность, так что о подобных вещах я думаю много."
language = "rus"
max_ngram_size = 1
deduplication_threshold = 0.9
numOfKeywords = 10
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text)
for kw in keywords:
    print(kw)

#не подходит
