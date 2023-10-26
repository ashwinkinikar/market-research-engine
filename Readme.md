**Description:**

OpenAssistant is a Flask-based web service that leverages various APIs and machine learning models to provide information about creators, Wikipedia search results, and real-time stock data for companies. It integrates **OpenAI's GPT-3.5 Turbo model** for natural language processing tasks.

---

**How to Use:**

**Task 1 - Check Creator:**

*Endpoint:* `/check`

Use the following curl request to check the creator of the service:

```bash
curl -X GET "http://HOST_NAME:5000/check"
```

---

**Task 2 - Get Wikipedia Info:**

*Endpoint:* `/get_wikipedia_info`

Use the following curl request to get Wikipedia search results for a specific query (e.g., "Amazon"):

```bash
curl --location 'http://HOST_NAME:5000/get_wikipedia_info' \
--header 'Content-Type: application/json' \
--data '{ "query": "Amazon" }'
```

---

**Task 3 - Get Stock Info:**

*Endpoint:* `/get_stock_info`

Use the following curl request to get real-time stock information for a specific company (e.g., "Amazon"):

```bash
curl -X GET "http://HOST_NAME:5000/get_stock_info?company_name=Amazon"
```

---

**Dependencies:**

- Flask
- Requests
- yfinance
- **OpenAI GPT-3.5 Turbo**
- python-dotenv

---

**Run Locally:**

1. Install dependencies using `pip install -r requirements.txt`.
2. Run the Flask application with `python app.py`.

*Note: Replace HOST_NAME in the curl requests with the appropriate host where the Flask application is running.*

---

**Contributing:**

Contributions are welcome! Feel free to open issues or submit pull requests.

---
