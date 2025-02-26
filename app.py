from flask import Flask, request, jsonify, render_template
from converter import convert_currency

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['GET'])
def convert():
    try:
        amount = float(request.args.get("amount", 1))
        from_currency = request.args.get("from_currency", "IDR").upper()
        to_currency = request.args.get("to_currency", "USD").upper()
        converted_amount = convert_currency(amount, from_currency, to_currency)

        # Format the amounts with a period as the thousand separator
        formatted_amount = "{:,.0f}".format(amount).replace(",", ".")
        formatted_converted_amount = "{:,.0f}".format(converted_amount).replace(",", ".")

        return jsonify({
            "formatted_amount": formatted_amount,
            "formatted_converted_amount": formatted_converted_amount
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
