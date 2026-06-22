from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load the newly trained 15-question model
with open('random_forest_personality_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Items that must be flipped based on the IPIP codebook properties
REVERSE_QUESTIONS = ['OPN2', 'CSN2', 'EXT2', 'EXT4', 'AGR1', 'EST2']

#  MAKE SURE THIS LIST LOOKS EXACTLY LIKE THIS IN YOUR APP.PY 
FEATURE_NAMES = [
    'OPN1', 'OPN2', 'OPN3',
    'CSN1', 'CSN2', 'CSN5',
    'EXT1', 'EXT2', 'EXT4',
    'AGR2', 'AGR1', 'AGR4',
    'EST1', 'EST2', 'EST3'
]

@app.route('/api/predict', methods=['POST'])
def predict_personality():
    try:
        data = request.get_json()
        user_answers = data.get('answers')
        
        # Change this validation check to 15!
        if not user_answers or len(user_answers) != 15:
            return jsonify({"error": "Invalid input. Exactly 15 answers required."}), 400
        
        # Structure payload into a Pandas DataFrame
        input_df = pd.DataFrame([user_answers], columns=FEATURE_NAMES)
        
        # Apply reverse scoring
        for col in REVERSE_QUESTIONS:
            input_df[col] = 6 - input_df[col]
            
        # Extract individual prediction distributions
        probabilities = model.predict_proba(input_df)[0]
        trait_names = model.classes_
        
        personality_breakdown = {
            trait: round(float(prob) * 100, 2) 
            for trait, prob in zip(trait_names, probabilities)
        }
        
        prediction_class = model.predict(input_df)[0]
        
        return jsonify({
            "status": "success",
            "predicted_personality": prediction_class,
            "trait_scores_percentage": personality_breakdown
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)