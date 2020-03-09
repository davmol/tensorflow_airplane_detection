import cv2
import numpy as np
import csv
from time import sleep
import system_stats


results = dict()

resolutions = {"0.3": (640,480), "800x600": (800,600), "1024x768": (1024,768), "1":(1280,960), "2":(1600,1200), "3": (2048,1536), "4": (2240,1680), "5": (2560,1920 ), "6":(3032,2008), "7":(3072,2304 ), "8": (3264,2448)}

for format, res in resolutions.items():

    video = cv2.VideoCapture(0)
    video.set(6, 1196444237) # MJPEG
    video.set(3,res[0])
    video.set(4,res[1])

    i = 0
    frame_rates = []

    while i < 100:
        e1 = cv2.getTickCount()
        fps = video.get(5)
        ret, frame = video.read()
        cv2.imshow("frame", frame)
        e2 = cv2.getTickCount()
        freq = cv2.getTickFrequency()
        t = (e2 - e1) / freq
        frame_rate_calc = 1 / t

        #print(format, res, fps, frame_rate_calc)
        frame_rates.append(frame_rate_calc)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if i == 9:
            global cpu
            cpu = system_stats.cpu()


        i += 1




    video.release()
    cv2.destroyAllWindows()

    results.update({format: {"format": format, "width": res[0], "height": res[1], "max_fps": fps, "fps": [round(i, 2) for i in frame_rates], "fps_mean": round(np.mean(frame_rates), 2), "cpu": cpu}})

    sleep(5)



with open('fps_mean_test2.csv', 'w', newline='') as csvfile:
    fieldnames = ['format', 'width',"height",  "max_fps", "fps", "fps_mean", "cpu"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, result in results.items():
        writer.writerow(result)