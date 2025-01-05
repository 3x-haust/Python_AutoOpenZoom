import pyautogui
import schedule
import time
import os
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

scheduled_time = ""
zoom_link = ""

class TimeChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global scheduled_time
        global zoom_link

        if event.src_path.endswith("schedule_time.txt"):
            print(f"{datetime.datetime.now()}: schedule_time.txt 파일이 변경되었습니다.")
            new_time = read_time_from_file()

            if new_time != scheduled_time:
                scheduled_time = new_time
                print(f"{datetime.datetime.now()}: 새로운 스케줄링 시간: {scheduled_time}")
                schedule.clear() 
                schedule.every().day.at(scheduled_time).do(open_zoom)
                print(f"{datetime.datetime.now()}: 새로운 스케줄이 설정되었습니다: 매일 {scheduled_time}에 줌을 엽니다.")

        elif event.src_path.endswith("zoom_link.txt"):
            print(f"{datetime.datetime.now()}: zoom_link.txt 파일이 변경되었습니다.")
            new_link = read_zoom_link_from_file()

            if new_link != zoom_link:
                zoom_link = new_link
                print(f"{datetime.datetime.now()}: 새로운 줌 링크: {zoom_link}")

# schedule_time.txt 파일에서 시간 읽기
def read_time_from_file():
    with open('schedule_time.txt', 'r') as file:
        return file.readline().strip()
    
# zoom_link.txt 파일에서 줌 링크 읽기
def read_zoom_link_from_file():
    with open('zoom_link.txt', 'r') as file:
        return file.readline().strip()

# image_path에 해당하는 이미지를 찾아서 클릭릭
def click_button(image_path):
    try:
        button_location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if button_location is not None:
            pyautogui.click(button_location)
            print(f"{datetime.datetime.now()}: '{image_path}' 버튼을 클릭했습니다.")
            return True 
        else:
            print(f"{datetime.datetime.now()}: '{image_path}' 버튼을 찾을 수 없습니다.")
            return False
    except Exception as e:
        return False 

def open_zoom():
    print(f"{datetime.datetime.now()}: 줌을 열기 시작합니다.")
    os.startfile(zoom_link)
    time.sleep(10) 
    
    click_button("join.png")

scheduled_time = read_time_from_file()
zoom_link = read_zoom_link_from_file()
schedule.every().day.at(scheduled_time).do(open_zoom)

print(f"{datetime.datetime.now()}: 스케줄링 시작. 매일 {scheduled_time}에 줌을 엽니다.")

# txt 파일 변경 감지
event_handler = TimeChangeHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
