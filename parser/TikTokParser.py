from TikTokApi import TikTokApi
import browsermobproxy
import urllib.request
import json
import re
import ffmpeg as fmp
import os
import datetime
import pickle
import shutil

PATH = "D:\\DATASET\\"
SEARCH_TAGS = {"sunsettimelapse" : 0,
               "sunsetchallenge" : 0,
               "sunset" : 0,
               "timelapse" : 0,
               "timelapsevideos" : 0,
               "sunsetting" : 0,
               "sunrise" : 0,
               "skytimelapse" : 0,
               "sky" : 0,
               "timelaspechallenge" : 0,
               "clouds" : 0,
               "ocean" : 0,
               "sunrising" : 0,
               "thunderstorm" : 0,
               "nature" : 0,
               "dusk" : 0,
               "naturetimelapse" : 0
               }

SELECTION_SETS = [{"sunset"}]

DELAY = 0
BATCH = 100
N_FRAMES = 30

def find_toks(tag, count):
    toks = api.byHashtag(tag, count=count, after=SEARCH_TAGS[tag])
    SEARCH_TAGS[tag] += count
    print(tag + ": " + str(len(toks)) + " found")
    return toks
  
def get_tags(tok):
    text = tok["itemInfos"]["text"]
    regex = "#(\w+)"
    return set(re.findall(regex, text))

def get_size(tok):
    width = tok["itemInfos"]["video"]["videoMeta"]["width"]
    height = tok["itemInfos"]["video"]["videoMeta"]["height"]
    return width, height

def select_toks(toks, num=3, width=0, height=0):
    selected_toks = []
    for tok in toks:
        tags = get_tags(tok)
        inter = len(set(SEARCH_TAGS.keys()).intersection(tags))
        w, h = get_size(tok)
        if width == 0:
            width = w
        if height == 0:
            height = h
                    
        if (inter >= num and width == w and height == h):
            selected_toks.append(tok)
    return selected_toks       
    """
    selected_toks = []
    for tok in toks:
        tags = get_tags(tok)
        for val in SELECTION_SETS:
            if(tags.issuperset(val)): #проверить чтобы не повторялись! #проверить, что масштаб подходит
                selected_toks.append(tok)
                break
    return selected_toks
    """
    

def download_toks(toks, subdir=""):
    if subdir=="":
        subdir = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M")
    try:
        os.mkdir(PATH + subdir)
    except FileExistsError:
        pass

    with open((PATH + subdir + "\\" + "toks"), "wb") as f_toks:
        pickle.dump(toks, f_toks)
        
    for tok in toks:
        url = tok["itemInfos"]["video"]["urls"][0]
        id = tok["itemInfos"]["id"]
        
        request = urllib.request.Request(url, headers={"Referer" : "https://www.tiktok.com/foryou"})
        response = urllib.request.urlopen(request)

        #только если файла нет!
        with open((PATH  + subdir + "\\"+ str(id) + ".mp4"), "wb") as f_video:
            f_video.write(response.read())
            
    return subdir

def save_toks(toks, name):
    with open((PATH + name), "wb") as f_toks:
        pickle.dump(toks, f_toks)

def read_toks(name):
    with open((PATH + name), "rb") as f_toks:
        toks = pickle.load(f_toks)
    return toks

def print_toks(toks):
    for tok in toks:
        print(json.dumps(tok, indent=4))

def print_toks_whrd(toks):
    for tok in toks:
        print(tok["itemInfos"]["video"]["videoMeta"].values())

def use_fmp(width, height, duration, path_from, path_to):
    print(path_from)
    print(path_to)
    input = fmp.input(path_from)
    video = input.video
    out = fmp.output(video, path_to)
    out.run_async()

def to_frames(path_from, path_to):
    os.system("ffmpeg -r 1 -i {0} -r 1 {1}".format(path_from, path_to + "\\%03d.jpg"))
    
def edit_videos(subdir):
    try:
        os.mkdir(PATH + subdir + "_frames")
    except FileExistsError:
        pass
    
    toks = []
    with open((PATH + subdir + "\\" + "toks"), "rb") as f_toks:
        toks = pickle.load(f_toks)

    i = 1000000
    for tok in toks:
        #только если файл существует!
        id = str(tok["itemInfos"]["id"])
        path_from = PATH + subdir + "\\" + id + ".mp4"
        path_to = PATH + subdir + "_frames" + "\\" + id
        path_seqs = PATH + subdir + "_sequences" + "\\"

        if not os.path.isfile(path_from):
            continue
        
        try:
            os.mkdir(path_to)
        except FileExistsError:
            pass
        try:
            os.mkdir(path_seqs)
        except FileExistsError:
            pass
        
        to_frames(path_from, path_to)
        
        files = os.listdir(path_to)
        N = len(files)//N_FRAMES
        seqs = [ files[j*N_FRAMES : (j + 1)*N_FRAMES] for j in range(0,N)]
        for seq in seqs:
            path_seq = path_seqs + str(i) + "\\"
            try:
                os.mkdir(path_seq)
            except FileExistsError:
                pass
            i += 1
            
            for frame in seq:
                shutil.move(path_to + "\\" + frame, path_seq + frame)
                
        '''
        use_fmp(tok["itemInfos"]["video"]["videoMeta"]["width"],
                tok["itemInfos"]["video"]["videoMeta"]["height"],
                tok["itemInfos"]["video"]["videoMeta"]["duration"],
                PATH + subdir + "\\" + str(tok["itemInfos"]["id"]) + ".mp4",
                PATH + subdir + "_ed" + "\\"  + str(tok["itemInfos"]["id"]) + "_ed" + ".mp4")
        '''
    
api = TikTokApi(debug=True, request_delay=DELAY)
toks = []
selected_toks = []



