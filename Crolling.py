import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


def get_members_all_page(link="https://maplestory.nexon.com/Common/Guild?gid=823828&wid=3&orderby=1"):
    df_lst = []
    for i in range(1, 11):
        df_lst.append(get_members_one_page(link, i))
    return pd.concat(df_lst)


def get_members_one_page(link, page):
    response = requests.get(link + "&page={}".format(page))
    dfs = pd.read_html(response.text)
    df = dfs[0]
    df = df.drop(['경험치', '인기도'], axis='columns')
    df.rename(columns={'캐릭터 정보' : '닉네임'}, inplace=True)
    df['닉네임'] = df['닉네임'].transform(lambda info: info.split()[0])
    df['레벨'] = df['레벨'].transform(lambda level: level[3:])
    df.set_index('닉네임', inplace=True)

    soup = bs(response.text, "html.parser")
    elements = soup.select('div.guild_user_list table.rank_table tbody tr')

    for e in elements:
        char_link = e.select('td.left dl dt a')[0].attrs['href']
        char_response = requests.get("https://maplestory.nexon.com" + char_link)
        char_soup = bs(char_response.text, "html.parser")
        name = char_soup.select('div.char_name span')[0].text
        name = name[:-1]
        class_name = char_soup.select('div.char_info dl:nth-child(2) dd')[0].text
        class_name = class_name.split('/')[1]
        df.loc[name, '직업'] = class_name

    return df


df = get_members_all_page()
df.reset_index(inplace=True)
df = df[['닉네임', '직업', '레벨', '직위']]
print(df)
df.to_csv("guild_member.csv", encoding="utf-8-sig")