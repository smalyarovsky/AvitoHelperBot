# BarygaHelperBot
Телеграмм ботик для отслеживания свежих объявлений на Авито

Этот бот написан полностью на питоне и является плодом моих прошлых нелепых фантазий о заработке на перепродаже компьютеров на Авито. Так как писал для себя, функционал довольно узкий - отслеживание объявлений по какому-то заданному набору ссылок. Свою задачу бот выполнял неплохо - каждые 30 секунд присылал, если таковые были, новые объявления. Проектом давно не занимался, поэтому не уверен что сейчас бот работоспособен.

Итак, всего бот состоит из трех py файлов:
1) **bot.py**, в котором прописана вся основная логика. Это главный файл, именно он компилируется для запуска бота
2) **condition.py**, в котором лежат 4 переменные, обозначающие, в каком состоянии сейчас находится бот.
3) **config.py**, в котором лежат разные переменные для настройки работы бота, в частности, текст который выдается в ответ на разные действия пользователя

Вот и весь бот
