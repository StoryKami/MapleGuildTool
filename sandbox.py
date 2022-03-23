import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
from collections import defaultdict
from Crolling import *

"""
df_weekly = pd.read_csv("weekly_pnt_mod.csv", encoding="utf-8-sig")
df_weekly = df_weekly[['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그']]

df_weekly = df_weekly.drop([14, 192])
df_weekly.reset_index(inplace=True, drop=True)

df_weekly.to_csv("weekly_pnt_mod_copy.csv", encoding="utf-8-sig")
"""

df_weekly = pd.read_csv("weekly_pnt_mod.csv", encoding="utf-8-sig")
df_weekly = df_weekly[['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그']]
df_weekly.reset_index(inplace=True, drop=True)


df_guild = pd.read_csv("sorted_guild_member.csv")
df_guild = df_guild[['닉네임', '직업', '레벨', '직위']]
df_guild.reset_index(inplace=True, drop=True)