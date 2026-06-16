from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os

load_dotenv()

kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

# Step 1 - Generate login url
print("Login here: ", kite.login_url())

# Step 2 - Get request token from the redirect url after login
request_token = input("Paste your request token here: ")

# Step 3 - Generate session and set access token
data = kite.generate_session(
    request_token,
    api_secret=os.getenv("KITE_API_SECRET")
)

kite.set_access_token(data["access_token"])
print("Authentication Success!!")

profile = kite.profile()
print(f"\n Welcome {profile["user_name"]}")
print(f"\n User ID : {profile["user_id"]}")

holdings = kite.holdings()
print(f"Your Holdings are {len(holdings)}")