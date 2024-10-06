from bs4 import BeautifulSoup
import cloudscraper
import uuid
import os

class FileShare:
	def __init__(self):
		self.scraper = cloudscraper.create_scraper()

	def _set_auth(self):
		response = self.scraper.get("https://file.com.ru/")
		response.raise_for_status()
		return response

	def _get_csrf_token(self):
		response = self._set_auth()
		soup = BeautifulSoup(response.text, 'html.parser')
		csrf_token_meta = soup.find('meta', attrs={'name': 'csrf-token'})
		if csrf_token_meta:
			csrf_token = csrf_token_meta['content']
			return csrf_token
		return None

	def upload_file(self, file, password="", auto_delete=0):
		csrf_token = self._get_csrf_token()
		dzuuid = str(uuid.uuid4())
		if not os.path.exists(file):
			raise FileNotFoundError(f"FileNotFoundError: {file}")

		file_size = os.path.getsize(file)
		chunk_size = 5242880  # 5 MB
		total_chunks = (file_size // chunk_size) + (1 if file_size % chunk_size else 0)

		with open(file, 'rb') as f:
			for chunk_index in range(total_chunks):
				chunk_data = f.read(chunk_size)
				if not chunk_data:
					break
				
				data = {
					"dzuuid": dzuuid,
					"dzchunkindex": chunk_index,
					"dztotalfilesize": file_size,
					"dzchunksize": len(chunk_data),
					"dztotalchunkcount": total_chunks,
					"dzchunkbyteoffset": chunk_index * chunk_size,
					"size": len(chunk_data),
					"password": str(password),
					"upload_auto_delete": int(auto_delete),
				}

				files = {"file": (os.path.basename(file), chunk_data, "application/octet-stream")}

				headers = {
					"cookie": "; ".join([f"{key}={value}" for key, value in self.scraper.cookies.get_dict().items()]),
					"x-csrf-token": csrf_token
				}
				response = self.scraper.post("https://file.com.ru/upload", headers=headers, files=files, data=data)
				response.raise_for_status()
				if chunk_index >= total_chunks - 1:
					return response.json()

	def download(self, id, filename=None):
		csrf_token = self._get_csrf_token()
		headers = {
					"cookie": "; ".join([f"{key}={value}" for key, value in self.scraper.cookies.get_dict().items()]),
					"x-csrf-token": csrf_token
				}

		download_id = id.split("download_")[1] if "download_" in id else id
		resp = self.scraper.post(f"https://file.com.ru/{download_id}/download/create", headers=headers)
		
		file = resp.json()["download_link"].split("/")[-1]
		exc = file.split('.')[1]
		filen = file.split('.')[0]

		with open(f"{filename}.{exc}" if filename else f"{filen}.{exc}", "wb") as newfile:
			response = self.scraper.get(resp.json()["download_link"])
			response.raise_for_status()
			newfile.write(response.content)
			return {"name": filen, "exc": exc, "fullname": file, "customName": filename + f".{exc}", "download": True}