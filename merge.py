import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
from collections import defaultdict
from Crolling import *
from similarity import get_similarities, sim_valid

def main():
    get = False

    if get:
        df = get_members_all_page()
        df.reset_index(inplace=True)
        df = df[['닉네임', '직업', '레벨', '직위']]
        print(df)
        df.to_csv("guild_member.csv", encoding="utf-8-sig")
        df = pd.read_csv("guild_member.csv")
        df = df[['닉네임', '직업', '레벨', '직위']]
        df.sort_values(by=['닉네임'], axis=0, inplace=True)
        df.reset_index(inplace=True, drop=True)
        df.to_csv("sorted_guild_member.csv", encoding="utf-8-sig")

    df_weekly = pd.read_csv("weekly_pnt_mod.csv", encoding="utf-8-sig")
    df_weekly = df_weekly[['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그']]
    df_weekly.reset_index(inplace=True, drop=True)
    df_guild = pd.read_csv("sorted_guild_member.csv")
    df_guild = df_guild[['닉네임', '직업', '레벨', '직위']]
    df_guild.reset_index(inplace=True, drop=True)


    merge_df_dev = pd.DataFrame(columns=['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그', '본캐', '닉네임 유사도', '직업 유사도', '레벨 유사도'])
    merge_df = pd.DataFrame(columns=['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그', '본캐'])
    new_df = pd.DataFrame(columns=['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그', '본캐'])
    del_df = pd.DataFrame(columns=['닉네임', '직업', '레벨', '본캐'])
    i = 0
    j = 0
    df_temp = pd.read_csv("weekly_pnt_mod.csv", encoding="utf-8-sig")
    df_temp = df_temp[['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그']]
    df_temp.reset_index(inplace=True, drop=True)
    temp_char = df_temp.loc[14].to_dict()
    while (i < len(df_weekly)) and (j < len(df_guild)):
        weekly_char = df_weekly.loc[i].to_dict()
        guild_char = df_guild.loc[j].to_dict()
        sim_dict_1 = get_similarities(weekly_char, guild_char)
        try:
            weekly_char_n = df_weekly.loc[i + 1].to_dict()
            sim_dict_2 = get_similarities(weekly_char_n, guild_char)
        except:
            sim_dict_2 = {'tot_sim' : -1}
        try:
            guild_char_n = df_guild.loc[j + 1].to_dict()
            sim_dict_3 = get_similarities(weekly_char, guild_char_n)
        except:
            sim_dict_3 = {'tot_sim': -1}
        if sim_valid(sim_dict_1):
            max_sim = max((sim_dict_1['tot_sim'], sim_dict_2['tot_sim'], sim_dict_3['tot_sim']))
            if sim_dict_1['tot_sim'] != max_sim:
                if sim_dict_2['tot_sim'] == max_sim:
                    i += 1
                    print(weekly_char, sim_dict_1['tot_sim'])
                    weekly_char.update({'본캐': '-신규-'})
                    new_df = new_df.append(weekly_char, ignore_index=True)
                else:
                    j += 1
                    print(guild_char, sim_dict_1['tot_sim'])
                    guild_char.update({'본캐': '-탈퇴-'})
                    guild_char.pop('직위')
                    del_df = del_df.append(guild_char, ignore_index=True)
                continue
        else:
            if sim_valid(sim_dict_2):
                i += 1
                print(weekly_char, sim_dict_1['tot_sim'])
                weekly_char.update({'본캐': '-신규-'})
                new_df = new_df.append(weekly_char, ignore_index=True)
            else:
                j += 1
                print(guild_char, sim_dict_1['tot_sim'])
                guild_char.update({'본캐': '-탈퇴-'})
                guild_char.pop('직위')
                del_df = del_df.append(guild_char, ignore_index=True)
            continue
        guild_char.pop('직위')
        weekly_char.update(guild_char)
        if weekly_char['직위'] in ('메린이', '메잘알', '메둥이', '메애기', '메태기', '유령'):
            weekly_char.update({'본캐': '-본캐-'})
        merge_df = merge_df.append(weekly_char, ignore_index=True)
        #print(weekly_char)
        weekly_char.update(sim_dict_1)
        merge_df_dev = merge_df.append(weekly_char, ignore_index=True)
        i += 1
        j += 1

    final_merge_df = pd.concat([merge_df, new_df, del_df], ignore_index=True)
    final_merge_df_dev = pd.concat([merge_df_dev, new_df, del_df], ignore_index=True)
    final_merge_df.to_csv("merged_member.csv", encoding="utf-8-sig")
    final_merge_df_dev.to_csv("merged_member_dev.csv", encoding="utf-8-sig")


if __name__ == "__main__":
    main()