# Лабораторная работа #8. RPC. gRPC. Protobuf

## Запуск и развёртывание

```bash
docker-compose up --build
```
![alt text](photo_4_2024-12-22_18-42-33.jpg)
![alt text](photo_5_2024-12-22_18-42-33.jpg)
![alt text](photo_1_2024-12-22_18-42-33.jpg)
## Демонстрация
### Swagger
![alt text](photo_3_2024-12-22_18-42-33.jpg)

### Получение списка всех терминов.

```
curl -X 'GET' \
  'http://localhost:8000/terms/' \
  -H 'accept: application/json'
```
![alt text](photo_6_2024-12-22_18-42-33.jpg)


### Получение информации о конкретном термине по ключевому слову.


``` 
curl -X 'GET' \
  'http://localhost:8000/terms/search/?keyword=saga' \
  -H 'accept: application/json'
```
![alt text](photo_8_2024-12-22_18-42-33.jpg)

### Получение термина по id

```
curl -X 'GET' \
  'http://localhost:8000/terms/15' \
  -H 'accept: application/json'
```
![alt text](photo_2_2024-12-22_18-42-33.jpg)

### Добавление нового термина с описанием.
```
curl -X 'POST' \
  'http://localhost:8000/terms/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "keyword": "test123",
  "description": "desc123"
}'
```
![alt text](photo_7_2024-12-22_18-42-33.jpg)
### Обновление существующего термина.

```
curl -X 'PUT' \
  'http://localhost:8000/terms/12' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "keyword": "test1",
  "description": "Test word 1"
}'
```
![alt text](3.png)

### Удаление термина из глоссария.

``` 
curl -X 'DELETE' \
  'http://localhost:8000/terms/12' \
  -H 'accept: application/json'
```

![alt text](7.png)
