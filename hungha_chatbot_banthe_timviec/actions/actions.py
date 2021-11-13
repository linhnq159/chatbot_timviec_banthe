# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Tracker
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import re
import gc
from rasa_sdk.forms import FormAction
from requests.models import Response
#import feedparser
import random
import pathlib
import os
#from bs4 import BeautifulSoup
from datetime import datetime

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

#Trả về action unknown
class act_unknown(Action):
    def name(self) -> Text:
        return "act_unknown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"payload":'/great_banthe',"title": "Mua thẻ điện thoại , xem chiết khấu mua thẻ "},
            {"payload":'/great_timviec',"title": "Tìm việc làm , tạo cv , tuyển dụng"},
        ]

        text = "Chào bạn. Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì! \n Đây là chatbot tự động bạn đang quan tâm đến dịch vụ nào ạ: "
        dispatcher.utter_message(text=text,buttons=buttons)
        gc.collect()
        return []

## chào hỏi giờ
class act_time(Action):

    def name(self) -> Text:
        return "action_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        dispatcher.utter_message("Bây giờ là: " + current_time)
        return []

## tìm chiết khấu trang web
class ActionChietKhau(Action):
    def name(self) -> Text:
        return 'action_chiet_khau'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        web = str(tracker.get_slot('web')).lower()
        web = no_accent_vietnamese(web)
        filepath = str(pathlib.Path().absolute()) + '/data/web.txt'.replace('/', os.sep)
        list_web = []
        list_web1 = []
        with open(filepath, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.split(",")[0:]
                text1 = line.split(",")[0]
                # text = no_accent_vietnamese(text)
                list_web.append(text)
                list_web1.append(text1)
                line = fp.readline()
                cnt += 1
            for i in range(len(list_web)):
                for j in range(len(list_web[i])):
                    text1 = list_web[i][j].replace("\n", "")
                    if (web == text1):
                        web = list_web[i][0].replace("\n","")
        if web in list_web1:
            dispatcher.utter_message("Bạn truy cập link: https://" + str(web) + ".com/chiet-khau để tham khảo chiết khẩu nhé")
        else :
            dispatcher.utter_message("Bạn truy cập link: https://banthe247.com/chiet-khau để tham khảo chiết khẩu nhé")
        return []

#Mua thẻ trên ứng dụng :
class ActionMuaTheUngDung(Action):
    def name(self) -> Text:
        return "action_mua_the_tren_ung_dung"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"payload":'/tai_ung_dung_mua_the{"web":"banthe247"}',"title":"Bán thẻ 247"},
            {"payload":'/tai_ung_dung_mua_the{"web":"banthe24h"}',"title":"Bán thẻ 24h"},
            {"payload":'/tai_ung_dung_mua_the{"web":"napthe365"}',"title":"Nạp thẻ 365"},
            {"payload":'/tai_ung_dung_mua_the{"web":"muathe123"}',"title":"Mua thẻ 123"},
            {"payload":'/tai_ung_dung_mua_the{"web":"muathe24h"}',"title":"Mua thẻ 24h"}
        ]

        text = "Chào bạn, bạn đang có nhu cầu sử dụng thẻ cào trên ứng dụng gì ạ? "
        dispatcher.utter_message(text=text,buttons=buttons)
        gc.collect()
        return []

# Hỏi giá thẻ
class action_hoi_gia(Action):
    def name(self):
        return 'action_hoi_gia'

    def run(self, dispatcher, tracker, domain):
        gia = str(tracker.get_slot('gia')).lower()
        gia = no_accent_vietnamese(gia)
        filepath = str(pathlib.Path().absolute()) + '/data/the.txt'.replace('/', os.sep)
        list_gia = []
        with open(filepath, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.split(",")[0:]
                # text = no_accent_vietnamese(text)
                list_gia.append(text)
                line = fp.readline()
                cnt += 1
            for i in range(len(list_gia)):
                for j in range(len(list_gia[i])):
                    text1 = list_gia[i][j].replace("\n", "")
                    if (gia == text1):
                        gia = list_gia[i][0].replace("\n", "")
        if (gia == "10k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 9.950 VNĐ")
        elif (gia == "20k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 19.000 VNĐ")
        elif (gia == "30k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 29.850 VNĐ")
        elif (gia == "50k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 48.750 VNĐ")
        elif (gia == "100k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 97.500 VNĐ")
        elif (gia == "200k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 195.000 VNĐ")
        elif (gia == "300k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 292.500 VNĐ")
        elif (gia == "500k"):
            dispatcher.utter_message(text="Bạn chỉ phải thanh toán 487.500 VNĐ")
        else:
            buttons = [
                {"payload": '/hoi_gia{"gia":"10k"}', "title": "10k"},
                {"payload": '/hoi_gia{"gia":"20k"}', "title": "20k"},
                {"payload": '/hoi_gia{"gia":"30k"}', "title": "30k"},
                {"payload": '/hoi_gia{"gia":"50k"}', "title": "50k"},
                {"payload": '/hoi_gia{"gia":"100k"}', "title": "100k"},
                {"payload": '/hoi_gia{"gia":"200k"}', "title": "200k"},
                {"payload": '/hoi_gia{"gia":"300k"}', "title": "300k"},
                {"payload": '/hoi_gia{"gia":"500k"}', "title": "500k"}
            ]
            dispatcher.utter_message(text="Hiện tại không có mệnh thẻ giá trị này . Bên mình có các mệnh giá dưới đây :",buttons=buttons)
        return []

# Tải ứng dụng mua thẻ
class ActionTaiUngDung(Action):

    def name(self) -> Text:
        return "action_tai_ung_dung_mua_the"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        web = str(tracker.get_slot('web')).lower()
        web = no_accent_vietnamese(web)
        filepath = str(pathlib.Path().absolute()) + '/data/web.txt'.replace('/', os.sep)
        list_web = []
        list_web1 = []
        with open(filepath, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.split(",")[0:]
                text1 = line.split(",")[0]
                # text = no_accent_vietnamese(text)
                list_web.append(text)
                list_web1.append(text1)
                line = fp.readline()
                cnt += 1
            for i in range(len(list_web)):
                for j in range(len(list_web[i])):
                    text1 = list_web[i][j].replace("\n", "")
                    if (web == text1):
                        web = list_web[i][0].replace("\n", "")
        if web == 'none':
            buttons = [
                {"payload": '/tai_ung_dung_mua_the{"web":"banthe247"}', "title": "Bán thẻ 247"},
                {"payload": '/tai_ung_dung_mua_the{"web":"banthe24h"}', "title": "Bán thẻ 24h"},
                {"payload": '/tai_ung_dung_mua_the{"web":"napthe365"}', "title": "Nạp thẻ 365"},
                {"payload": '/tai_ung_dung_mua_the{"web":"muathe123"}', "title": "Mua thẻ 123"},
                {"payload": '/tai_ung_dung_mua_the{"web":"muathe24h"}', "title": "Mua thẻ 24h"}
            ]
            text = "Bạn có thể chọn để tài 1 trong những ứng dụng dưới đây : "
            dispatcher.utter_message(text=text,buttons=buttons)
            return []
        if web != 'none':
            url = 'https://play.google.com/store/apps/details?id=vn.'+ str(web) + '.' + str(web)
            dispatcher.utter_message("Chào bạn, bạn truy cập link : " + url + " để tải ứng dụng về điện thoại ạ ")
        return []

# Hỏi sđt tổng đài
class ActionTongDai(Action):
    def name(self) -> Text:
        return 'action_lien_he_tong_dai'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tongdai = str(tracker.get_slot('tongdai')).lower()
        tongdai = no_accent_vietnamese(tongdai)
        filepath = str(pathlib.Path().absolute()) + '/data/tongdai1.txt'.replace('/', os.sep)
        list_tong_dai = []
        with open(filepath, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.split(",")[0:]
                # text = no_accent_vietnamese(text)
                list_tong_dai.append(text)
                line = fp.readline()
                cnt += 1
            for i in range(len(list_tong_dai)):
                for j in range(len(list_tong_dai[i])):
                    text1 = list_tong_dai[i][j].replace("\n", "")
                    if (tongdai == text1):
                        tongdai = list_tong_dai[i][0]

        tongdai = tongdai.replace("\n", "")
        list_tong_dai = []
        filepath1 = str(pathlib.Path().absolute()) + '/data/tongdai.txt'.replace('/', os.sep)
        print(tongdai)
        with open(filepath1, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.split("|")[1] .replace("\n", "").lower()
                text = no_accent_vietnamese(text)
                list_tong_dai.append(text)
                if (tongdai == text):
                    sdt = line.split("|")[0].replace("\n", "")
                    dispatcher.utter_message("Chào bạn,bạn liên hệ " + sdt + " để được hỗ trợ ạ ")
                line = fp.readline()
                cnt += 1

        if tongdai not in list_tong_dai:
            buttons = [
                {"payload": '/lien_he_tong_dai{"tongdai":"viettel"}', "title": "Viettel"},
                {"payload": '/lien_he_tong_dai{"tongdai":"mobifone"}', "title": "Mobifone"},
                {"payload": '/lien_he_tong_dai{"tongdai":"vinaphone"}', "title": "Vinaphone"},
                {"payload": '/lien_he_tong_dai{"tongdai":"vietnammobile"}', "title": "Vietnammobile"}
            ]
            text = "Mời nhập lại tổng đài bạn muốn quan tâm :"
            dispatcher.utter_message(text=text,buttons=buttons)
        return[]

# Đối tác
class ActionDoiTac(Action):

    def name(self) -> Text:
        return "action_doi_tac"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        web1 = str(tracker.get_slot('web1')).lower()
        web1 = web1.replace('.vn','')
        web2 = str(tracker.get_slot('web2')).lower()
        web2 = web2.replace('.vn','')
        filepath = str(pathlib.Path().absolute()) + '/data/doitac.txt'.replace('/', os.sep)
        list_web = []
        with open(filepath, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.replace("\n", "").lower()
                text = no_accent_vietnamese(text)
                list_web.append(text)
                line = fp.readline()
                cnt += 1
        if (web1 in list_web and web2 in list_web and web1 != web2):
            dispatcher.utter_message("Chào bạn, " + str(web1) + " là đối tác của " + str(web2) +" ạ" )
        elif (web1 == web2):
            dispatcher.utter_message("Chào bạn , 2 web là một ạ ")
        else:
            dispatcher.utter_message("Chào bạn, " + str(web1) + " không phải là đối tác của " + str(web2) +" ạ" )

        return []

## search luong on tinh thanh
class ActionLuongTinhThanh(Action):
    def name(self) -> Text:
        return 'action_luong_tinh_thanh'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        province_input = str(tracker.get_slot('province'))
        province = province_input.lower()
        province = no_accent_vietnamese(province)
        filepath = str(pathlib.Path().absolute()) + '/data/id.txt'.replace('/', os.sep)
        list_province = []
        list_id = []
        with open(filepath, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.split("|")[1].replace("\n", "").lower()
                text = no_accent_vietnamese(text)
                list_province.append(text)
                text1 = line.split("|")[0].replace("\n", "").lower()
                text1 = no_accent_vietnamese(text1)
                list_id.append(text1)
                line = fp.readline()
                cnt += 1
        if province in list_province:
            i = list_province.index(province)
            id = list_id[i]
            province = province.replace(' ', '-')
            url = 'https://timviec365.vn/ssl/luong-tai-' + str(province) + '-' + str(id) + '.html'
            dispatcher.utter_message(
                "Để tham khảo lương quanh khu vực " + province_input + ".\nMời truy cập " + url + "\nBạn cần trợ giúp gì nữa không ạ?")
        else:
            buttons = [
                {"payload": '/luong_tinh_thanh{"province":"Hà Nội"}', "title": "Hà Nội"},
                {"payload": '/luong_tinh_thanh{"province":"Hồ Chí Minh"}', "title": "Hồ Chí Minh"},
                {"payload": '/luong_tinh_thanh{"province":"Quảng Ninh"}', "title": "Quảng Ninh"},
                {"payload": '/luong_tinh_thanh{"province":"Bắc Ninh"}', "title": "Bắc Ninh"},
                {"payload": '/luong_tinh_thanh{"province":"Hải Dương"}', "title": "Hải Dương"}
            ]
            text = "Chào bạn. Bạn vui lòng truy cập link https://timviec365.vn/ssl/so-sanh-luong.html Nhập thông tin tỉnh thành bạn cần tra cứu và ấn tìm kiếm ạ."
            dispatcher.utter_message(text=text, buttons=buttons)
        return []

## tìm việc thcs
class Actionvieclamthpt(Action):
    def name(self) -> Text:
        return 'action_viec_lam_thcs'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        lop = str(tracker.get_slot('lop')).lower()
        lop = no_accent_vietnamese(lop)
        filepath = str(pathlib.Path().absolute()) + '/data/lop.txt'.replace('/', os.sep)
        list_lop = []
        with open(filepath, encoding="utf8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                text = line.replace("\n", "").lower()
                text = no_accent_vietnamese(text)
                list_lop.append(text)
                line = fp.readline()
                cnt += 1

        if lop in list_lop:
            dispatcher.utter_message("Chào bạn, bạn hoàn thành chương trình học trung học cơ sở trước ạ")
        else:
            dispatcher.utter_message(
                "Chào bạn, bạn truy cập https://timviec365.com/dang-ky-ung-vien.html để tạo tk Ứng viên trên web. Và chủ động tìm Nhà tuyển dụng phù hợp để nộp hồ sơ online ứng tuyển nhé")

        return []
