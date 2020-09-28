from TikTokParser import *

g_toks = []

for tag in SEARCH_TAGS:
    g_toks += read_toks("tags\\" + tag)
