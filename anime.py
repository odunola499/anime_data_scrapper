import requests
import bs4
import csv

#creating header
columns = [
    "Name",
    "Type",
    "Episode",
    "Aired",
    "Premiered",
    "Producers",
    "Studios",
    "Source",
    "Genre",
    "Demographic",
    "Theme",
    "Duration",
    "Rating",
    "Score",
    "Ranking",
    "Popularity",
    "Members"
]


fields = columns[1:12]

#creating the file
file = open("anime_data.csv",mode = "w")
writer = csv.writer(file)
writer.writerow(columns)




#get name
def get_name(page):
    name = page.find("h1",class_ = "title-name").text.strip()
    return [name]

#get type to rating
def get_type_to_rating(page,field):
    left = page.find("div",class_ = "leftside")
    divs = left.findAll("div",class_ = "spaceit_pad")
    #get first and last
    for i in divs:
        if "Type" in i.text:
            start = divs.index(i)
        if "Rating" in i.text:
            end = divs.index(i) +1
    divs = divs[start:end]
    values = {}
    values_list = []
    for div in divs:
        values[div.text.split(":")[0].strip()] = div.text.split(":")[1].strip()
    for i in field:
        if i in values.keys():
            values_list.append(values[i])
        else:
            values_list.append("empty")
    return values_list

#get score,ranking and popularity
def get_ScoreRankingPopularity(page):
    #get score
    score_to_last = []
    score = page.find("div",class_ = "score-label").text
    score_to_last.append(score)
    #get ranking
    left = page.find("div",class_ = "leftside")
    divs = left.findAll("div",class_ = "spaceit_pad")[-3:]
    for i in divs:
        try:
            score_to_last.append(i.text.split("#")[1].strip())
        except:
            score_to_last.append(i.text.split(":")[1].strip())
    return score_to_last

def anime_scrape(row):
    count = 0
    number = 0
    while number <=row:
        try:
            #get each page
            browser = requests.get(r"https://myanimelist.net/topanime.php?limit={}".format(number))
            page = bs4.BeautifulSoup(browser.text,"html.parser")
            #get the table links for each page
            table_row = page.findAll("tr")[1:]
            row_links = [row.find("a")["href"] for row in table_row]
            #enter each linkA
            for link in row_links:
                count = count + 1
                print(f"number {count}")
                browser = requests.get(link)
                page = bs4.BeautifulSoup(browser.text,"html.parser")
                total = get_name(page) + get_type_to_rating(page,fields) + get_ScoreRankingPopularity(page)
                writer.writerow(total)
            
        except:
            print(f"error at number {count}")
            count = count + 1
        number+=50
    print("saving file...")
    file.close()
    print("Done")

anime_scrape(1400)