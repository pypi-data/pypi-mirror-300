import json
import math
import re

import requests
from bs4 import BeautifulSoup

class EasyMoneyPostChildReply:
    def __init__(self, data):
        self.reply_id = data.get('reply_id')
        self.reply_state = data.get('reply_state')
        self.user_id = data.get('user_id')
        self.reply_time = data.get('reply_time')
        self.reply_publish_time = data.get('reply_publish_time')
        self.reply_text = data.get('reply_text')
        self.source_post_code = data.get('source_post_code')
        self.source_post_id = data.get('source_post_id')
        self.source_reply = [EasyMoneyPostSourceReply(reply) for reply in data.get('source_reply', [])]
        self.reply_picture = data.get('reply_picture')
        self.reply_is_top = data.get('reply_is_top')
        self.reply_like_count = data.get('reply_like_count')
        self.reply_is_like = data.get('reply_is_like')
        self.reply_is_author = data.get('reply_is_author')
        self.reply_user = EasyMoneyUserData(data.get('reply_user', {}))
class EasyMoneyUserData:
    def __init__(self, data):
        self.user_id = data.get("user_id")
        self.user_nickname = data.get("user_nickname")
        self.user_name = data.get("user_name")
        self.user_v = data.get("user_v")
        self.user_type = data.get("user_type")
        self.user_is_majia = data.get("user_is_majia")
        self.user_level = data.get("user_level")
        self.user_first_en_name = data.get("user_first_en_name")
        self.user_age = data.get("user_age")
        self.user_influ_level = data.get("user_influ_level")
        self.user_black_type = data.get("user_black_type")
        self.user_third_intro = data.get("user_third_intro")
        self.user_bizflag = data.get("user_bizflag")
        self.user_bizsubflag = data.get("user_bizsubflag")
        self.user_medal_details = data.get("user_medal_details")
        self.user_extendinfos = data.get("user_extendinfos", {})
class EasyMoneyPostReply:
    def __init__(self, data):
        self.child_replys = [EasyMoneyPostChildReply(child_data) for child_data in data.get('child_replys', [])]
        self.reply_count = data.get('reply_count')
        self.child_reply_count = data.get('child_reply_count')
        self.reply_id = data.get('reply_id')
        self.source_post_code = data.get('source_post_code')
        self.source_post_id = data.get('source_post_id')
        self.reply_state = data.get('reply_state')
        self.user_id = data.get('user_id')
        self.reply_time = data.get('reply_time')
        self.reply_publish_time = data.get('reply_publish_time')
        self.reply_text = data.get('reply_text')
        self.reply_picture = data.get('reply_picture')
        self.reply_is_top = data.get('reply_is_top')
        self.reply_like_count = data.get('reply_like_count')
        self.reply_is_like = data.get('reply_is_like')
        self.reply_is_author = data.get('reply_is_author')
        self.reply_ar = data.get('reply_ar')
        self.reply_from = data.get('reply_from')
        self.reply_ip_address = data.get('reply_ip_address')
        self.reply_hide = data.get('reply_hide')
        self.reply_god = data.get('reply_god')
        self.reply_extend = data.get('reply_extend', {})
        self.reply_is_amazing = data.get('reply_is_amazing')
        self.reply_is_follow = data.get('reply_is_follow')
        self.reply_tag = data.get('reply_tag')
        self.reply_user = EasyMoneyUserData(data.get('reply_user', {}))

class EasyMoneyPostSourceReply:
    def __init__(self, data):
        self.source_reply_id = data.get("source_reply_id")
        self.source_reply_state = data.get("source_reply_state")
        self.source_reply_text = data.get("source_reply_text")
        self.source_reply_picture = data.get("source_reply_picture")
        self.source_reply_ar = data.get("source_reply_ar")
        self.source_reply_user_id = data.get("source_reply_user_id")
        self.source_reply_user_nickname = data.get("source_reply_user_nickname")
        self.source_reply_user_type = data.get("source_reply_user_type")
        self.source_reply_user = EasyMoneyUserData(data.get("source_reply_user"))
        self.source_reply_is_author = data.get("source_reply_is_author")
        self.source_reply_ip_address = data.get("source_reply_ip_address")
        self.source_reply_hide = data.get("source_reply_hide")
        self.source_likenum = data.get("source_likenum")
        self.reply_extend = data.get("reply_extend")
class EastMoneyPost:
    def __init__(self,data,total_num,total_page):
        self.post_id = data.get('post_id')
        self.post_title = data.get('post_title')
        self.stockbar_code = data.get('stockbar_code')
        self.stockbar_name = data.get('stockbar_name')
        self.stockbar_type = data.get('stockbar_type')
        self.stockbar_exchange = data.get('stockbar_exchange')
        self.user_id = data.get('user_id')
        self.user_nickname = data.get('user_nickname')
        self.user_extendinfos = data.get('user_extendinfos')
        self.post_click_count = data.get('post_click_count')
        self.post_forward_count = data.get('post_forward_count')
        self.post_comment_count = data.get('post_comment_count')
        self.post_publish_time = data.get('post_publish_time')
        self.post_last_time = data.get('post_last_time')
        self.post_type = data.get('post_type')
        self.post_state = data.get('post_state')
        self.post_from_num = data.get('post_from_num')
        self.v_user_code = data.get('v_user_code')
        self.post_top_status = data.get('post_top_status')
        self.post_has_pic = data.get('post_has_pic')
        self.post_has_video = data.get('post_has_video')
        self.user_is_majia = data.get('user_is_majia')
        self.post_ip = data.get('post_ip')
        self.qa = data.get('qa')
        self.grade_type = data.get('grade_type')
        self.institution = data.get('institution')
        self.notice_type = data.get('notice_type')
        self.notice_type_code = data.get('notice_type_code')
        self.post_display_time = data.get('post_display_time')
        self.media_type = data.get('media_type')
        self.zmt_article = data.get('zmt_article')
        self.post_source_id = data.get('post_source_id')
        self.bullish_bearish = data.get('bullish_bearish')
        self.modules = data.get('modules')
        self.spec_column = data.get('spec_column')
        self.cms_media_type = data.get('cms_media_type')
        self.art_unique_url = data.get('art_unique_url')
        self.total_num=total_num
        self.total_page=total_page
        #计算url
        self.post_url=f"https://guba.eastmoney.com/news,{self.stockbar_code},{self.post_id}.html"

class EastMoneyPostDetail:
    def __init__(self, data):
        self.post_id = data.get('post_id')
        self.post_user = data.get('post_user')
        self.post_guba = data.get('post_guba')
        self.post_title = data.get('post_title')
        self.post_content = data.get('post_content')
        self.post_abstract = data.get('post_abstract')
        self.post_publish_time = data.get('post_publish_time')
        self.post_last_time = data.get('post_last_time')
        self.post_display_time = data.get('post_display_time')
        self.post_ip = data.get('post_ip')
        self.post_state = data.get('post_state')
        self.post_checkState = data.get('post_checkState')
        self.post_click_count = data.get('post_click_count')
        self.post_forward_count = data.get('post_forward_count')
        self.post_comment_count = data.get('post_comment_count')
        self.post_comment_authority = data.get('post_comment_authority')
        self.post_like_count = data.get('post_like_count')
        self.post_is_like = data.get('post_is_like')
        self.post_is_collected = data.get('post_is_collected')
        self.post_type = data.get('post_type')
        self.post_source_id = data.get('post_source_id')
        self.post_top_status = data.get('post_top_status')
        self.post_status = data.get('post_status')
        self.post_from = data.get('post_from')
        self.post_from_num = data.get('post_from_num')
        self.post_pdf_url = data.get('post_pdf_url')
        self.post_has_pic = data.get('post_has_pic')
        self.has_pic_not_include_content = data.get('has_pic_not_include_content')
        self.post_pic_url = data.get('post_pic_url')
        self.source_post_id = data.get('source_post_id')
        self.source_post_state = data.get('source_post_state')
        self.source_post_user_id = data.get('source_post_user_id')
        self.source_post_user_nickname = data.get('source_post_user_nickname')
        self.source_post_user_type = data.get('source_post_user_type')
        self.source_post_user_is_majia = data.get('source_post_user_is_majia')
        self.source_post_pic_url = data.get('source_post_pic_url')
        self.source_post_title = data.get('source_post_title')
        self.source_post_content = data.get('source_post_content')
        self.source_post_abstract = data.get('source_post_abstract')
        self.source_post_ip = data.get('source_post_ip')
        self.source_post_type = data.get('source_post_type')
        self.source_post_guba = data.get('source_post_guba')
        self.post_video_url = data.get('post_video_url')
        self.source_post_video_url = data.get('source_post_video_url')
        self.source_post_source_id = data.get('source_post_source_id')
        self.code_name = data.get('code_name')
        self.product_type = data.get('product_type')
        self.v_user_code = data.get('v_user_code')
        self.source_click_count = data.get('source_click_count')
        self.source_comment_count = data.get('source_comment_count')
        self.source_forward_count = data.get('source_forward_count')
        self.source_publish_time = data.get('source_publish_time')
        self.source_user_is_majia = data.get('source_user_is_majia')
        self.ask_chairman_state = data.get('ask_chairman_state')
        self.selected_post_code = data.get('selected_post_code')
        self.selected_post_name = data.get('selected_post_name')
        self.ask_question = data.get('ask_question')
        self.ask_answer = data.get('ask_answer')
        self.qa = data.get('qa')
        self.fp_code = data.get('fp_code')
        self.codepost_count = data.get('codepost_count')
        self.extend = data.get('extend')
        self.post_pic_url2 = data.get('post_pic_url2')
        self.source_post_pic_url2 = data.get('source_post_pic_url2')
        self.relate_topic = data.get('relate_topic')
        self.source_extend = data.get('source_extend')
        self.digest_type = data.get('digest_type')
        self.source_post_atuser = data.get('source_post_atuser')
        self.post_inshare_count = data.get('post_inshare_count')
        self.repost_state = data.get('repost_state')
        self.post_atuser = data.get('post_atuser')
        self.reptile_state = data.get('reptile_state')
        self.post_add_list = data.get('post_add_list')
        self.extend_version = data.get('extend_version')
        self.post_add_time = data.get('post_add_time')
        self.post_modules = data.get('post_modules')
        self.post_speccolumn = data.get('post_speccolumn')
        self.post_ip_address = data.get('post_ip_address')
        self.source_post_ip_address = data.get('source_post_ip_address')
        self.post_mod_time = data.get('post_mod_time')
        self.post_mod_count = data.get('post_mod_count')
        self.allow_likes_state = data.get('allow_likes_state')
        self.system_comment_authority = data.get('system_comment_authority')
        self.limit_reply_user_auth = data.get('limit_reply_user_auth')
        self.post_tipstate = data.get('post_tipstate')
        self.disable_ad = data.get('disable_ad')
        self.disable_color = data.get('disable_color')
        self.fundimgs = data.get('fundimgs')
        self.source_fundimgs = data.get('source_fundimgs')
        self.textsource = data.get('textsource')
        self.source_textsource = data.get('source_textsource')
        self.qrcimgs = data.get('qrcimgs')
        self.source_qrcimgs = data.get('source_qrcimgs')
        self.payauth = data.get('payauth')
        self.stockimgs = data.get('stockimgs')
        self.source_stockimgs = data.get('source_stockimgs')
        self.comment_section = data.get('comment_section')
        self.topiccirclesimple = data.get('topiccirclesimple')
class WebArticle:
    def __init__(self, data):
        self.post_is_like = data.get('post_is_like', False)
        self.post_is_collected = data.get('post_is_collected', False)
        self.post_status = data.get('post_status', 0)
        self.source_post_id = data.get('source_post_id', 0)
        self.source_post_state = data.get('source_post_state', 0)
        self.source_post_user_id = data.get('source_post_user_id', "")
        self.source_post_user_nickname = data.get('source_post_user_nickname', "")
        self.source_post_user_type = data.get('source_post_user_type', 0)
        self.source_post_user_is_majia = data.get('source_post_user_is_majia', False)
        self.source_post_user_extendinfos = data.get('source_post_user_extendinfos', {})
        self.source_post_pic_url = data.get('source_post_pic_url', [])
        self.source_post_title = data.get('source_post_title', "")
        self.source_post_content = data.get('source_post_content', "")
        self.source_post_ip = data.get('source_post_ip', "")
        self.source_post_type = data.get('source_post_type', 0)
        self.source_post_guba = data.get('source_post_guba', {})
        self.source_post_from = data.get('source_post_from', "")
        self.source_post_like_count = data.get('source_post_like_count', 0)
        self.source_comment_count = data.get('source_comment_count', "")
        self.selected_post_code = data.get('selected_post_code', "")
        self.selected_post_name = data.get('selected_post_name', "")
        self.selected_relate_guba = data.get('selected_relate_guba', None)
        self.source_extend = data.get('source_extend', {})
        self.source_post_source_id = data.get('source_post_source_id', "")
        self.zwpage_flag = data.get('zwpage_flag', 0)
        self.source_post_comment_count = data.get('source_post_comment_count', 0)
        self.post_from_num = data.get('post_from_num', 0)
        self.content_type = data.get('content_type', 0)
        self.media_type = data.get('media_type', 0)
        self.post_content = data.get('post_content', "")
        self.post_abstract = data.get('post_abstract', "")
        self.post_publish_time = data.get('post_publish_time', "")
        self.post_display_time = data.get('post_display_time', "")
        self.post_ip = data.get('post_ip', "")
        self.post_state = data.get('post_state', 0)
        self.post_checkState = data.get('post_checkState', 0)
        self.post_forward_count = data.get('post_forward_count', 0)
        self.post_comment_authority = data.get('post_comment_authority', 0)
        self.post_like_count = data.get('post_like_count', 0)
        self.post_type = data.get('post_type', 0)
        self.post_source_id = data.get('post_source_id', "")
        self.post_top_status = data.get('post_top_status', 0)
        self.post_from = data.get('post_from', "")
        self.post_has_pic = data.get('post_has_pic', False)
        self.post_pic_url = data.get('post_pic_url', [])
        self.ask_question = data.get('ask_question', "")
        self.ask_answer = data.get('ask_answer', "")
        self.qa = data.get('qa', None)
        self.extend = data.get('extend', {})
        self.post_pic_url2 = data.get('post_pic_url2', [])
        self.relate_topic = data.get('relate_topic', {})
        self.post_atuser = data.get('post_atuser', [])
        self.reply_list = data.get('reply_list', [])
        self.repost_state = data.get('repost_state', 0)
        self.modules = data.get('modules', [])
        self.spec_column = data.get('spec_column', "")
        self.post_mod_time = data.get('post_mod_time', None)
        self.reptile_state = data.get('reptile_state', 0)
        self.allow_likes_state = data.get('allow_likes_state', 0)
        self.disable_color = data.get('disable_color', 0)
        self.post_id = data.get('post_id', 0)
        self.post_user = data.get('post_user', {})
        self.post_guba = data.get('post_guba', {})
        self.post_title = data.get('post_title', "")
        self.post_last_time = data.get('post_last_time', "")
        self.post_click_count = data.get('post_click_count', 0)
        self.post_comment_count = data.get('post_comment_count', 0)
        self.post_address = data.get('post_address', None)
def getPostData(url,data,headers=None):
    if headers is None:
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'qgqp_b_id=332a3f546cfa76734ca2f63c20646b56;  st_pvi=27895011384798; ',
        'Origin': 'https://guba.eastmoney.com',
        'Referer': 'https://guba.eastmoney.com/news,cfhpl,1462253811.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        }
    response = requests.post(
        url,
        headers=headers,
        data=data,
    )
    return response.text
def getHtml(url,headers=None):
    if headers is None:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'qgqp_b_id=332a3f546cfa76734ca2f63c20646b56; websitepoptg_api_time=1726413783725; mtp=1; sid=; vtpst=%7c; st_si=36851793234096; _adsame_fullscreen_12952=1; st_asi=delete; st_pvi=27895011384798; st_sp=2024-09-12%2022%3A52%3A54; st_inirUrl=https%3A%2F%2Fcn.bing.com%2F; st_sn=17; st_psi=20240916114308656-117001356556-2170777194',
            'Referer': 'https://guba.eastmoney.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
    response = requests.get(url,headers=headers)
    return response.text

def parseEastMoneyPostHtml(html,url):
    soup = BeautifulSoup(html, 'html.parser')
    script_tags = soup.find_all("script")
    # 遍历每个<script>标签，提取其中的JavaScript代码
    javascript_code=""
    for script_tag in script_tags:
        javascript_code += script_tag.text
    pattern = r'var\s+article_list\s*=\s*({.*?});'
    match = re.search(pattern, javascript_code,re.DOTALL)
    if match is None:
        raise Exception(f"没有相关数据,{url}")
    json_list = json.loads(match.group(1))
    return json_list


def getEastMoneyPostByUrl(url,headers=None):
    html = getHtml(url,headers)
    return parseEastMoneyPostHtml(html,url)

def getEastMoneyPostList(stock_code,page=1,headers=None):
    url=f"https://guba.eastmoney.com/list,{stock_code},f_{page}.html"
    res=getEastMoneyPostByUrl(url,headers=headers)
    east_money_post_list=[]
    for data in res["re"]:
        east_money_post_list.append(EastMoneyPost(data,total_num=res["count"],total_page=math.ceil(res["count"]/80)))
    return east_money_post_list

def parseEastMoneyPostDetail(html,url):
    soup = BeautifulSoup(html, 'html.parser')
    script_tags = soup.find_all("script")
    # 遍历每个<script>标签，提取其中的JavaScript代码
    javascript_code = ""
    for script_tag in script_tags:
        javascript_code += script_tag.text+";"
    pattern = r'var\s+post_article\s*=\s*({.*?});'
    match = re.search(pattern, javascript_code, re.DOTALL)
    if match is None:
        raise Exception(f"没有相关数据,{url}")
    json_list = json.loads(match.group(1))
    return json_list

def getEastMoneyPostDetailByUrl(url,headers=None):
    html = getHtml(url,headers=headers)
    return parseEastMoneyPostDetail(html,url)
def getEstMoneyPostDetail(stock_code,post_id,headers=None):
    url = f"https://guba.eastmoney.com/news,{stock_code},{post_id}.html"
    res = getEastMoneyPostDetailByUrl(url, headers=headers)
    return EastMoneyPostDetail(res)


def getEasyMoneyPostReplyByUrl(url,data,headers=None):
    json_str = getPostData(url,data=data,headers=headers)
    json_data=json.loads(json_str)
    return json_data
def getEasyMoneyPostReplyList(post_id,page=1,page_size=30,headers=None):
    data = {
        'param': f'postid={post_id}&sort=1&sorttype=1&p={page}&ps={page_size}',
        'plat': 'Web',
        'path': 'reply/api/Reply/ArticleNewReplyList',
        'env': '2',
        'origin': '',
        'version': '2022',
        'product': 'Guba',
    }
    url="https://guba.eastmoney.com/api/getData?code=cfhpl&path=reply/api/Reply/ArticleNewReplyList"
    res=getEasyMoneyPostReplyByUrl(url,data,headers=headers)
    reply_list=[]
    if res["re"] is None:
        return None
    for r in res["re"]:
        reply_list.append(EasyMoneyPostReply(r))
    return reply_list

def getEasyMoneyWebArticleByUrl(url,data,headers=None):
    json_str = getPostData(url, data=data, headers=headers)
    json_data = json.loads(json_str)
    return json_data

def getEasyMoneyWebArticleList(stock_code,page=1,page_size=40,headers=None):
    data={
        "param": f"code={stock_code}&type=0&sorttype=0&p={page}&ps={page_size}",
        "plat": "Web",
        "path": "webarticlelist/api/article/WebArticleList",
        "env": 2,
        "origin": "",
        "version": 2022,
        "product": "Guba"
    }
    url = "https://guba.eastmoney.com/api/getData?code=zssh000001&path=webarticlelist/api/article/WebArticleList"
    res = getEasyMoneyWebArticleByUrl(url, data, headers=headers)
    reply_list = []
    if res["re"] is None:
        return None
    for r in res["re"]:
        reply_list.append(WebArticle(r))
    return reply_list