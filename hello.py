import streamlit as st
import os
import requests
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()
INSTANCE_ID = os.getenv("INSTANCE_ID")
TOKEN = os.getenv("TOKEN")

# Separate male and female rishtas
male_rishtas = [
    {"name": "Muneeb", "age": 22},
    {"name": "Muhammad Ubaid Hussain", "age": 25},
    {"name": "Azan", "age": 19},
    {"name": "Hassan", "age": 24},
    {"name": "Zain", "age": 20},
    {"name": "Ali", "age": 23},
    {"name": "Saad", "age": 21},
    {"name": "Areeb", "age": 26},
    {"name": "Talha", "age": 22},
    {"name": "Fahad", "age": 24},
    {"name": "Junaid", "age": 23},
    {"name": "Hamza", "age": 20},
    {"name": "Daniyal", "age": 25},
    {"name": "Rehan", "age": 22},
    {"name": "Shayan", "age": 21},
    {"name": "Ibrahim", "age": 20},
    {"name": "Sameer", "age": 23},
    {"name": "Abdullah", "age": 19},
    {"name": "Usman", "age": 24},
    {"name": "Salman", "age": 26}
]

female_rishtas = female_rishtas = [
    {"name": "Ayesha", "age": 22},
    {"name": "Fatima", "age": 24},
    {"name": "Zara", "age": 23},
    {"name": "Hira", "age": 21},
    {"name": "Amna", "age": 25},
    {"name": "Iqra", "age": 20},
    {"name": "Mariam", "age": 26},
    {"name": "Noor", "age": 19},
    {"name": "Aleena", "age": 22},
    {"name": "Mahnoor", "age": 24},
    {"name": "Sana", "age": 23},
    {"name": "Laiba", "age": 21},
    {"name": "Mehwish", "age": 25},
    {"name": "Emaan", "age": 20},
    {"name": "Areeba", "age": 22},
    {"name": "Komal", "age": 26},
    {"name": "Nimra", "age": 24},
    {"name": "Bushra", "age": 23},
    {"name": "Huma", "age": 19},
    {"name": "Anum", "age": 25},
    {"name": "Sadia", "age": 21},
    {"name": "Kiran", "age": 20},
    {"name": "Sumaira", "age": 26},
    {"name": "Tuba", "age": 22},
    {"name": "Tehreem Fatima", "age": 18}
]


# Save data to CSV
def save_to_csv(name, phone, age, gender):
    data = {
        "name": [name],
        "phone": [phone],
        "age": [age],
        "gender": [gender],
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    df = pd.DataFrame(data)
    if os.path.exists("submissions.csv"):
        df.to_csv("submissions.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("submissions.csv", index=False)

# Send WhatsApp message
def send_rishta_details(name, phone, age, gender):
    if not phone.startswith("+"):
        st.error("❌ Phone number must start with + (e.g., +923001234567)")
        return None

    # Gender-based matching
    if gender == "Male":
        matched_rishtas = [p for p in female_rishtas if abs(p["age"] - age) <= 2]
    else:
        matched_rishtas = [p for p in male_rishtas if abs(p["age"] - age) <= 2]

    if not matched_rishtas:
        rishta_list = "😔 Koi rishta nahi mila aapki age ke aas paas."
    else:
        rishta_list = "\n".join([f"- {p['name']} (Age: {p['age']})" for p in matched_rishtas])

    message = (
        f"Assalam u Alaikum! \n"
        f"Apka Naam: {name}\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"📍 City: Karachi\n\n"
        f"🔎 Matching Rishtay:\n{rishta_list}\n\n"
        f"📞 Contact for more info!\n"
        f"JazakAllah ❤️"
    )

    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    payload = {
        "token": TOKEN,
        "to": phone,
        "body": message
    }

    response = requests.post(url, json=payload)
    return response

# Streamlit App Config
st.set_page_config(page_title="Rishta App", page_icon="💍", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .typewriter {
            font-family: monospace;
            overflow: hidden;
            border-right: .15em solid pink;
            white-space: nowrap;
            animation: typing 3s steps(40, end), blink-caret .75s step-end infinite;
            font-size: 24px;
            color: #C71585;
            text-align: center;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes slide {
            from {transform: translateY(30px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }

        .footer {
            text-align: center;
            color: gray;
            font-size: 12px;
        }

        .form-input {
            background-color: #fff0f5;
            padding: 8px 10px;
            border-radius: 8px;
            border: 1px solid #ddd;
            margin-bottom: 10px;
            width: 100%;
        }

        .form-label {
            font-weight: bold;
            color: #C71585;
            margin-bottom: 4px;
            display: block;
        }

        .send-button {
            background: linear-gradient(to right, #ff69b4, #ff1493);
            border: none;
            color: white;
            padding: 10px 25px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }

        .send-button:hover {
            background: linear-gradient(to right, #ff1493, #ff69b4);
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='typewriter'>💍 Welcome to My Rishta App</h1>", unsafe_allow_html=True)

# Image
st.markdown("""
    <div style="text-align: center;">
        <img 
            src="https://t4.ftcdn.net/jpg/13/42/94/23/360_F_1342942305_I2u6JyECgnfLECvVzRTfqlcOX1nVA6hW.jpg" 
            width="500" 
            style="border-radius: 10px;"
        />
    </div>
""", unsafe_allow_html=True)

# Form
with st.form("rishta_form"):
    st.markdown('<label class="form-label">👤 Your Name</label>', unsafe_allow_html=True)
    name = st.text_input("", key="name_input")

    st.markdown('<label class="form-label">📱 WhatsApp Number</label>', unsafe_allow_html=True)
    phone = st.text_input("", key="phone_input")

    st.markdown('<label class="form-label">🎂 Age</label>', unsafe_allow_html=True)
    age = st.number_input("", min_value=18, max_value=60, value=25, key="age_input")

    st.markdown('<label class="form-label">⚧️ Gender</label>', unsafe_allow_html=True)
    gender = st.selectbox("", ["Male", "Female"], key="gender_input")

    submitted = st.form_submit_button("📨 Send Rishta", use_container_width=True)

    if submitted:
        with st.spinner("⏳ Sending your rishta to WhatsApp... please wait 💖"):
            response = send_rishta_details(name, phone, age, gender)
            save_to_csv(name, phone, age, gender)
        if response and response.status_code == 200:
            st.success("✅ Rishta card sent via WhatsApp!")
            st.balloons()
            st.markdown("""
                <audio autoplay>
                  <source src="https://www.soundjay.com/button/beep-07.wav" type="audio/wav">
                </audio>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Something went wrong. Please check your number or try again.")

# Footer
st.markdown("---")
st.markdown("<div class='footer'>Made with ❤️ by Tehreem Fatima</div>", unsafe_allow_html=True)
