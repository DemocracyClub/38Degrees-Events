import os
import glob

import requests

class NoMoreEventsError(Exception): pass
class EventNotPublishedError(Exception): pass

class Scraper(object):
    def __init__(self, known_max=0):
        self.start_id = self.get_start_id()
        self.current = self.start_id
        self.known_max = known_max

    def get_start_id(self):
        paths = glob.glob('data/*')
        ids = [int(n.split('/')[1].split('.')[0]) for n in paths] or [260, ]
        return max(ids)

    def build_detail_url(self, id):
        return "https://election.38degrees.org.uk/events/{0}".format(id)

    def scrape_single(self, id):
        url = self.build_detail_url(id)
        path = "data/{0}.html".format(id)
        if os.path.exists(path):
            return path
        req = requests.get(url)
        if req.status_code == 200:
            with open(path, 'w') as f:
                f.write(req.content)
        if req.status_code == 404:
            raise NoMoreEventsError("No more events found")
        if req.status_code == 302:
            raise EventNotPublishedError("Event {0} not published yet".format(
                id
            ))

    def scrape_all(self):
        while True:
            try:
                self.scrape_single(self.current)
            except NoMoreEventsError:
                if self.current >= self.known_max:
                    print("All events found")
                    break
            except EventNotPublishedError, e:
                print(e)
            finally:
                self.current += 1



if __name__ == "__main__":
    s = Scraper(known_max=2009)
    print s.scrape_all()
