- TASK 1
  curl -X GET "http://HOST_NAME:5000/check"

- TASK 2

```
curl --location 'http://HOST_NAME:5000/get_wikipedia_info' \
--header 'Content-Type: application/json' \
--data '{ "query": "Facebook" }
'
```

- TASK 3
  curl -X GET "http://HOST_NAME:5000/get_stock_info?company_name=Amazon"
