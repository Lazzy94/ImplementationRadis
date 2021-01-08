# ImplementationRedis #
Для запуска приложения нужно выполнить команду:

```docker-compose up -d --build  ```

Для работы с сервером можно использовать библиотеку [redis](https://pypi.org/project/redis/) или консольную утилиту [redis-cli](https://redis.io/topics/rediscli)

Пример взаимодействия с сервером продемонстрирован в client.py 

Через env переменные можно переопредить хост (HOST), порт (PORT) и максимальное колличество клиентов (MAX_CLIENTS)

Дефолтный порт = 31337 

Дефолтный хоcт = 0.0.0.0 

В данном приложении реализованны следующие методы:

1) SET - записывает ключ и значение
2) GET - возвращает значение по указанному ключу
3) DEL - удаляет ключ и значение по указанному ключу
4) KEYS - возращает все ключи и их значения, по паттерну (похожие на указанные в запросе)
5) FLUSHDB - очищает весь список
6) EXPIRE - задает время жизни (ttl) для заданного ключа (время указывается в секундах)
7) HGET - Возвращает значение, связанное с полем в хэше, хранящемся в ключе
8) HSET - Устанавливает поле в хэше, хранящемся под ключом к значению Если ключ не существует, создается новый ключ,
   содержащий хеш Если поле уже существует в хэше, оно перезаписывается
9) LSET - Устанавливает элемент списка по индексу
10) RPUSH -Добавляет все указанные значения в конец списка, хранящегося в ключе Если ключ не существует, он создается
    как пустой список перед выполнением операции push Когда ключ содержит значение, не являющееся списком, возвращается
    ошибка Можно протолкнуть несколько элементов с помощью одного вызова команды, просто указав несколько аргументов
    Элементы вставляются один за другим в конец списка, от крайнего левого элемента до крайнего правого элемента
11) LPUSH - команда похожая на RPUSH, отличие в том что добавляет элементы в начало списка
12) LRANGE - Возвращает указанные элементы списка, хранящегося в ключе Смещения start и stop - это индексы,
    отсчитываемые от нуля, где 0 - это первый элемент списка (заголовок списка), 1 - следующий элемент и так далее.
13) LINDEX - Возвращает элемент по индексу в списке, хранящемся в ключе Индекс отсчитывается от нуля, поэтому 0 означает
    первый элемент, 1 - второй элемент и так далее Отрицательные индексы могут использоваться для обозначения элементов,
    начинающихся в конце списка Здесь -1 означает последний элемент, -2 означает предпоследний и так далее Если значение
    в ключе не является списком, возвращается ошибка
