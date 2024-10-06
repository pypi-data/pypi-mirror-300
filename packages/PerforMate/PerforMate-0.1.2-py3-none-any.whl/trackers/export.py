from abc import ABC, abstractmethod

class ExportService(ABC):
    @abstractmethod
    def send_data(self, data):
        pass

class GetDataService(ExportService):
    def send_data(self, data):
        pass
        
class HTTPExportService(ExportService):
    def send_data(self, data):
        """Send data to an HTTP endpoint (define the URL and logic)."""
        print(f"Sending data to HTTP service: {data}")
        # You can use requests.post to send data, for example:
        # requests.post("https://your-api-endpoint", json=data)

class FTPExportService(ExportService):
    def send_data(self, data):
        """Send data to an FTP server (define the server and credentials)."""
        print(f"Sending data to FTP server: {data}")
        # Implement FTP logic here, e.g., using ftplib