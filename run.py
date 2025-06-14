from app import create_app
import ssl

app = create_app()

if __name__ == "__main__":
    # For development with self-signed certificate
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=True)
    except (FileNotFoundError, ssl.SSLError):
        # Fall back to adhoc SSL if certificates aren't available
        print("Using adhoc SSL certificate (self-signed)")
        app.run(host='0.0.0.0', port=5000, ssl_context='adhoc', debug=True)
