import time
import requests

try:
    with open("api_keys.txt", "r") as f:
        api_keys = f.readlines()
    with open("dorks.txt", "r", encoding = "utf-8") as f:
        dorks = f.readlines()
except (FileNotFoundError, PermissionError, UnicodeError) as e:
    print(e)
    exit()

results_per_page = 10
links_count = 0
api_key_index = 0
with open("links.txt", "w", encoding = "utf-8") as f:
    for dork in dorks:
        dork = dork.strip()
        links = []
        start = 0
        while links_count < 100:
            if api_key_index >= len(api_keys):
                break
            api_key = api_keys[api_key_index].strip()
            success = False
            while not success:
                try:
                    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx=56d717bd9ac1a45a3&q={dork}&start={start}"
                    response = requests.get(url, timeout = 10)
                    response.raise_for_status()
                    success = True
                except requests.exceptions.HTTPError as err:
                    if err.response.status_code == 429:
                        print(f"Request timed out {err}")
                        api_key_index +=1
                        break
                    else:
                        print(f"An HTTP error occurred: {err}")
                        break
                except requests.exceptions.ConnectionError as err:
                    print(f"A connection error occurred: {err}")
                    break
                except requests.exceptions.Timeout as err:
                    print(f"The request timed out: {err}")
                    break
                except requests.exceptions.RequestException as err:
                    print(f"An error occurred while making the request: {err}")
                    break
            items = response.json().get("items", [])
            if not items:
                break
            for item in items:
                links.append(item["link"])
                f.write(item["link"] + "\n")
                links_count += 1
            start += results_per_page
            time.sleep(1)
        links_count = 0

print("All done!")
