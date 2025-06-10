try:
    from reportlab.lib.pagesizes import letter
    print("ReportLab import successful")
except ImportError as e:
    print(f"ReportLab import failed: {e}")

try:
    import docx
    print("docx import successful")
except ImportError as e:
    print(f"docx import failed: {e}")

try:
    import flask
    print("Flask import successful")
except ImportError as e:
    print(f"Flask import failed: {e}")