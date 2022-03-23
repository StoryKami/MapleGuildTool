import distance as dist
from jamo import h2j, j2hcj

def get_similarity(str1, str2):
    str1_ = j2hcj(h2j(str1))
    str2_ = j2hcj(h2j(str2))
    lev_dist = dist.levenshtein(str1_, str2_, normalized=True)
    sorensen_dist = dist.sorensen(str1_, str2_)

    return 1 - min(lev_dist, sorensen_dist)


def get_similarities(char1, char2):
    sim_dict = {}
    sim_dict['닉네임 유사도'] = get_similarity(char1['닉네임'], char2['닉네임'])
    sim_dict['직업 유사도'] = get_similarity(char1['직업'], char2['직업'])
    sim_dict['레벨 유사도'] = get_similarity(str(char1['레벨']), str(char2['레벨']))
    sim_dict['tot_sim'] = sim_dict['닉네임 유사도'] * 0.6 + sim_dict['직업 유사도'] * 0.2 + sim_dict['레벨 유사도'] * 0.2
    return sim_dict

def sim_valid(sim_dict):
    if sim_dict['tot_sim'] < 0.3:
        return False
    if sim_dict['닉네임 유사도'] < 0.3:
        return False
    return True
