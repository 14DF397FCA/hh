Для работы приложения необходимо иметь `Client ID` и `Client Secret`. 
Для получения `Client ID` и `Client Secret` необходимо зарегистрировать приложение на https://dev.hh.ru.

* Запустить на сервере к которому можно обратиться из интернета приложение `listener.py`.
* Сформировать ссылку для получения `authorization_code` из инструкции к API https://github.com/hhru/api/blob/master/docs/authorization_for_user.md.
* Из вывода приложения `listener.py` получить (скопировать) `code`
* 

Поддерживаемые ключи запуска приложения `listener.py`.
```
python3.6 ./listener.py -h
usage: listener.py [-h] [-p PORT] [-i INTERFACE] [-d DEBUG]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Listen port
  -i INTERFACE, --interface INTERFACE
                        Listen interface
  -d DEBUG, --debug DEBUG
                        Flask debug



https://hh.ru/oauth/authorize?response_type=code&client_id=GL95U30HT0QFMATRU5I696CIHVQR8SMEEDSGINKK2DND3I77BFQT1GEFOG6PO1GB&redirect_uri=http://hh.shop-vl.ru:8080/callback