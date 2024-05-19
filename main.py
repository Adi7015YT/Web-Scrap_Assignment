#Custom
import Functions.GetURLParams as gup
import Functions.Export_to_Excel as ex

#Third Party
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlwt

#Built-in
from datetime import date,datetime
from collections import defaultdict
import os

workbook = xlwt.Workbook()
count = 0
all_data = []

while True:
    count+=1
    final_params = gup.get_URL_params()
    URL = 'https://internshala.com/'+final_params.lower()
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    max_pages = int(soup.find(id='total_pages').text.strip())
  
    limit = int(input("How many pages you would like to get? Max Pages ({max_pages})\n".format(max_pages=max_pages)))
    if limit > max_pages:
        limit = max_pages
        print("Pages Set to Maximum pages present")
    elif limit <= 0:
        limit = 1
        print("Pages set to 1")
        
    flag = 0
    if limit > 1:
        flag = input('Different pages on different sheets?(Default: Yes) | 1: No\n')

    for i in range(limit):
            current_url = URL + f'/page-{i + 1}'
            page = requests.get(current_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            intern_titles = soup.find_all(class_='cta_container')
            if not intern_titles:
                print('No Results Found....')
                exit()

            print(f'--------------Scraping Page {i + 1} -----------------')
            for title in intern_titles:
                elem = title.find('a')
                elim = elem.get('href')
                sub_URL = 'https://internshala.com/' + elim

                sub_page = requests.get(sub_URL)
                sub_soup = BeautifulSoup(sub_page.content, 'html.parser')

                data = {
                    'internship_title': sub_soup.find(class_='heading_4_5 profile').text.strip(),
                    'company': sub_soup.find(class_='heading_6 company_name').find('a').text.strip(),
                    'location': sub_soup.find(id='location_names').text.strip(),
                }

                info = sub_soup.find(class_='internship_other_details_container')
                other_details = info.find_all(class_='item_body')

                data.update({
                    'duration': other_details[1].text.strip(),
                    'stipend': other_details[2].text.strip(),
                    'apply_by': other_details[3].text.strip(),
                    'applicants': sub_soup.find(class_='applications_message').text.strip(),
                })

                try:
                    skills_raw = sub_soup.find(class_='heading_5_5', string='Skill(s) required')
                    skills_raw = skills_raw.findNext(class_='round_tabs_container')
                    data['skills'] = ', '.join([i.text.strip() for i in skills_raw.find_all(class_='round_tabs')])
                except (IndexError, AttributeError):
                    data['skills'] = ''

                try:
                    perks_raw = sub_soup.find(class_='heading_5_5', string='Perks')
                    perks_raw = perks_raw.findNext(class_='round_tabs_container')
                    data['perks'] = ', '.join([i.text.strip() for i in perks_raw.find_all(class_='round_tabs')])
                except (IndexError, AttributeError):
                    data['perks'] = ''

                try:
                    data['openings'] = sub_soup.find_all(class_='text-container')[-1].text.strip()
                except IndexError:
                    data['openings'] = ''
                
                data.update({
                    'link': sub_URL
                })

                all_data.append(data)

    df = pd.DataFrame(all_data)

    if flag == '1':
            sheet_name = f"Sheet - {count}"
            sheet = workbook.add_sheet(sheet_name)
            ex.write_header(sheet)
            params = df.to_dict(orient='list')
            ex.write_body(params, sheet)
    else:
            for i in range(limit):
                sheet_name = f"Sheet - {count}|Page - {i + 1}"
                sheet = workbook.add_sheet(sheet_name)
                ex.write_header(sheet)
                params = df.iloc[i * len(intern_titles):(i + 1) * len(intern_titles)].to_dict(orient='list')
                ex.write_body(params, sheet)

    ex.save_and_export(workbook)
