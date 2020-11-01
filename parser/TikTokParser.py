from TikTokApi import TikTokApi
import urllib.request
import json
import re
import os
import subprocess
import datetime
import pickle
import shutil

PATH = "D:\home\study\practice\datasets"
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
               "naturetimelapse" : 0,
               "dawn" : 0
               }
SELECT_SIZES = {(576, 1024),
                (540, 960),
                (720, 1280)}

DELAY = 0
BATCH = 100
N_FRAMES = 30
N_SEQUENCES = 5
  
def get_tags(tok):
    text = tok["itemInfos"]["text"]
    regex = "#(\w+)"
    return set(re.findall(regex, text))

def get_size(tok):
    width = tok["itemInfos"]["video"]["videoMeta"]["width"]
    height = tok["itemInfos"]["video"]["videoMeta"]["height"]
    return width, height

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

def remove_duplicates(toks):
    unique = []
    for t in toks:
        add = True
        for u in unique:
            if t["itemInfos"]["id"] == u["itemInfos"]["id"]:
                add = False
                break
        if (add):
            unique.append(t)
    return unique

def update_toks(path_to_toks):
    g_toks = read_toks(PATH + path_to_toks + "\\toks")
    n_toks = []

    remove_duplicates(g_toks)
    for tok in g_toks:
        id = str(tok["itemInfos"]["id"])
        if os.path.isfile(PATH + path_to_toks + "\\" + id + ".mp4"):
            n_toks.append(tok)

    print(len(n_toks))
    print("Save it?")
    if str(input()) == "y":
        save_toks(n_toks, PATH + path_to_toks + "\\toks")

def find_toks(tag, count):
    toks = api.byHashtag(tag, count=count, after=SEARCH_TAGS[tag])
    SEARCH_TAGS[tag] += count
    print(tag + ": " + str(len(toks)) + " found")
    return toks

def select_toks(toks, num=2):
    selected_toks = []
    for tok in toks:
        tags = get_tags(tok)
        inter = len(set(SEARCH_TAGS.keys()).intersection(tags))
        w, h = get_size(tok)
                   
        if (inter >= num and SELECT_SIZES.issuperset({(w, h)}) ):
            selected_toks.append(tok)
    return selected_toks

def download_toks(toks, subdir=""):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Referer', 'https://www.tiktok.com/foryou')]
    urllib.request.install_opener(opener)
    
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
        if os.path.isfile(PATH  + subdir + "\\"+ str(id) + ".mp4"):
            continue
        with open((PATH  + subdir + "\\"+ str(id) + ".mp4"), "wb") as f_video:
            f_video.write(response.read())
            
    return subdir

def videos_to_frames(path_to_videos, path_to_frames):
    
    toks = read_toks(path_to_videos + "\\toks")
    toks = remove_duplicates(toks)

    if os.path.isfile(PATH + path_to_frames + "\\toks"):
        print("ERROR: path_to_frames shoulde be empty")
        return
    save_toks(toks, path_to_frames + "\\toks")
    
    for tok in toks:
        id = tok["itemInfos"]["id"]
        video_name = str(id) + ".mp4"
        if not os.path.isfile(PATH + path_to_videos + "\\" + video_name):
            continue
        if not os.path.isdir(PATH + path_to_frames):
            os.mkdir(PATH + path_to_frames)
        else:
            pass
            #implement recreation of folder
            
        os.mkdir(PATH + path_to_frames + "\\" + str(id))

        command = "ffmpeg -i {0} -vf scale=540:-1 -qscale:v 2 {1}\%06d.jpg".format(\
                   PATH + path_to_videos + "\\" + video_name,
                   PATH + path_to_frames + "\\" + str(id))

        CREATE_NO_WINDOW = 0x08000000
        output = subprocess.run(command, shell=True, capture_output=True,
                                creationflags=CREATE_NO_WINDOW)
        print(output.stderr.decode("utf-8"))

def frames_to_sequences(path_to_frames, path_to_sequences, n_frames=N_FRAMES, n_sequences=N_SEQUENCES):
    toks = read_toks(path_to_frames + "\\toks")
    toks = remove_duplicates(toks)

    i = 1000000
    for tok in toks:
        id = tok["itemInfos"]["id"]
        frames_name = str(id)

        #implement checking
        if not os.path.isdir(PATH + path_to_frames + "\\" + frames_name):
            continue
        if not os.path.isdir(PATH + path_to_sequences):
            os.mkdir(PATH + path_to_sequences)
        else:
            pass
            #implement recreation of folder
        
        images = os.listdir(PATH + path_to_frames + "\\" + frames_name)
        N = n_frames*n_sequences
        a = (len(images) - N)//2
        b = a + n_frames
        sequences = [images[a + n_frames*j : b + n_frames*j] for j in range (0, n_sequences)]

        for sequence in sequences:
            os.mkdir(PATH + path_to_sequences + "\\" + str(i))
            for image in sequence:
                shutil.copy(PATH + path_to_frames + "\\" + frames_name + "\\" + image,
                            PATH + path_to_sequences + "\\" + str(i) + "\\" + image)
            i += 1

def frames_to_single_sequences(path_to_frames, path_to_sequences, n_frames=150):
    toks = read_toks(path_to_frames + "\\toks")
    toks = remove_duplicates(toks)

    i = 1000000
    for tok in toks:
        id = tok["itemInfos"]["id"]
        frames_name = str(id)

        #implement checking
        if not os.path.isdir(PATH + path_to_frames + "\\" + frames_name):
            continue
        if not os.path.isdir(PATH + path_to_sequences):
            os.mkdir(PATH + path_to_sequences)
        else:
            pass
            #implement recreation of folder
        
        images = os.listdir(PATH + path_to_frames + "\\" + frames_name)
        n_frames = min(len(images), n_frames)
        a = (len(images) - n_frames)//2
        b = a + n_frames
        sequence = images[a : b]

        os.mkdir(PATH + path_to_sequences + "\\" + str(i))
        for image in sequence:
                shutil.copy(PATH + path_to_frames + "\\" + frames_name + "\\" + image,
                            PATH + path_to_sequences + "\\" + str(i) + "\\" + image)
        i += 1


api = TikTokApi(debug=True, request_delay=DELAY)

#implement frames_to_video

#implement frames_to_sequences

"""
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
            to_frames(path_from, path_to)
        except FileExistsError:
            pass
        try:
            os.mkdir(path_seqs)
        except FileExistsError:
            pass
        
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
                shutil.copy(path_to + "\\" + frame, path_seq + frame)
"""

'''
    def to_frames(path_from, path_to):
        os.system("ffmpeg -r 1 -i {0} -r 1 {1}".format(path_from, path_to + "\\%06d.jpg"))

        use_fmp(tok["itemInfos"]["video"]["videoMeta"]["width"],
                tok["itemInfos"]["video"]["videoMeta"]["height"],
                tok["itemInfos"]["video"]["videoMeta"]["duration"],
                PATH + subdir + "\\" + str(tok["itemInfos"]["id"]) + ".mp4",
                PATH + subdir + "_ed" + "\\"  + str(tok["itemInfos"]["id"]) + "_ed" + ".mp4")

        def use_fmp(width, height, duration, path_from, path_to):
        print(path_from)
        print(path_to)
        input = fmp.input(path_from)
        video = input.video
        out = fmp.output(video, path_to)
        out.run_async()
'''



