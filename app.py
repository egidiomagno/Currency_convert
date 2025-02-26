import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def get_exchange_rates(base_currency="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["rates"]
    else:
        raise Exception("Failed to fetch exchange rates")

def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates(from_currency)
    if to_currency in rates:
        return amount * rates[to_currency]
    else:
        raise Exception("Target currency not available")

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Currency Converter</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }

            .container {
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }

            h1 {
                text-align: center;
                margin-bottom: 30px;
            }

            .form-container {
                display: flex;
                flex-direction: column;
            }

            label {
                margin-bottom: 8px;
                font-weight: bold;
            }

            input, select {
                margin-bottom: 20px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }

            input[type="number"] {
                width: 100%;
            }

            select {
                width: 100%;
            }

            .result-container {
                text-align: center;
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #e0f7fa;
                border-radius: 4px;
            }

            .result-container.error {
                background-color: #ffcccb;
                color: red;
            }

            .result-container.success {
                background-color: #c8e6c9;
                color: green;
            }
        </style>
        <script>
            function convertCurrency() {
                const amount = document.getElementById('amount').value;
                const fromCurrency = document.getElementById('from_currency').value.toUpperCase();
                const toCurrency = document.getElementById('to_currency').value.toUpperCase();

                if (amount <= 0) {
                    alert("Amount should be greater than 0");
                    return;
                }

                // Send AJAX request to Flask server
                fetch(`/convert?amount=${amount}&from_currency=${fromCurrency}&to_currency=${toCurrency}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            document.getElementById('result-container').innerHTML = "Error: " + data.error;
                            document.getElementById('result-container').style.display = 'block';
                            document.getElementById('result-container').classList.add('error');
                            document.getElementById('result-container').classList.remove('success');
                        } else {
                            // Check if formatted_amount and formatted_converted_amount exist
                            if (data.formatted_amount && data.formatted_converted_amount) {
                                const formattedAmount = data.formatted_amount;
                                const formattedConvertedAmount = data.formatted_converted_amount;

                                document.getElementById('result-container').innerHTML = `${formattedAmount} ${fromCurrency} = ${formattedConvertedAmount} ${toCurrency}`;
                                document.getElementById('result-container').style.display = 'block';
                                document.getElementById('result-container').classList.add('success');
                                document.getElementById('result-container').classList.remove('error');
                            } else {
                                document.getElementById('result-container').innerHTML = "Error: Conversion data is missing.";
                                document.getElementById('result-container').style.display = 'block';
                                document.getElementById('result-container').classList.add('error');
                                document.getElementById('result-container').classList.remove('success');
                            }
                        }
                    })
                    .catch(error => {
                        document.getElementById('result-container').innerHTML = "An error occurred. Please try again later.";
                        document.getElementById('result-container').style.display = 'block';
                        document.getElementById('result-container').classList.add('error');
                        document.getElementById('result-container').classList.remove('success');
                    });
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Currency Converter</h1>
            <div class="form-container">
                <label for="amount">Amount:</label>
                <input type="number" id="amount" name="amount" placeholder="Enter amount" oninput="convertCurrency()">
                
                <label for="from_currency">From Currency:</label>
                <select id="from_currency" name="from_currency" onchange="convertCurrency()">
                    <option value="IDR">IDR - Indonesian Rupiah</option>
                    <option value="USD">USD - US Dollar</option>
                    <option value="EUR">EUR - Euro</option>
                    <option value="JPY">JPY - Japanese Yen</option>
                    <option value="GBP">GBP - British Pound</option>
                    <!-- Add more currency options here as needed -->
                </select>
                
                <label for="to_currency">To Currency:</label>
                <select id="to_currency" name="to_currency" onchange="convertCurrency()">
                    <option value="USD">USD - US Dollar</option>
                    <option value="IDR">IDR - Indonesian Rupiah</option>
                    <option value="EUR">EUR - Euro</option>
                    <option value="JPY">JPY - Japanese Yen</option>
                    <option value="GBP">GBP - British Pound</option>
                    <!-- Add more currency options here as needed -->
                </select>
            </div>

            <div id="result-container" class="result-container">
                <!-- Result will be displayed here -->
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/convert', methods=['GET'])
def convert():
    try:
        amount = float(request.args.get("amount", 1))
        from_currency = request.args.get("from_currency", "IDR").upper()
        to_currency = request.args.get("to_currency", "USD").upper()
        converted_amount = convert_currency(amount, from_currency, to_currency)

        # Format the amount with a period as the thousand separator
        formatted_amount = "{:,.0f}".format(amount).replace(",", ".")
        
        # Format the converted amount similarly
        formatted_converted_amount = "{:,.0f}".format(converted_amount).replace(",", ".")

        return jsonify({
            "formatted_amount": formatted_amount,
            "formatted_converted_amount": formatted_converted_amount
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
