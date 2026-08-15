import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
Superkart_salesRevenue_api = Flask("Superkart_SalesRevenue")
MODEL_PATH= "SuperKart_Sales Prediction_model_v1_0.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ ERROR: Failed to load model file at {MODEL_PATH}")
    print(f"Error details: {e}")
    model = None

# Define a route for the home page
@Superkart_salesRevenue_api.get('/')
def home():
    return "Welcome to the Superkart Sales Revenue prediction API!"

# Define an endpoint to predict price for a single house
@Superkart_salesRevenue_api.post('/v1/predict')  # this is a end point which is an online processing send only one data and get result then it is online processing
def predict_store_price():
    # Get JSON data from the request
    """ this function handles POST requests to the V1/Storesales endpoint.
    it expects JSON payload containing products, stores details and returns
    the predicted sales revenue for the given input.
    """
    Product_Store_data = request.get_json()

    # Extract relevant house features from the input data
    sample = {
        'Product_Weight': Product_Store_data['Product_Weight'],
        'Product_Sugar_Content': Product_Store_data['Product_Sugar_Content'],
        'Product_Allocated_Area': Product_Store_data['Product_Allocated_Area'],
        'Product_Type': Product_Store_data['Product_Type'],
        'Product_MRP': Product_Store_data['Product_MRP'],
        'Store_Id': Product_Store_data['Store_Id'],
        'Store_Size': Product_Store_data['Store_Size'],
        'Store_Location_City_Type': Product_Store_data['Store_Location_City_Type'],
        'Store_Type': Product_Store_data['Store_Type'],
        'Product_ID_Tag': Product_Store_data['Product_ID_Tag'],
        'Product_Store_Age': Product_Store_data['Product_Store_Age']
    }


    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    try:
        if model is None:
            return jsonify({'error': 'Model is not loaded on server.'}), 500

        # Make a prediction using the trained model
        prediction = model.predict(input_data).tolist()[0]

        # Return the prediction as a JSON response
        return jsonify({'Predicted_Product_Store_Sales_Total': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define an endpoint to predict price for a batch of houses
@Superkart_salesRevenue_api.post('/v1/predictbatch')     # this is a end point which is batch processing get many reports this is not instant we need to wait to get the result.
def predict_store_price_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Add predictions to the DataFrame
    input_data['Predicted_Product_Store_Sales_Total'] = predictions

    # Convert results to dictionary
    result = input_data.to_dict(orient="records")

    return jsonify(result)

# Run the Flask app in debug mode
if __name__ == '__main__':
   Superkart_salesRevenue_api.run(debug=True)
