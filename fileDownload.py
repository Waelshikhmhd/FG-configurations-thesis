import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import random

# Suppress only the single HTTPSConnectionPool warning caused by not verifying SSL certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def download_text_file(url, save_path):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully to {save_path}")
            return len(response.content)  # Return the size of the downloaded content
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

if __name__ == "__main__":
    num_requests = int(input("Enter the number of requests: "))
    times_virus_file = int(input("Enter how many times virus file should be downloaded: "))
    times_normal_file = int(input("Enter how many times normal file should be downloaded: "))
    
    url1 = f"https://192.168.17.110:443/vrs1.virus"
    url2 = f"https://192.168.17.110:443/no-virus-file"
    save_path1 = f"C:/Users/cisco/Desktop/EXD600-Yaman-Wael/Our bench by Wael/vrs1.virus"
    save_path2 = f"C:/Users/cisco/Desktop/EXD600-Yaman-Wael/Our bench by Wael/no-virus-files/no-virus-file"
    
    start_time = time.time()

    total_downloads = 0
    virus_downloads = 0
    normal_downloads = 0
    complete_requests = 0
    failed_requests = 0
    total_transferred = 0  # Initialize total transferred data

    while total_downloads < num_requests:
        # Weighted random choice between virus and normal files
        choice = random.choices([url1, url2], weights=[times_virus_file - virus_downloads, times_normal_file - normal_downloads])[0]
        if choice == url1:
            if virus_downloads < times_virus_file:
                file_size = download_text_file(choice, save_path1)
                if file_size > 0:
                    complete_requests += 1
                    total_transferred += file_size  # Add the size of the downloaded file
                else:
                    failed_requests += 1
                virus_downloads += 1
                total_downloads += 1
        else:
            if normal_downloads < times_normal_file:
                file_size = download_text_file(choice, save_path2)
                if file_size > 0:
                    complete_requests += 1
                    total_transferred += file_size  # Add the size of the downloaded file
                else:
                    failed_requests += 1
                normal_downloads += 1
                total_downloads += 1

    end_time = time.time()
    total_time = end_time - start_time
    requests_per_second = num_requests / total_time
    transferred_rate = total_transferred / total_time  # Calculate transfer rate in bytes per second

    print(f"Total requests: {num_requests}")
    print(f"Complete requests: {complete_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Requests per second: {requests_per_second:.2f}")
    print(f"Time taken for tests: {total_time:.2f} seconds")
    print(f"Total transferred: {total_transferred / (1024 * 1024):.2f} MB")  # Convert bytes to MB
    print(f"Transferred rate: {transferred_rate / (1024 * 1024):.2f} MB/s")  # Convert bytes/s to MB/s
