from flask import Flask, redirect, request, session, url_for, render_template
import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Environment vars
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
SIMULATED_MODE = os.getenv("SIMULATED_MODE", "true").lower() == "true"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    encoded_redirect_uri = urllib.parse.quote(REDIRECT_URI, safe='')

    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={encoded_redirect_uri}"
        f"&scope=r_liteprofile%20r_emailaddress%20w_member_social"
    )

    print(f"[{'SIM' if SIMULATED_MODE else 'LIVE'}] Redirecting to LinkedIn: {auth_url}")
    return redirect(auth_url)

@app.route("/callback")
def callback():
    if SIMULATED_MODE:
        access_token = "DUMMY_ACCESS_TOKEN_1234567890"
        session["access_token"] = access_token
        return f"Simulated access token stored: {access_token[:12]}..."
    else:
        code = request.args.get("code")
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(token_url, data=data, headers=headers)
        token_json = response.json()

        access_token = token_json.get("access_token")
        if not access_token:
            return f"OAuth failed. Response: {token_json}", 400

        session["access_token"] = access_token
        return f"Access token: {access_token[:12]}... stored in session"

@app.route("/profile")
def profile():
    access_token = session.get("access_token")
    if not access_token:
        return "You must log in with LinkedIn first.", 401

    if SIMULATED_MODE:
        # Simulated response
        profile_data = {
            "localizedFirstName": "Mike",
            "localizedLastName": "Peterson",
            "headline": "Developer • AI Builder • Database Expert",
            "emailAddress": "jprflipside@gmail.com"
        }
    else:
        # Real API calls
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        profile_url = "https://api.linkedin.com/v2/me"
        email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"

        profile_resp = requests.get(profile_url, headers=headers)
        email_resp = requests.get(email_url, headers=headers)
        profile_data = profile_resp.json()
        email_data = email_resp.json()

        profile_data = {
            "localizedFirstName": profile_data.get("localizedFirstName", ""),
            "localizedLastName": profile_data.get("localizedLastName", ""),
            "headline": profile_data.get("headline", {}).get("localized", {}).get("en_US", ""),
            "emailAddress": email_data.get("elements", [{}])[0].get("handle~", {}).get("emailAddress", "")
        }

    return (
        f"<h2>LinkedIn Profile ({'Simulated' if SIMULATED_MODE else 'Live'})</h2>"
        f"<p><strong>Name:</strong> {profile_data['localizedFirstName']} {profile_data['localizedLastName']}</p>"
        f"<p><strong>Headline:</strong> {profile_data['headline']}</p>"
        f"<p><strong>Email:</strong> {profile_data['emailAddress']}</p>"
    )

@app.route("/post")
def post_to_linkedin():
    access_token = session.get("access_token")

    if not access_token:
        return "You must log in with LinkedIn first.", 401

    if SIMULATED_MODE:
        # Simulated post output
        post_data = {
            "author": "urn:li:person:1234567890",
            "text": "Testing post from rez.ai — automation is coming!"
        }

        print("✅ [Simulated Post]")
        print(post_data)
        return "✅ Simulated post created successfully!"
    else:
        # Real LinkedIn UGC post
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        author_urn = "urn:li:person:YOUR_REAL_LINKEDIN_ID"  # Replace with actual ID from /me
        #TODO - This is for real use, need to fetch the author urn dynamically 
        #me_resp = requests.get("https://api.linkedin.com/v2/me", headers=headers)
        #author_urn = "urn:li:person:" + me_resp.json().get("id")


        post_data = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": "Testing post from rez.ai — automation is coming!"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=post_data)
        if response.status_code != 201:
            return f"❌ Post failed: {response.status_code} - {response.text}", 400

        return "✅ Real LinkedIn post submitted!"
   
if __name__ == "__main__":
    app.run(debug=True)