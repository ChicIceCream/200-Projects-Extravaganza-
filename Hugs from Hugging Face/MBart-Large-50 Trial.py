import requests
from dotenv import load_dotenv
load_dotenv()
import os

API_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Gujarati text to summarize
text = "મશીન લર્નિંગએ ડેટા આધારિત અંદાજો અને ઑટોમેશનને સક્ષમ બનાવીને અનેક ઉદ્યોગોમાં પરિવર્તન લાવ્યું છે. તે જ વિસ્તાર પૈકીનો એક છે આરોગ્યસંભાળ, જ્યાં મશીન લર્નિંગ અલ્ગોરિધમ્સ દ્વારા હવે આરોગ્યસંભાળ પ્રદાતાઓને રોગચાળો પહેલાંથી આગાહી કરવા, સારવાર યોજના વ્યક્તિગત બનાવવી અને દર્દીના ડેટાના વિશાળ પ્રમાણને વધુ કાર્યક્ષમતાથી વિશ્લેષણ કરવું શક્ય બન્યું છે. વધારામાં, છબી ઓળખાણમાં મશીન લર્નિંગના अनुप્રયોગો શોધખોળમાં પ્રગતિ તરફ દોરી જાય છે, ખાસ કરીને રેડિયોલોજી જેવા ક્ષેત્રોમાં, જ્યાં મોડલ્સ ડૉક્ટર્સને ચિકિત્સાકીય છબીઓમાં અનિયમિતતાઓ ઓળખવામાં મદદરૂપ થાય છે. તેમ છતાં, મશીન લર્નિંગમાં વિસંગતતાઓ અને ડેટા ગોપનીયતાની ખાતરી કરવા જેવી પડકારોનો સામનો કરવો પડે છે."

# Send a request to the Hugging Face API for summarization
response = requests.post(
    "https://api-inference.huggingface.co/models/facebook/mbart-large-50",
    headers=headers,
    json={"inputs": text}
)

# Check if the response is successful
if response.status_code == 200:
    # Try to access the generated text in the response
    result = response.json()
    summary = result
    print("Summary:", summary)
else:
    # Print the error if the request was unsuccessful
    print("Error:", response.status_code, response.json())