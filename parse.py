import glob
import json

from bs4 import BeautifulSoup
from dateutil.parser import parse

class EventParser(object):
    all_data = []

    def parse_single(self, html):
        soup = BeautifulSoup(html)
        event_info = soup.find('ul', {'class': 'fa-ul'})
        if not event_info:
            return
        # print event_info
        title = soup.find('div', {'class': 'panel-body'}).findNext('h3').text
        date = event_info.find(title="Meeting time").parent.text
        location_text = event_info.find(title="Meeting point").parent.text.strip()
        link = event_info.find(title="Link").parent.text.strip()
        description = soup.find('p', {'class': 'event-details'})
        date = parse(date)
        data = {
            'date': str(date),
            'location_text': location_text.strip(),
            'link': link,
        }

        if title.lower() != "key":
            data['title'] = title
        if description:
            data['description'] = description.text
        self.all_data.append(data)


    def parse_all(self):
        for path in glob.glob('data/*.html'):
            with open(path) as f:
                self.parse_single(f.read())
        with open('all_data.json', 'w') as f:
            f.write(json.dumps(self.all_data, indent=4))

if __name__ == "__main__":
    p = EventParser()
    p.parse_all()