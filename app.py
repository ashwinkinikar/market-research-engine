import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
import yfinance as yf  # Import yfinance library for stock data
import json
# Load environment variables from .env file
load_dotenv()

open_api_key = os.getenv("OPEN_API_KEY")
# Wikipedia API endpoint URL
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

app = Flask(__name__)


def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# TASK 1
@app.route('/check', methods=['GET'])
def check():
    response = {'creator': 'Ashwin Kinikar'}
    return jsonify(response)

# TASK 2
@app.route('/get_wikipedia_info', methods=['POST'])
def get_wikipedia_info():
    # Get the query from the request data
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Define the parameters for the Wikipedia API request
    params = {
        'action': 'query',
        'list': 'search',
        'format': 'json',
        'srsearch': query
    }

    try:
        # Make a request to the Wikipedia API
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract the number of hits and the content of the first hit
        search_results = data.get('query', {}).get('search', [])
        number_of_hits = len(search_results)
        first_hit = search_results[0]['snippet'] if number_of_hits > 0 else "No results found"

        # Remove HTML tags from the snippet using a simple regex
        first_hit = remove_html_tags(first_hit)

        return jsonify({
            'numberOfHits': number_of_hits,
            'firstHit': first_hit
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to Wikipedia API'}), 500


# TASK 3
@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    company_name = request.args.get('company_name')
    print(company_name)

    if not company_name:
        return jsonify({'error': 'Company name not provided'}), 400

    try:
        url = "https://api.openai.com/v1/chat/completions"
        key = f'Bearer {open_api_key}'

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides information about companies."
                },
                {
                    "role": "user",
                    "content": f"Do a market research on {company_name} and provide as much information in a JSON format: market_research: str, stock_symbol: str "
                }
            ],
            "temperature": 0.7,
            "max_tokens": 150,
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': key
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if 'choices' in response_data:
            print(response_data)
            text_result = response_data['choices'][0]['message']['content']
            # Parse the JSON from the response
            result = json.loads(text_result)
            if 'stock_symbol' in result:
                # Create a Ticker object for the company
                company_ticker = result['stock_symbol']
                stock_info = yf.Ticker(company_ticker)

                # Get the latest data point for the stock
                data = stock_info.history(period="1d")

                # Get the current stock price
                current_price = data['Close'][0]

                print(f"Current stock price for {company_ticker}: ${current_price:.2f}")
                result["current_price"] = current_price
                result["company_name"] = company_name

            return result
        else:
            return jsonify({'error': 'Failed to generate text from OpenAI GPT-3.'}), 500

    except Exception as e:
        return jsonify({'error': 'Failed to fetch data from OpenAI GPT-3 or yfinance.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
