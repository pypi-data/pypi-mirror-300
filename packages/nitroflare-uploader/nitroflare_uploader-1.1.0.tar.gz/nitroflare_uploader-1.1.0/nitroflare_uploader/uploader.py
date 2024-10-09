import requests
import json
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class NitroflareUploader:
    def __init__(self, user_hash):
        self.user_hash = user_hash

    def get_server_url(self):
        """
        Retrieves the server URL from Nitroflare.
        """
        try:
            response = requests.get('http://nitroflare.com/plugins/fileupload/getServer')
            response.raise_for_status()
            server_url = response.text.strip()
            return server_url
        except requests.exceptions.RequestException as e:
            raise Exception(f'Failed to get server URL: {e}')

    def upload_file(self, file_path):
        """
        Uploads a file to Nitroflare with a progress bar.

        :param file_path: The path to the file to upload.
        :return: The JSON response from the server.
        """
        server_url = self.get_server_url()
        try:
            file_size = self.get_file_size(file_path)
            with open(file_path, 'rb') as f:
                fields = {
                    'user': self.user_hash,
                    'files': (file_path, f),
                }
                encoder = MultipartEncoder(fields=fields)
                progress_bar = tqdm(total=encoder.len, unit='B', unit_scale=True, desc=f'Uploading {file_path}')

                def progress_callback(monitor):
                    progress_bar.update(monitor.bytes_read - progress_bar.n)

                monitor = MultipartEncoderMonitor(encoder, progress_callback)
                headers = {'Content-Type': monitor.content_type}

                response = requests.post(server_url, data=monitor, headers=headers)
                progress_bar.close()
                response.raise_for_status()

                result = response.json()
                return result
        except requests.exceptions.RequestException as e:
            raise Exception(f'File upload failed: {e}')
        except json.JSONDecodeError:
            raise Exception('Failed to parse JSON response.')
        except Exception as e:
            raise Exception(f'An error occurred: {e}')

    @staticmethod
    def get_file_size(file_path):
        """
        Returns the size of the file in bytes.
        """
        import os
        return os.path.getsize(file_path)

# For convenience, provide a standalone function
def upload_file(file_path, user_hash):
    uploader = NitroflareUploader(user_hash)
    return uploader.upload_file(file_path)
