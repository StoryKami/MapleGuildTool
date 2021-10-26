import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
from collections import defaultdict

df = pd.read_csv("guild_member.csv")
df = df[['닉네임', '직업', '레벨', '직위']]
df.sort_values(by=['닉네임'], axis=0, inplace=True)
df.reset_index(inplace=True, drop=True)
df.to_csv("sorted_guild_member.csv", encoding="utf-8-sig")