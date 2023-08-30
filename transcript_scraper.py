from bs4 import BeautifulSoup
import requests
import re
from urllib import request
from urllib.request import Request, urlopen
import os
from pdfminer.six import extract_text
import slate3k as slate

 # generates a dictionary of appropriate transcript paths
 # if you already have the text data, set path_to_local_txt to True. 
link_to_file_on_website = True
path_to_local_pdf = False
path_to_local_txt = False

if link_to_file_on_website:
    base_url = "https://www.federalreserve.gov/monetarypolicy/"
if path_to_local_pdf or path_to_local_txt:
    base_directory = "./feddata/"

transcript_links = {}
for year in range(2008, 2009): # from 1982 - 2008
    
    if link_to_file_on_website:
        path = "fomchistorical" + str(year) + ".htm"
        html_doc = requests.get(base_url + path)
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        links = soup.find_all("a", string=re.compile('Transcript .*'))
        link_base_url = "https://www.federalreserve.gov"
        transcript_links[str(year)] = [link_base_url + link["href"] for link in links]
        
    elif path_to_local_pdf or path_to_local_txt:
        files = []
        path_to_folder = base_directory + str(year)
        new_files = os.walk(path_to_folder)
        for file in new_files:
            for f in file[2]:
                if path_to_local_pdf:
                    if f[-3:] == "meeting.pdf":
                        files.append(str(file[0]) + "/" + f)
                elif path_to_local_txt:
                    if f[-11:] == "meeting.txt":
                        files.append(str(file[0]) + "/" + f)
        transcript_links[str(year)] = files
    print("Year Complete: ", year)

all_transcripts = []

for year in transcript_links.keys():
    if not os.path.exists("./feddata/" + year):
        os.makedirs("./feddata/" + year)
    for link in transcript_links[year]:
        #print(link)
        response = Request(str(link), headers={"User-Agent": "Mozilla/5.0"})
        name = re.search("[^/]*$", str(link))
        #print(link)
        all_transcripts.append("./feddata/" + year + "/" + name.group())
        with open("./feddata/" + year + "/" + name.group(), 'wb') as f:
            f.write(urlopen(response).read())
        print("file uploaded")

print(all_transcripts)

for pdf_transcript in all_transcripts:
    reader = PdfReader(pdf_transcript)
    len_ = len(reader.pages)
    pages = reader.pages[len_+1]
    text = pages.extract_text()
    print(text)

# create list of all paths and sort in increasing order
# sorted_transcripts = []
# for linkset in transcript_links.values():
#     sorted_transcripts += linkset
# sorted_transcripts = sorted(sorted_transcripts)
# print("Number of Documents", len(sorted_transcripts))

# print(sorted_transcripts)
        


