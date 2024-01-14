from bs4 import BeautifulSoup

# open saved newletters page
with open('LinkedIn.html', encoding='utf-8') as html_file:
    soup = BeautifulSoup(html_file, 'html.parser')

newsletter_links = []

for link in soup.find_all('a'):
    if (link.get('href')) and ('newsletter' in link.get('href')):
        newsletter_links.append(link.get('href')) 

# remove dups
newsletter_links = list(set(newsletter_links))

# save links to text file
with open('newsletter_links.txt', 'w') as f:
    for item in newsletter_links:
        f.write(f"{item}\n")