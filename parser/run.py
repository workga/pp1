from TikTokParser import *
import operator
import os
import json

#videos_to_frames("\\videos\\train_videos", "\\frames\\train_frames")
#now you have to generate maps
#frames_to_single_sequences("\\sources\\frames\\test_frames", "\\test_30frames\\test_B", n_frames=30)
#frames_to_single_sequences("\\sources\\maps\\test_maps", "\\test_30frames\\test_A", n_frames=30)

frames_to_sequences("\\sources\\frames\\train_frames", "\\dataset_small_7\\train_B", n_frames=30, n_sequences=5)
frames_to_sequences("\\sources\\maps\\train_maps", "\\dataset_small_7\\train_A", n_frames=30, n_sequences=5)

#frames_to_sequences("\\sources\\frames\\train_frames", "\\dataset\\train_B")
#frames_to_sequences("\\sources\\maps\\train_maps", "\\dataset\\train_A")




"""
#names of folders by tags

names = ("sunsettimelapse_131",
        "sunset_190",
        "timelapse_66",
        "timelapsevideos_4",
        "sunsetting_55",
        "skytimelapse_53",
        "sky_232",
        "timelaspechallenge_22",
        "clouds_336",
        "ocean_526",
        "sunrising_51",
        "thunderstorm_104",
        "nature_305",
        "dusk_403",
        "naturetimelapse_10",
        "dawn_90",
        "sunrise_368",
        "sunsetchallenge_763")
"""


"""
#print total duration

g_toks = read_toks("\\DS_selected_videos_good\\toks")
sum = 0
for tok in g_toks:
    dur = tok["itemInfos"]["video"]["videoMeta"]["duration"]
    print(dur)
    sum += dur
print(sum)
"""

"""
#update directory

g_toks = read_toks("\\DS_selected_videos_best\\toks")

n_toks = []
for tok in g_toks:
    id = str(tok["itemInfos"]["id"])
    if os.path.isfile(PATH + "\\DS_selected_videos_best\\" + id + ".mp4"):
        n_toks.append(tok)

print(len(n_toks))
print("it is not saved yet")
#save_toks(n_toks, "\\DS_selected_videos_best\\toks")
"""



"""
#downloading

tags = ("sunsettimelapse",
        "sunset",
        "timelapse",
        "timelapsevideos",
        "sunsetting",
        "skytimelapse",
        "sky",
        "timelaspechallenge",
        "clouds",
        "ocean",
        "sunrising",
        "thunderstorm",
        "nature",
        "dusk",
        "naturetimelapse",
        "dawn")

N = 763 + 368
for tag in tags:
    g_toks = find_toks(tag, 2000)
    s_toks = select_toks(g_toks)
    l = len(s_toks)
    N += l
    path = "\\" + tag + "_" + str(l)
    download_toks(s_toks, path)
print("DOWNLOADED: " + str(N))

"""



"""
#print table of sizes

g_toks = read_toks("\\tags\\all")

s_toks = select_toks(g_toks)
print(len(s_toks))

sizes = {}
for tok in s_toks:
    w, h = get_size(tok)
    name = str(w) + ", " + str(h)
    if name in sizes:
        sizes[name] += 1
    else:
        sizes[name] = 1
        
for v in sorted(sizes.items(), key=operator.itemgetter(1))[::-1]:
    print(v)
"""

