import os, sys, tempfile, warnings

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
# Isolated throw-away database: tests never touch the real agrismart.db.
_tmp = tempfile.mkdtemp(prefix="agrismart_test_")
os.environ["AGRISMART_DATABASE_URL"] = f"sqlite:///{os.path.join(_tmp, 'test.db')}"
os.environ["AGRISMART_JWT_SECRET"] = "test-secret"
os.environ["GEMINI_API_KEY"] = ""
