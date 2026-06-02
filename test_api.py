import requests

URL = "http://127.0.0.1:5000/api/predict"

# ⚠️ COUNT THEM: This is exactly 15 answers (values 1 to 5) for your model!
fake_user_answers = [4, 2, 5, 5, 1, 4, 3, 2, 4, 5, 2, 4, 2, 4, 3]

payload = {"answers": fake_user_answers}

print("--- TESTING YOUR 15-QUESTION SYSTEM FROM SCRATCH ---")
try:
    response = requests.post(URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"\n API Connection: SUCCESS")
        print(f"Dominant Personality Type: {result.get('predicted_personality')}\n")
        print(" --- ALL FIVE TRAITS PERCENTAGES ---")
        for trait, score in result.get('trait_scores_percentage', {}).items():
            print(f" * {trait}: {score}%")
        print("------------------------------------")
    else:
        print(f" Server Error! Status Code: {response.status_code}")
        print(f"Details: {response.text}")
except Exception as e:
    print(f" Failed to reach backend: {str(e)}")