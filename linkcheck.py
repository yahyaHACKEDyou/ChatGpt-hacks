import requests
from bs4 import BeautifulSoup

def check_fake_link(link):
    response = requests.get(link)
    if response.status_code != 200:
        return True
    soup = BeautifulSoup(response.text, "html.parser")
    if soup.find("script"):
        return True
    if not soup.title:
        return True
    if "404" in soup.title.text.lower():
        return True
    return False

with open("links.txt") as file:
    links = file.readlines()

fake_links = []
for link in links:
    link = link.strip() + "'"
    if check_fake_link(link):
        fake_links.append(link)

with open("fake.txt", "w") as file:
    for fake_link in fake_links:
        file.write(fake_link + "\n")
