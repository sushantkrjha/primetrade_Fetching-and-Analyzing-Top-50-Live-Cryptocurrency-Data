import schedule
import time
import subprocess

def update_data():
    print("Updating Excel data...")
    subprocess.run(["python3", "fetch_crypto.py"])

# Schedule to run every 5 minutes
schedule.every(5).minutes.do(update_data)

if __name__ == "__main__":
    print("Scheduler started. Updating every 5 minutes...")
    update_data()  # Run once before scheduling
    while True:
        schedule.run_pending()
        time.sleep(60)
