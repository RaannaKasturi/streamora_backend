import requests

class AutoEmbed2:
    def __init__(self):
        self.video_data_list = []
        self.base_url = "https://hin.autoembed.cc/api/getVideoSource"
        self.decrypt_url = "https://hin.autoembed.cc/api/decryptVideoSource"
        self.headers = {
            'Referer': 'https://hin.autoembed.cc/',
            'Origin': 'https://hin.autoembed.cc',
        }

    def scrape(self, imdb_id, media_type, title, year, season=None, episode=None):
        # try:
            final_url = f"{self.base_url}?type={media_type}&id={imdb_id}"
            if media_type == "tv" and season and episode:
                final_url = f"{final_url}/{season}/{episode}"

            encoded_response = requests.get(final_url, headers=self.headers)
            encoded_response.raise_for_status()

            decrypted_response = requests.post(self.decrypt_url, json=encoded_response.json(), headers=self.headers)
            decrypted_response.raise_for_status()

            data = decrypted_response.json()
            print(data)
            if isinstance(data, dict) and "audioTracks" in data:
                for i, audio_track in enumerate(data["audioTracks"], start=1):
                    label = audio_track.get("label", "Unknown")
                    file_url = audio_track.get("file")
                    if file_url and file_url not in self.video_data_list:
                        self.video_data_list.append(
                            {
                                f"AUTOEMBED2_{len(self.video_data_list)+1} ({label})": file_url
                            }
                        )
        # except Exception as e:
        #     print(f"Error: {e}")

            return self.video_data_list
