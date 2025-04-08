import requests

class AutoEmbed1:
    def __init__(self):
        self.video_data_list = []
        self.base_url = "https://nono.autoembed.cc/api/getVideoSource"
        self.decrypt_url = "https://nono.autoembed.cc/api/decryptVideoSource"
        self.headers = {
            'Referer': 'https://nono.autoembed.cc',
            'Origin': 'https://nono.autoembed.cc',
        }

    def scrape(self, imdb_id, media_type, title, year, season=None, episode=None):
        try:
            final_url = f"{self.base_url}?type={media_type}&id={imdb_id}"
            if media_type == "tv" and season and episode:
                final_url = f"{final_url}/{season}/{episode}"

            encoded_response = requests.get(final_url, headers=self.headers)
            encoded_response.raise_for_status()

            decrypted_response = requests.post(self.decrypt_url, json=encoded_response.json(), headers=self.headers)
            decrypted_response.raise_for_status()

            video_source = decrypted_response.json().get("videoSource")
            if video_source:
                self.video_data_list.append({
                    f"AUTOEMBED1_{len(self.video_data_list) + 1}" : video_source
                })

        except Exception as e:
            print(f"Error: {e}")

        return self.video_data_list
