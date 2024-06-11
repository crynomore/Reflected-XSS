import requests
import urllib.parse
import subprocess

# Constant payload file
PAYLOAD_FILE = 'payloads.txt'


# Function to check for reflected XSS
# Function to check for reflected XSS
# Function to check for reflected XSS
def check_xss(url, payloads):
    for payload in payloads:
        # Encode the payload
        encoded_payload = urllib.parse.quote(payload, safe='')
        test_url = f"{url}{encoded_payload}"

        # Send the request
        try:
            response = requests.get(test_url)
            print(f"Testing payload: {payload}")
            print(f"Test URL: {test_url}")
            print(f"Response length: {len(response.text)}")

            # Check for variations of the payload in the response
            variations = [
                payload,  # Original payload
                f"<{payload[:-1]} =\"{payload[-1]}\">",  # Payload with double quotes
                f"<{payload[:-1]} =\'{payload[-1]}\'>",  # Payload with single quotes
                f"<{payload[:-1]} = \"{payload[-1]}\">",  # Payload with spaces and double quotes
                f"<{payload[:-1]} = \'{payload[-1]}\'>"  # Payload with spaces and single quotes
            ]

            # Check if any variation of the payload is reflected in the response
            for variation in variations:
                if variation in response.text:
                    print(f"[VULNERABLE] Payload: {variation}")
                    return True

            # No variations of the payload were reflected, so not vulnerable
            print(f"[NOT VULNERABLE] Payload: {payload}")

        except requests.RequestException as e:
            print(f"Error sending request to {test_url}: {e}")

    return False


# Function to detect WAF using wafw00f command line
def detect_waf(url):
    result = subprocess.run(['wafw00f', url], capture_output=True, text=True)
    if result.returncode == 0:
        print("WAF Detection Result:")
        print(result.stdout)
    else:
        print("WAF detection failed.")
        print(result.stderr)


def main():
    # Cocky way to ask for the URL
    url = input("Alright hotshot, give me the URL to test (with the parameter placeholder): ")

    # Read payloads from the constant file
    try:
        with open(PAYLOAD_FILE, 'r') as file:
            payloads = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: Payload file '{PAYLOAD_FILE}' not found.")
        return

    # Check for reflected XSS
    print(f"Checking XSS on: {url}")
    xss_vulnerable = check_xss(url, payloads)

    if xss_vulnerable:
        print("The site is vulnerable to XSS.")
    else:
        print("No XSS vulnerability detected.")

    # Detect WAF
    print("Detecting WAF...")
    detect_waf(url)


if __name__ == "__main__":
    main()
