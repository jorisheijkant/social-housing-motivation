import os 
from bs4 import BeautifulSoup
import csv

jobs_folder = "output/listing"
listings = []
limit = 10000

for (folder, labels, files) in os.walk(jobs_folder):
    for file_index, file in enumerate(files):
        if file_index < limit:
            file_path = f"{jobs_folder}/{file}"
            print(f"Parsing file {file_index}")
            with open(file_path, "r") as html_file:
                soup = BeautifulSoup(html_file, 'html.parser')
                house_info_container = soup.find("div", {"id": "$b16"})
                house_text_container = soup.find("div", {"id": "$b17"})

                job_id = file.split(".")[0]
                job_title = ""
                info_text = ""

                if house_info_container:
                    job_title_item = house_info_container.find("div", {"class": "flex2"})
                    if job_title_item:
                        job_title = job_title_item.text 

                if house_text_container: 
                    info_item = house_text_container.find("div", {"class": "text-grey"})
                    if info_item: 
                        info_text = info_item.text

                if job_id and job_title:
                    listings.append({
                        "job_id": job_id,
                        "job_title": job_title, 
                        "info_text": info_text
                    })

with open("output.csv", "w") as csv_output:
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(["id", "title","info_text"])

    for job in listings:
        csv_writer.writerow([job["job_id"], job["job_title"], job["info_text"]])

print(f"All data added to the csv")
            