
from skimage import io
import db_mac
from collections import defaultdict

import os
import datetime
img_dir = "/Users/david/GoogleDrive/BA/project/2020_01_X/"

brightness_values = defaultdict()

xmin = 1500
xmax = 2000
ymin = 900
ymax = 1400



def img_luminance(img_path, timestamp):

    img = io.imread(img_path)
    #shape = (img.shape)
    #x = shape[1]
    #y = shape[0]


    cropped_img = img[ymin:ymax, xmin:xmax]

    #plt.figure(figsize=(20, 10))
    #plt.subplot(121), plt.imshow(cropped_img), plt.axis('off')
    #plt.show()

    srgb  = [i.item() for i in cropped_img.mean(axis=0).mean(axis=0)]

    vrgb = [i /255 for i in srgb]

    intensity = sum(srgb)/3


    vrgb_lin = []
    for c in vrgb:
        if (c <= 0.04045):
            c / 12.92
            vrgb_lin.append(c)
        else:
            c = pow(((c + 0.055) / 1.055), 2.4)
            vrgb_lin.append(c)


    luminance = 0.2126 * vrgb_lin[0] + 0.7152 * vrgb_lin[1] + 0.0722 * vrgb_lin[2]

    #print("sRGB", sR, sG, sB)
    #print("intensity", intensity)
    #print("vRGB", vrgb)
    #print("colorCHlin", vrgb_lin)


    brightness =  {"timestamp": timestamp, "srgb": [round(i,2) for i in srgb], "vrgb": [round(i,2) for i in vrgb], "vrgb_lin": [round(i,2) for i in vrgb_lin], "intensity": round(intensity,2), "luminance": round(luminance,2)}

    return brightness

def insert_table_brightness(brightness_values):
    colnames = ["timestamp", "srgb", "vrgb", "vrgb_lin", "intensity", "luminance"]




    vals = []
    for name in colnames:
        vals.append(brightness_values[name])


    vals_str_list = ["%s"] * len(vals)
    vals_str = ", ".join(vals_str_list)
    cols = ', '.join(colnames)
    sql = """INSERT INTO public.brightness ({cols}) VALUES ({vals_str})""".format(
        cols=cols, vals_str=vals_str)
    db_mac.execute((sql, vals))


file_list = []
for root, dirs, files in os.walk(img_dir, topdown=False):
   for name in files:

       if "c_in_" in name:
           file_list.append(name)

print(file_list)
img_ts = []
sql = "select img_url, timestamp from od2 where img_url is not null"
result = db_mac.execute(sql)
for row in result:
    img_ts.append(row)


for img_t in img_ts:
    img_name = img_t[0]
    timestamp = img_t[1]

    name_ts = img_name.replace("/home/pi/Desktop/project/", "")

    pos1 = name_ts.find("2020")
    pos2 = name_ts.find(".png")
    if pos2 == -1:
        pos2 = name_ts.find(".jpg")

    name_ts = name_ts[pos1:pos2]

    for file in file_list:
        if name_ts in file:
            brightness = img_luminance(img_dir + "/" + file, timestamp)

            print(img_name)
            print(name_ts)
            print(file)
            print(brightness)
            insert_table_brightness(brightness)



if __name__ == "__main__":

    """
    https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color
    https://de.wikipedia.org/wiki/Luminanz
    https://www.zbs-ilmenau.de/pdf/script/oeffentlich/grafik/Farbraeume_CG_KHF_02_WS1314_ZBS_WEB.pdf
    
    https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color
    
    PLOTS
    https://machinelearningmastery.com/time-series-data-visualization-with-python/
    https://www.geeksforgeeks.org/python-pandas-series/
    
    Brightness is a perceptual attribute, it does not have a direct measure.
    
    Perceived lightness is measured by some vision models such as CIELAB, here L* (Lstar) is a measure of perceptual lightness, and is non-linear to approximate the human vision non-linear response curve.
    
    Luminance is a linear measure of light, spectrally weighted for normal vision but not adjusted for non-linear perception of lightness.
    
    Luma (Y´ prime) is a gamma encoded, weighted signal used in some video encodings. It is not to be confused with linear luminance.
    
    Gamma or transfer curve (TRC) is a curve that is often similar to the perceptual curve, and is commonly applied to image data for storage or broadcast to reduce perceived noise and/or improve data utilization (and related reasons).
    
    To determine perceived lightness, first convert gamma encoded R´G´B´ image values to linear luminance (L or Y ) and then to non-linear perceived lightness (L*)
    
    """