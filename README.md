# Скрипт генерации файлов конфигурации Postfix. Производит соответствие пользователей входящих в группу Active Directory, параметрам SMTP, указанным в файле конфигурации

Для использования данного скрипта необходимо:

  - Клонировать репозиторий 

  ``` git clone https://github.com/maximishchenko/postfix_relay_by_ldap_group.git ``` 


  - Перейти в каталог скрипта 

  ``` cd /path/to/script ```

  - Скопировать файл config/config.ini.sample в config/config.ini 

  ``` cp config/config.ini.sample config/config.ini ```


  - указать в файле config/config.ini актуальные данные (секции AD и OUT обязательные, остальные секции опциональны, по одной на каждую группу ldap, минимально должно присутствовать 1 описание группы Active Directory)

  - запустить скрпит main.py 

  ``` python3 /path/to/main.py ```