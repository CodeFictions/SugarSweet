import bs4
import requests
import csv


def read_csv(csv_file):
    with open(csv_file, newline='') as csv_file:
        file = csv.reader(csv_file, delimiter=' ', quotechar='|')
        rows = []
        for row in file:
            string_row = ""
            for char in row:
                string_row += char
            rows.append(string_row)
        return rows


def write_csv(csv_file, data):
    with open(csv_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)


def find_link(course_):
    link_ = course_.select(".content .header .card-header")[0]["href"]
    link_ = requests.get(link_)
    link_ = bs4.BeautifulSoup(link_.text, "html.parser")
    link_ = link_.find(class_="ui big inverted green button discBtn")["href"]
    link_ = requests.get(link_)
    link_ = bs4.BeautifulSoup(link_.text, "html.parser")
    link_ = link_.find(class_="text centered ui green label").find_next_sibling().get_text()
    return link_


def fetch_coupons():
    url = requests.get('https://www.discudemy.com/language/english')
    soup = bs4.BeautifulSoup(url.text, "html.parser")
    courses = soup.select("section.card")
    links = []
    for course in courses:
        label = course.find("label").getText()
        if label == "Free":
            content = course.select(".content .header .card-header")[0].getText()
            price = (course.select(".content .meta span span"))
            link = find_link(course)
            entries = read_csv('list.csv')
            if len(price) > 2 and link not in entries:
                links.append(link)
                write_csv('list.csv', link)
                """print("-------------------------------------")
                print(label)
                print(content)
                for p in price:
                    print(p.getText(), end=" ")
                print()
                print(f"Link: {link}")
                print("-------------------------------------")"""
    return links


