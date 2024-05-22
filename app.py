from flask import Flask, render_template, request, jsonify
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid_secrets import client_id, secret

app = Flask(__name__)

# Your Plaid credentials
PLAID_CLIENT_ID = client_id
PLAID_SECRET = secret
PLAID_ENV = 'sandbox'

# Configure the Plaid client
configuration = Configuration(
    host=plaid.Environment.Sandbox,  # Use plaid.Environment.Development or plaid.Environment.Production as needed
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_link_token', methods=['GET'])
def create_link_token():
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(
                client_user_id='unique_user_id'
            ),
            client_name='Flow Grapher',
            products=['transactions'],
            country_codes=['US'],
            language='en',
            webhook='https://your-webhook-url.com'
        )
        response = client.link_token_create(request)
        return jsonify({'link_token': response['link_token']})
    except plaid.ApiException as e:
        error_message = e.body
        return jsonify({'error': error_message}), 400

@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    public_token = request.json.get('public_token')
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        return jsonify({'access_token': access_token})
    except plaid.ApiException as e:
        error_message = e.body
        return jsonify({'error': error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)
