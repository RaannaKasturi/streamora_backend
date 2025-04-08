import re
import requests
from bs4 import BeautifulSoup

class TwoEmbed:
    def __init__(self):
        self.video_data_list = []
        self.base_url = "https://uqloads.xyz/e/"
    
    def get_stream_id(self, imdb_id, media_type, title, year, season=None, episode=None):
        url = "https://www.2embed.cc/embed/"
        if media_type == "tv" and season and episode:
            url = f"{url}{imdb_id}/season-{season}-episode-{episode}"
        else:
            url = f"{url}{imdb_id}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            stream_id = soup.find('iframe')['data-src'].split('?id=')[1].split('&')[0]
            return stream_id
        else:
            print(f"Error fetching stream ID: {response.status_code}")
            return None
        
    def int_to_base(self, x, base):
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        if x < 0:
            return '-' + self.int_to_base(-x, base)
        elif x < base:
            return digits[x]
        else:
            return self.int_to_base(x // base, base) + digits[x % base]
        
    def js_obfuscation_replacer(self, p, a, c, k):
        for i in range(c - 1, -1, -1):
            if k[i]:
                base_a = format(i, 'x') if a == 16 else format(i, 'b') if a == 2 else format(i, 'o') if a == 8 else str(i)
                try:
                    base_a = self.int_to_base(i, a)
                except:
                    pass
                p = re.sub(r'\b' + re.escape(base_a) + r'\b', k[i], p)
        return p
    
    def get_pack(self, packed_data):
        p = packed_data.split("}',")[0]+"}'"
        k = "|"+packed_data.split(",'|")[1].split("'.split")[0]
        ac = packed_data.split("}',")[1].split(",'|")[0]
        a = int(ac.split(",")[0])
        c = int(ac.split(",")[1])
        return p, a, c, k.split("|")

    def extract_video_source(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all('script')
        for script in script_tags:
            script_text = str(script.string or '')
            if script_text.startswith("eval(function(p,a,c,k,e,d)"):
                p,a,c,k = self.get_pack(script_text.strip())
                data = self.js_obfuscation_replacer(p, a, c, k)
                source = data.split("\"}],image:")[0].split("[{file:\"")[1].strip()
                return source
        return None
    
    def scrape(self, imdb_id, media_type, title, year, season=None, episode=None):
        try:
            stream_id = self.get_stream_id(imdb_id, media_type, title, year, season, episode)
            if stream_id:
                video_source_url = f"{self.base_url}{stream_id}"
                response = requests.get(video_source_url, headers={
                    'Host': 'uqloads.xyz',
                    'Referer': 'https://streamsrcs.2embed.cc/',
                })
                source = self.extract_video_source(response.content)
                if source:
                    self.video_data_list.append({
                        f"TWOEMBED_{len(self.video_data_list) + 1}": source
                    })
                else:
                    print("No video source found.")
        except Exception as e:
            print(f"Error: {e}")
        return self.video_data_list
    
            
# TwoEmbed().scrape("tt14513804", "movie", "Captain America: Brave New World", "2025")