# hw-mafia-game
gRPC Mafia game app 

### Setup
```
docker-compose build
docker-compose up
```

### Usage
* Сгенерировать код из .proto файла можно из директории proto с помощью следующих команд:

(Пример для другой организации файлов)
```
pip install grpcio-tools
python3 -m grpc_tools.protoc -I pkg/proto --python_out=. --grpc_python_out=. pkg/proto/mafia.proto
```

* Для консольного запуска сервера/клиента:
```
python client_main.py
python server_main.py
```

### Game process
__Выбор комнаты__:
В начале игры участники задают имена и имя комнаты. Далее либо создается новая комната, либо участник ждет подключения к нужной комнате по запросу.

После подключения можно выбрать режим прохождения игры: бот/игрок

__Игровой день__:
Информация об участниках выводится в консоль по ходу игры
Днем можно запросить информацию об участниках и тд
Далее проводится голосование, боты голосуют автоматически
Игра заканчивается после очереди голосований и победы одной из команд

