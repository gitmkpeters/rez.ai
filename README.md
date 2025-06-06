# rez.ai 🚀

An AI-powered LinkedIn automation prototype built in Flask.

## 🔄 Dual-Mode App (Simulated vs Live)

Toggle between **simulated development mode** and **real LinkedIn API mode** using a `.env` flag.

### .env File
```env
SIMULATED_MODE=true
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_secret
LINKEDIN_REDIRECT_URI=http://localhost:5000/callback

