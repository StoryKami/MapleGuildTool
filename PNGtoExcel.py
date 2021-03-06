import json
import pandas as pd
from collections import defaultdict
from Char_class import character
from modify_OCR import *

import cv2
import requests
import os
from shutil import copy
import shutil
import sys

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40

TEXT_X = 220
TEXT_Y = 180

TEXT_H = 408
TEXT_W = 450


def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def get_text_part(image_path: str):
    """
    Screen capture image에서 text part만 get

    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    image = image[TEXT_Y:TEXT_Y+TEXT_H, TEXT_X:TEXT_X+TEXT_W]

    for x in range(TEXT_W):
        for y in range(TEXT_H):
            b, g, r = image[y, x]
            if (b, g, r) == (255, 255, 255) or (b, g, r) == (179, 179, 179):
                image[y, x] = (0, 0, 0)
            else:
                image[y, x] = (255, 255, 255)

    img_path = "{}_text.jpg".format(image_path[:-3])
    cv2.imwrite(img_path, image)

    return img_path

#    path_lst = []
#    for i in range(17):
#        img_path = "{}_text_{}.jpg".format(image_path, i)
#        cv2.imwrite(img_path, image[i * 24 : (i + 1) * 24, :])
#        path_lst.append(img_path)
#    return path_lst



def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})


def main():
    #if len(sys.argv) != 3:
    #    print("Please run with args: $ python example.py /path/to/image appkey")
    #image_path, appkey = sys.argv[1], sts,argv[2]

    #image_path = get_text_part(image_path)

    appkey = "03f389b0dfea751af276e3caa1ed79aa"

    weekly_dict = {'닉네임': [None]*17, '직업': [None]*17, '레벨': [None]*17, '직위': [None]*17, '주간미션': [None]*17, '지하 수로': [None]*17, '플래그 레이스': [None]*17}

    member_lst = []

    path_dir = './capture'
    file_lst = os.listdir(path_dir)

    for i, image_name in enumerate(file_lst):
        image_path = os.path.join(path_dir, image_name)
        new_img_path = os.path.join(path_dir, 'sample' + str(i) + 'png')
        copy(image_path, new_img_path)
        image_path = get_text_part(new_img_path)
        resize_impath = kakao_ocr_resize(image_path)
        if resize_impath is not None:
            image_path = resize_impath
            print("원본 대신 리사이즈된 이미지를 사용합니다.")

        results = kakao_ocr(image_path, appkey).json()
        os.unlink(image_path)
        os.unlink(new_img_path)
        results['result'].sort(key=lambda result: result['boxes'][0][0])
        results = results['result']

        member_dict = defaultdict(list)

        for i, result in enumerate(results):
            member_dict[result['boxes'][0][1] // 24].append((result['boxes'][0][0], ' '.join(result['recognition_words'])))

        for lst in member_dict.values():
            lst.sort()

        temp_lst = list(member_dict.items())
        temp_lst.sort()
        char_pnt_lst = []
        for _, char in temp_lst:
            nick = ''
            cls = ''
            lv = ''
            pos = ''
            week_pnt = ''
            boss_pnt = ''
            flag_pnt = ''
            for info in char:
                if info[0] < 50:
                    nick += info[1].replace(" ", "")
                elif info[0] < 150:
                    cls += info[1].replace(" ", "")
                elif info[0] < 175:
                    lv += info[1].replace(" ", "")
                elif info[0] < 250:
                    pos += info[1].replace(" ", "")
                elif info[0] < 300:
                    week_pnt += info[1].replace(" ", "")
                elif info[0] < 375:
                    boss_pnt += info[1].replace(" ", "")
                else:
                    flag_pnt += info[1].replace(" ", "")
            if len(nick) > 6 and cls == '':
                cls = nick[6:]
                nick = nick[:6]
            if lv == '':
                lv = cls[-3:]
                cls = cls[:-3]
            cls.strip(',')

            pos = modify_pos(pos)
            lv = modify_lv(lv)
            week_pnt = modify_weekly_pnt(week_pnt)
            boss_pnt = modify_boss_pnt(boss_pnt)
            flag_pnt = modify_flag_pnt(flag_pnt)
            week_pnt, boss_pnt, flag_pnt = validation(week_pnt, boss_pnt, flag_pnt)

            ch = character(nick, cls, lv, pos)
            pnt = (week_pnt, boss_pnt, flag_pnt)
            char_pnt_lst.append((ch, pnt))

        member_lst.extend(char_pnt_lst)
        #print(member_list)
    print(member_lst)

    temp_lst = []
    for char, pnt in member_lst:
        tmp = char.to_lst()
        tmp.extend(pnt)
        temp_lst.append(tmp)
    print(temp_lst)
    df = pd.DataFrame(temp_lst, columns=['닉네임', '직업', '레벨', '직위', '주간포인트', '수로', '플래그'])
    df.to_csv("weekly_pnt_mod.csv", encoding="utf-8-sig")

    """
    for image_path in path_lst:
        resize_impath = kakao_ocr_resize(image_path)
        if resize_impath is not None:
            image_path = resize_impath
            print("원본 대신 리사이즈된 이미지를 사용합니다.")

        results = kakao_ocr(image_path, appkey).json()
        results['result'].sort(key=lambda result: result['boxes'][0][0])
        results = results['result']
        print(results)

        for i, result in enumerate(results):
            if i % 7 == 0:
                weekly_dict['닉네임'].append(' '.join(result['recognition_words']))
            elif i % 7 == 1:
                weekly_dict['직업'].append(' '.join(result['recognition_words']))
            elif i % 7 == 2:
                weekly_dict['레벨'].append(' '.join(result['recognition_words']))
            elif i % 7 == 3:
                weekly_dict['직위'].append(' '.join(result['recognition_words']))
            elif i % 7 == 4:
                weekly_dict['주간미션'].append(' '.join(result['recognition_words']))
            elif i % 7 == 5:
                weekly_dict['지하 수로'].append(' '.join(result['recognition_words']))
            elif i % 7 == 6:
                weekly_dict['플래그 레이스'].append(' '.join(result['recognition_words']))
    """

#    df = pd.DataFrame.from_dict(weekly_dict)

    #print("[OCR] output:\n{}\n".format(df))
    #print("[OCR] output:\n{}\n".format(json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False)))


if __name__ == "__main__":
    main()