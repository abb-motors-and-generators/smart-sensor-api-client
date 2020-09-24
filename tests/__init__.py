import os

from dotenv import load_dotenv, find_dotenv
SETTING_FILE_PATH = os.getcwd() + '\\settings.yaml'

def setup_test_environment():
    load_dotenv(find_dotenv())

    with open(SETTING_FILE_PATH, 'w') as f:
        debug_line = "debug: yes" if os.getenv("DEBUG") else "debug: yes"
        api_url_line = "api_url: " + os.getenv("SMART_SENSOR_API_URL", "")
        api_key_line = "api_key: " + os.getenv("SMART_SENSOR_API_KEY", "")
        proxy_http_line = "proxy: " + os.getenv("PROXY", "")
        f.write('{}\n{}\n{}\n{}\n'.format(debug_line, api_url_line, api_key_line, proxy_http_line))



