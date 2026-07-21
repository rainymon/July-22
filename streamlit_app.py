# streamlit_app.py
import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2019.07.22 — 176 Headlines",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ACTIVE_TIMELINE_SECONDS = 43.0
LEAD_IN_SECONDS = 1.0

SPECIAL_ARTICLES = {
    1:   {"file": "assets/article_001.jpg", "duration": 3.5, "scroll": False},
    6:   {"file": "assets/article_006.jpg", "duration": 1.2, "scroll": False},

    161: {"file": "assets/article_161.jpg", "duration": 1.2, "scroll": False},
    162: {"file": "assets/article_162.jpg", "duration": 2.0, "scroll": False},
    176: {"file": "assets/article_176.jpg", "duration": 2.8, "scroll": False},
}

ARTICLES = json.loads(r'''[{"num":1,"time":"00:00","minute":0,"title":"‘열여덟의 순간’ 옹성우-김향기-신승호가 밝힌 관전 포인트"},{"num":2,"time":"04:45","minute":285,"title":"열여덟의 순간' 옹성우·김향기·신승호·강기영, 직접 밝힌 관전 포인트"},{"num":3,"time":"08:10","minute":490,"title":"‘열여덟의 순간’, 오늘 첫방..눈부시게 빛나는 ‘Pre-청춘’ 옹성우X김향기X신승호 출격"},{"num":4,"time":"09:21","minute":561,"title":"[TV알리미] 옹성우·김향기·신승호 ‘열여덟의 순간’, ‘입덕 보장’ 관전포인트 셋"},{"num":5,"time":"12:45","minute":765,"title":"드라마 '열여덟의 순간' 인물관계도? 옹성우X김향기X신승호, 초현실 비주얼에 '헉' 나이는? 몇부작·재방송"},{"num":6,"time":"14:13","minute":853,"title":"신승호 `셔츠는 깜빡 하고~` [MK포토]"},{"num":7,"time":"14:22","minute":862,"title":"옹성우-김향기-신승호, 우린 하트 제조기 [포토엔HD]"},{"num":8,"time":"14:23","minute":863,"title":"[포토]옹성우-김향기-신승호, 우리는 열여덟!"},{"num":9,"time":"14:23","minute":863,"title":"신승호, 약간 긴장한 눈빛 [포토엔HD]"},{"num":10,"time":"14:24","minute":864,"title":"[포토]신승호, 훈훈한 비주얼!"},{"num":11,"time":"14:24","minute":864,"title":"[포토]신승호, 훈남스타일"},{"num":12,"time":"14:25","minute":865,"title":"신승호, 반장이지만 약간 건방진 포즈 [포토엔HD]"},{"num":13,"time":"14:26","minute":866,"title":"옹성우-김향기-신승호-강기영, 주역들 (열여덟의 순간 제작발표회)"},{"num":14,"time":"14:26","minute":866,"title":"신승호,'팔색조 매력 발산'"},{"num":15,"time":"14:27","minute":867,"title":"[포토] 신승호, 강렬한 눈빛으로"},{"num":16,"time":"14:28","minute":868,"title":"신승호, 부드러운 미소"},{"num":17,"time":"14:28","minute":868,"title":"김향기,'옹성우-신승호 사이에서 팔짱끼고'"},{"num":18,"time":"14:29","minute":869,"title":"김향기 '옹성우-신승호 배려하는 매너손'[엑's HD포토]"},{"num":19,"time":"14:29","minute":869,"title":"[SW포토]강기영-옹성우-김향기-신승호,'열여덟의 순간 파이팅!'"},{"num":20,"time":"14:30","minute":870,"title":"[포토] 옹성우-김향기-신승호, 열여덟 학생들의"},{"num":21,"time":"14:30","minute":870,"title":"신승호, 무더위라 셔츠는 안보이는 패션으로 인사 [포토엔HD]"},{"num":22,"time":"14:30","minute":870,"title":"[T포토] 신승호 '웃음 꾹 참고'"},{"num":23,"time":"14:30","minute":870,"title":"[포토S] 신승호, 시크한 손인사"},{"num":24,"time":"14:30","minute":870,"title":"강기영-옹성우-김향기-신승호,'열여덟의 순간들, 파이팅'"},{"num":25,"time":"14:30","minute":870,"title":"옹성우-김향기-신승호, 주역들 (열여덟의 순간 제작발표회)"},{"num":26,"time":"14:31","minute":871,"title":"김향기 `옹성우와 신승호 사이에서 다정하게 팔짱끼고` [MK포토]"},{"num":27,"time":"14:31","minute":871,"title":"[포토S] 신승호, 매력 미소"},{"num":28,"time":"14:31","minute":871,"title":"[포토]옹성우-김향기-신승호, 심쿵 3인방"},{"num":29,"time":"14:31","minute":871,"title":"[SW포토]옹성우-김향기-신승호,'떨리는 매너손'"},{"num":30,"time":"14:31","minute":871,"title":"[ST포토] 신승호 '블랙'"},{"num":31,"time":"14:32","minute":872,"title":"김향기, '옹성우 신승호 사이에서 하트 뿅뿅'"},{"num":32,"time":"14:32","minute":872,"title":"신승호, 훤칠 미남"},{"num":33,"time":"14:32","minute":872,"title":"[포토] 김향기 '옹성우-신승호 멋진 두 남자와 함께'"},{"num":34,"time":"14:32","minute":872,"title":"신승호 '너무 깊이 파인 의상에 매너손'[엑's HD포토]"},{"num":35,"time":"14:32","minute":872,"title":"[포토S] 신승호, 남성미 물씬"},{"num":36,"time":"14:32","minute":872,"title":"[ST포토] 신승호 '평범한 포즈'"},{"num":37,"time":"14:33","minute":873,"title":"[T포토] 옹성우-김향기-신승호 '깜찍 애교 하트'"},{"num":38,"time":"14:33","minute":873,"title":"신승호 '불량 청소년 포스'[엑's HD포토]"},{"num":39,"time":"14:33","minute":873,"title":"옹성우-김향기-신승호-강기영, 빛나는 주역들 (열여덟의 순간 제작발표회)"},{"num":40,"time":"14:34","minute":874,"title":"[포토] 신승호 '쑥스러운 눈빛 인사'"},{"num":41,"time":"14:34","minute":874,"title":"[포토] 신승호 '잘생긴 눈빛'"},{"num":42,"time":"14:34","minute":874,"title":"[SW포토]옹성우-김향기-신승호,'하트 발사'"},{"num":43,"time":"14:35","minute":875,"title":"[TEN PHOTO]옹성우 신승호 '김향기의 매너손, 감동이야~'"},{"num":44,"time":"14:36","minute":876,"title":"[MD포토] 신승호 '그 누구보다 완벽하고도, 미숙한 아이 캐릭터'"},{"num":45,"time":"14:36","minute":876,"title":"[ST포토] 옹성우-김향기-신승호 '풋풋함 가득'"},{"num":46,"time":"14:37","minute":877,"title":"옹성우-김향기-신승호, 우린 열여덟"},{"num":47,"time":"14:37","minute":877,"title":"포즈 취하는 배우 신승호 [스타포토]"},{"num":48,"time":"14:38","minute":878,"title":"[SW포토]매력적인 미소의 배우 신승호"},{"num":49,"time":"14:38","minute":878,"title":"[TD포토] 신승호 '축구선수 출신'"},{"num":50,"time":"14:38","minute":878,"title":"[포토] 신승호, 매력적인 보이스"},{"num":51,"time":"14:40","minute":880,"title":"[SW포토]축구선수 출신 배우 신승호"},{"num":52,"time":"14:41","minute":881,"title":"[포토]신승호, 매력적인 보조개!"},{"num":53,"time":"14:42","minute":882,"title":"<포토>신승호 '빠져드는 눈빛'"},{"num":54,"time":"14:43","minute":883,"title":"[TD포토] 신승호 '잘생김 폭발'"},{"num":55,"time":"14:43","minute":883,"title":"신승호 '차세대 하이틴 스타'[엑's HD포토]"},{"num":56,"time":"14:43","minute":883,"title":"<포토>신승호 '셔츠를 잊은 패션'"},{"num":57,"time":"14:44","minute":884,"title":"옹성우-김향기-신승호, 청춘 하트 [포토엔HD]"},{"num":58,"time":"14:44","minute":884,"title":"[T포토] 신승호 '셔츠는 생략~'"},{"num":59,"time":"14:46","minute":886,"title":"신승호, 강렬한 남성미 (열여덟의 순간 제작발표회)"},{"num":60,"time":"14:46","minute":886,"title":"신승호, 훈훈한 매력 (열여덟의 순간 제작발표회)"},{"num":61,"time":"14:46","minute":886,"title":"[포토] 신승호, '수줍게 손인사' (열여덟의 순간)"},{"num":62,"time":"14:46","minute":886,"title":"[ST포토] 신승호, 훈훈함 물씬"},{"num":63,"time":"14:47","minute":887,"title":"옹성우-김향기-신승호, 청춘 선남선녀 [포토엔HD]"},{"num":64,"time":"14:47","minute":887,"title":"[포토] '열여덟의 순간' 신승호, 휘영에 완벽 빙의"},{"num":65,"time":"14:48","minute":888,"title":"신승호, 스윗함이 흐르는 인사 [포토엔HD]"},{"num":66,"time":"14:48","minute":888,"title":"[TEN PHOTO]옹성우 김향기 신승호 설레는 삼각관계''"},{"num":67,"time":"14:48","minute":888,"title":"[T포토] 신승호 '모델 포스, 시크 훈남'"},{"num":68,"time":"14:48","minute":888,"title":"[포토]신승호, 상남자 느낌 물씬"},{"num":69,"time":"14:49","minute":889,"title":"[포토] '열여덟의 순간' 신승호, 차분한 미소"},{"num":70,"time":"14:49","minute":889,"title":"[TD포토] 옹성우-김향기-신승호 '열여덟의 순간'많이 사랑해주세요~"},{"num":71,"time":"14:49","minute":889,"title":"신승호, '노셔츠' 야성미 어필! (열여덟의 순간 제작발표회)"},{"num":72,"time":"14:50","minute":890,"title":"[포토]신승호, 축구선수 출신 연기자"},{"num":73,"time":"14:50","minute":890,"title":"[동아포토]신승호,부끄부끄"},{"num":74,"time":"14:50","minute":890,"title":"[TD포토] 김향기 매너손에 폭소하는 옹성우-신승호"},{"num":75,"time":"14:51","minute":891,"title":"‘열여덟의 순간’ 반장 신승호의 모델 포스"},{"num":76,"time":"14:52","minute":892,"title":"[포토]'열여덟의 순간' 제작발표회, 포즈 취하는 신승호"},{"num":77,"time":"14:52","minute":892,"title":"[TD포토] 김향기 '좌 옹성우-우 신승호'든든한 팔짱"},{"num":78,"time":"14:54","minute":894,"title":"신승호,'우월한 수트핏'"},{"num":79,"time":"14:54","minute":894,"title":"옹성우-김향기-신승호-강기영-심나연 감독, 주역들 (열여덟의 순간 제작발표회)"},{"num":80,"time":"14:55","minute":895,"title":"[포토] '열여덟의 순간' 옹성우-김향기-신승호, 세 배우의 하트"},{"num":81,"time":"14:55","minute":895,"title":"[포토] 신승호, 완벽하지만 미숙한 아이"},{"num":82,"time":"14:55","minute":895,"title":"[TD포토] 강기영-옹성우-김향기-신승호 '힘찬 화이팅~'"},{"num":83,"time":"14:56","minute":896,"title":"열여덟의 순간' 신승호 \"'에이틴' 이어 청춘물..'공감' 노력\""},{"num":84,"time":"14:57","minute":897,"title":"[포토] 옹성우-김향기, 신승호, 학생들의 하트"},{"num":85,"time":"14:57","minute":897,"title":"<포토>옹성우-김향기-신승호 '기대되는 케미'"},{"num":86,"time":"14:59","minute":899,"title":"[MD포토] 축구선수 출신 탤런트 신승호 '훤칠한 등장'"},{"num":87,"time":"15:00","minute":900,"title":"열여덟의 순간' 신승호 \"'에이틴' 이어 청춘물, 학생役 할 수 있어 감사해\""},{"num":88,"time":"15:01","minute":901,"title":"[포토]신승호, '열여덟의 순간' 기대해주세요!"},{"num":89,"time":"15:01","minute":901,"title":"[bnt포토] 신승호 '훈훈한 손인사'"},{"num":90,"time":"15:02","minute":902,"title":"[MD포토] 신승호 '매력적인 보조개'"},{"num":91,"time":"15:02","minute":902,"title":"[bnt포토] 신승호 '웃음 참기 힘드네~'"},{"num":92,"time":"15:02","minute":902,"title":"[오마이포토] '열여덟의 순간' 옹성우-신승호, 선배 김향기따라"},{"num":93,"time":"15:04","minute":904,"title":"[TEN PHOTO]신승호 '훈훈한 인사'"},{"num":94,"time":"15:04","minute":904,"title":"옹성우-김향기-신승호 '풋풋한 조합'[엑's HD포토]"},{"num":95,"time":"15:04","minute":904,"title":"[조이HD]옹성우-김향기-신승호, 순정만화 주인공처럼~"},{"num":96,"time":"15:04","minute":904,"title":"[조이HD]김향기, 옹성우-신승호 사이에서 어쩔줄 몰라~"},{"num":97,"time":"15:04","minute":904,"title":"인사말하는 신승호 (열여덟의 순간 제작발표회)"},{"num":98,"time":"15:04","minute":904,"title":"[현장] 신승호 \"25살에 고등학생 연기, 시청자 공감위해 노력\"('열여덟의순간')"},{"num":99,"time":"15:05","minute":905,"title":"[TEN PHOTO]신승호 '축구선수 출신의 우월한 피지컬'"},{"num":100,"time":"15:05","minute":905,"title":"[포토]신승호, '열여덟의 순간'으로 인사드려요!"},{"num":101,"time":"15:05","minute":905,"title":"[bnt포토] 옹성우-신승호 '김향기 매너손에 빵 터졌어요~'"},{"num":102,"time":"15:05","minute":905,"title":"[조이HD]'열여덟의 순간' 신승호, 훈훈한 외모"},{"num":103,"time":"15:06","minute":906,"title":"[MD포토] 옹성우,김향기,신승호 '열여덟의 순간' 기대하세요!"},{"num":104,"time":"15:07","minute":907,"title":"[조이HD]신승호, 깜빡하고 셔츠 놓고 왔어요~"},{"num":105,"time":"15:08","minute":908,"title":"[포토]'열여덟의 순간' 주연 맡은 옹성우-김향기-신승호"},{"num":106,"time":"15:08","minute":908,"title":"[T포토] 신승호 '터져버린 웃음'"},{"num":107,"time":"15:08","minute":908,"title":"신승호, 듬직한 피지컬 (열여덟의 순간)"},{"num":108,"time":"15:08","minute":908,"title":"열여덟의 순간' 신승호 \"'에이틴' 성공 이후 부담감 생겨\""},{"num":109,"time":"15:10","minute":910,"title":"‘열여덟의 순간’ 김향기 “오랜만의 또래 호흡..옹성우∙신승호 낯설었다”"},{"num":110,"time":"15:11","minute":911,"title":"[MD포토] 옹성우,김향기,신승호 '달달한 포즈'"},{"num":111,"time":"15:11","minute":911,"title":"옹성우-김향기-신승호-강기영,'많은 사랑 부탁드려요'"},{"num":112,"time":"15:13","minute":913,"title":"[MD포토] 옹성우,김향기,강기영,신승호 '열여덟의 순간' 기대히세요!"},{"num":113,"time":"15:17","minute":917,"title":"강기영-옹성우-김향기-신승호, 반짝이는 화이팅 [포토엔HD]"},{"num":114,"time":"15:18","minute":918,"title":"신승호 '장신의 훈남'[엑's HD포토]"},{"num":115,"time":"15:18","minute":918,"title":"[포토] 옹성우-김향기-신승호, '열여덟의 순간' 사랑해 주세요~"},{"num":116,"time":"15:18","minute":918,"title":"신승호 '너무 과감한가?'[엑's HD포토]"},{"num":117,"time":"15:19","minute":919,"title":"열여덟의 순간' 김향기X용성우X신승호 실제 나이는?"},{"num":118,"time":"15:19","minute":919,"title":"신승호 '루즈핏 완벽 소화'[엑's HD포토]"},{"num":119,"time":"15:20","minute":920,"title":"[오마이포토] '열여덟의 순간' 옹성우-신승호, 김향기 매너손에 빵"},{"num":120,"time":"15:20","minute":920,"title":"[포토] 신승호, 말끔한 스타일"},{"num":121,"time":"15:21","minute":921,"title":"신승호, 갑자기 덥네요 [포토엔HD]"},{"num":122,"time":"15:24","minute":924,"title":"[포토]함께 하트 만들어보이는 옹성우-김향기-신승호"},{"num":123,"time":"15:25","minute":925,"title":"신승호 '강기영 입담에 덥다 더워'[엑's HD포토]"},{"num":124,"time":"15:27","minute":927,"title":"[포토]'열여덟의 순간'에서 호흡 맞추는 옹성우-김향기-신승호"},{"num":125,"time":"15:28","minute":928,"title":"[E-핫스팟] '열여덟의 순간', 옹성우X김향기X신승호의 '설렘 가득' 청춘물"},{"num":126,"time":"15:28","minute":928,"title":"[오마이포토] '열여덟의 순간' 강기영-옹성우-김향기-신승호, 18살 있는 그대로!"},{"num":127,"time":"15:29","minute":929,"title":"‘열여덟의 순간’ 신승호 “촬영장에서 열여덟로 살아갈 수 있어 감사”"},{"num":128,"time":"15:30","minute":930,"title":"[포토]옹성우-김향기-신승호, '열여덟의 순간' 기대해주세요!"},{"num":129,"time":"15:40","minute":940,"title":"[MD포토] 김향기 '옹성우,신승호에게 착한 팔짱은 이런거?'"},{"num":130,"time":"15:41","minute":941,"title":"[포토] 신승호, '우월한 비율 뽐내며~'"},{"num":131,"time":"15:42","minute":942,"title":"[포토] 신승호, '부드러운 손인사~'"},{"num":132,"time":"15:45","minute":945,"title":"[현장] 신예스타 등용문 옹성우-김향기-신승호…‘열여덟의 순간’, “학원물이지만 10대~30대까지 시청 가능한 드라마의 탄생” (종합)"},{"num":133,"time":"15:46","minute":946,"title":"[HD포토] 신승호, ‘올블랙으로 시크하게 등장’ (열여덟의순간)"},{"num":134,"time":"15:46","minute":946,"title":"[HD포토] 신승호, ‘모델 포스 뿜뿜’ (열여덟의순간)"},{"num":135,"time":"15:46","minute":946,"title":"[HD포토] 신승호, ‘훈훈한 비주얼’ (열여덟의순간)"},{"num":136,"time":"15:46","minute":946,"title":"[HD포토] 신승호, ‘더워서 셔츠 안 입었어요’ (열여덟의순간)"},{"num":137,"time":"15:46","minute":946,"title":"[HD포토] 신승호, ‘멋짐으로 무장’ (열여덟의순간)"},{"num":138,"time":"15:46","minute":946,"title":"[HD포토] 신승호, ‘어색한 손하트’ (열여덟의순간)"},{"num":139,"time":"15:46","minute":946,"title":"[HD포토] 옹성우-김향기-신승호, ‘풋풋한 삼각관계’ (열여덟의순간)"},{"num":140,"time":"15:46","minute":946,"title":"[HD포토] 옹성우-김향기-신승호, ‘우리 친해요’ (열여덟의순간)"},{"num":141,"time":"15:55","minute":955,"title":"[종합②] '열여덟의 순간' 옹성우-김향기-신승호, 무더위 날릴 청량케미 사단(ft.강기영)"},{"num":142,"time":"15:58","minute":958,"title":"옹성우 김향기 신승호 그릴 청춘 성장기, '열여덟의 순간'"},{"num":143,"time":"15:58","minute":958,"title":"[동아포토]옹성우-김향기-신승호, 기대되는 청춘 로맨스"},{"num":144,"time":"16:22","minute":982,"title":"[bnt포토] 옹성우-김향기-신승호 '케미 기대해주세요~'"},{"num":145,"time":"16:22","minute":982,"title":"옹성우에 신승호까지…김향기(Kim Hyang gi)가 전한 행복한 촬영 환경 ('열여덟의 순간' 제작발표회) [SS쇼캠]"},{"num":146,"time":"16:24","minute":984,"title":"[bnt포토] 강기영-옹성우-김향기-신승호 '열여덟의 순간 파이팅'"},{"num":147,"time":"16:27","minute":987,"title":"[포토] 옹성우-김향기-신승호-강기영 \"오늘(22일) 첫방송 본방사수 해주세요~\""},{"num":148,"time":"16:30","minute":990,"title":"‘열여덟의 순간’ 옹성우X김향기X신승호X강기영 훈훈함이 넘치는 ‘포토 타임’ [뉴스엔TV]"},{"num":149,"time":"16:41","minute":1001,"title":"[포토] '열여덟의 순간' 신승호, 잘생긴 외모로 시선강탈"},{"num":150,"time":"16:56","minute":1016,"title":"[TEN 현장] 옹성우·김향기·신승호의 만남…뜨겁고 치열한 '열여덟의 순간'이 온다"},{"num":151,"time":"17:11","minute":1031,"title":"신승호(Shin Seung ho), 셔츠 잊은 과감한 의상에 '수줍은 손' ('열여덟의 순간' 제작발표회) [SS쇼캠]"},{"num":152,"time":"17:12","minute":1032,"title":"[S영상] 옹성우 x 김향기 x 신승호, '매너손으로 시작 알려' ('열여덟의 순간' 제작발표회)"},{"num":153,"time":"17:17","minute":1037,"title":"[HD영상] ‘열여덟의 순간’ 신승호, “학창시절 부족했던 추억, 작품 통해 경험”(190722)"},{"num":154,"time":"17:36","minute":1056,"title":"[포토] '열여덟의 순간' 신승호, 캐릭터 살려 삐딱하게"},{"num":155,"time":"17:37","minute":1057,"title":"[포토] '열여덟의 순간' 신승호, 대형 멍뭉미"},{"num":156,"time":"18:20","minute":1100,"title":"[포토] ‘열여덟의 순간’ 옹성우-김향기-신승호 ‘깜찍한 손하트’"},{"num":157,"time":"18:25","minute":1105,"title":"[포토] ‘열여덟의 순간’ 신승호 ‘시원시원한 손인사’"},{"num":158,"time":"18:30","minute":1110,"title":"\"치열했다\"…'열여덟의 순간' 옹성우X김향기X신승호의 '18살 청춘' [엑's 현장]"},{"num":159,"time":"18:52","minute":1132,"title":"옹성우·김향기·신승호·강기영, 드라마 '열여덟의 순간' 주역들"},{"num":160,"time":"20:54","minute":1254,"title":"[포토] 신승호, 앗! 셔츠를 잊어버렸네! (JTBC 열여덟의 순간)"},{"num":161,"time":"21:22","minute":1282,"title":"옹성우·김향기·강기영·신승호·심나연 감독, 드라마 '열여덟의 순간' 파이팅"},{"num":162,"time":"21:29","minute":1289,"title":"열여덟의 순간' 옹성우·김향기·신승호 등 등장인물 관계도는?"},{"num":163,"time":"21:59","minute":1319,"title":"‘열여덟의 순간’ 옹성우, 전학 이유 말하려다 신승호에 저지"},{"num":164,"time":"22:00","minute":1320,"title":"옹성우, 신승호와 대립…“그럴 필요 없었다”(열여덟의 순간)"},{"num":165,"time":"22:00","minute":1320,"title":"‘열여덟의 순간’ 옹성우·신승호 묘한 긴장감 “어색하다고 거짓말하면 안 돼”"},{"num":166,"time":"22:03","minute":1323,"title":"열여덟의 순간' 옹성우X신승호 \"거짓말 하면 안 되지\"…묘한 신경전"},{"num":167,"time":"22:13","minute":1333,"title":"[현장영상] JTBC 드라마 ‘열여덟의 순간’ 제작발표회, 옹성우·김향기·신승호·강기영"},{"num":168,"time":"22:18","minute":1338,"title":"열여덟의 순간' 옹성우-김향기-신승호, 삼각관계? 인물 관계도-애정 관계는?"},{"num":169,"time":"22:30","minute":1350,"title":"신승호, 시크한 매력 (열여덟의 순간)"},{"num":170,"time":"22:34","minute":1354,"title":"[종합] ‘열여덟의 순간-첫방’ 옹성우, 허영지 편의점 도둑 잡고 알바시작…김향기-신승호 옹성우 과거 알고 ‘깜놀’"},{"num":171,"time":"22:48","minute":1368,"title":"열여덟의 순간' 옹성우X김향기X신승호, '설렘→긴장'…첫방부터 삼각관계 [줄거리]"},{"num":172,"time":"22:52","minute":1372,"title":"[종합]\"쓰레기는 너\"…'열여덟의 순간' 옹성우, 절도범으로 몰렸다→신승호와 대립"},{"num":173,"time":"22:53","minute":1373,"title":"열여덟의 순간' 옹성우x신승호, 묘한 긴장감 \"거짓말하면 안 되지\""},{"num":174,"time":"22:56","minute":1376,"title":"열여덟의 순간' 옹성우X신승호, 절도범 진실 놓고 날선 대립 [종합]"},{"num":175,"time":"23:00","minute":1380,"title":"열여덟의 순간' 옹성우, 김향기→신승호까지 첫방부터 위기 연속 [종합]"},{"num":176,"time":"23:09","minute":1389,"title":"열여덟의 순간' \"어쩔건데, 쓰레기야\" 옹성우, 김향기 반에 전학→신승호와 신경전(종합)"}]''')
BASE_DIR = Path(__file__).resolve().parent

def file_to_data_url(path_str: str) -> str:
    path = BASE_DIR / path_str
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"

special_media = {}
for num, config in SPECIAL_ARTICLES.items():
    special_media[num] = {
        "src": file_to_data_url(config["file"]),
        "duration": float(config["duration"]),
        "scroll": bool(config["scroll"]),
    }

st.markdown(
    """
    <style>
      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stStatusWidget"],
      #MainMenu,
      footer { display:none !important; }
      .block-container { max-width:none !important; padding:0 !important; }
      .stApp { background:#eeeeec; }
    </style>
    """,
    unsafe_allow_html=True,
)

payload = {
    "articles": ARTICLES,
    "activeSeconds": ACTIVE_TIMELINE_SECONDS,
    "leadInSeconds": LEAD_IN_SECONDS,
    "specialMedia": special_media,
}

html = r"""
<div id="j22-app">
  <div class="controls">
    <button id="replay" type="button">다시 시작 · R</button>
    <button id="pause" type="button">일시정지 · Space</button>
    <button id="fullscreen" type="button">전체화면 · F</button>
    <button id="start" type="button">재생 시작</button>
    <span>실제 기사 캡처를 포함한 176개 제목 타임라인</span>
  </div>

  <main id="stage" tabindex="0">
    <header class="masthead">
      <div class="date">2019.07.22</div>
      <div class="live-time" id="live-time">00:00</div>
      <div class="counter"><span id="counter">000</span> / 176</div>
    </header>

    <div class="timeline">
      <div class="timeline-track">
        <div class="timeline-progress" id="timeline-progress"></div>
        <div class="timeline-dot" id="timeline-dot"></div>
      </div>
      <div class="timeline-labels">
        <span class="timeline-label label-start" style="left:0%">00:00</span>
        <span class="timeline-label" style="left:59.236111%">14:13</span>
        <span class="timeline-label label-end" style="left:96.458333%">23:09</span>
      </div>
    </div>

    <section class="feed-wrap">
      <div class="feed-fade feed-fade-top"></div>
      <ol id="feed" class="feed"></ol>
      <div class="feed-fade feed-fade-bottom"></div>
    </section>

    <section id="media-card" class="media-card" aria-live="polite">
      <div class="media-header">
        <span id="media-num">001</span>
        <span id="media-time">00:00</span>
      </div>
      <div class="media-viewport" id="media-viewport">
        <img id="media-image" alt="기사 캡처" />
      </div>
    </section>

    <footer class="footer">
      <span>HEADLINES IN PUBLICATION ORDER</span>
      <span>REAL INTERVALS · LINEARLY COMPRESSED</span>
    </footer>

    <section id="end-card" class="end-card" aria-label="엔딩 크레딧">
      <div class="end-count">176</div>
      <div class="end-label">HEADLINES</div>
      <div class="end-rule"></div>
      <div class="end-date">2019.07.22</div>
      <div class="end-time">00:00—23:09</div>
      <div class="end-title">〈열여덟의 순간〉</div>
      <div class="end-info">제작발표회 · 첫 방송</div>

    </section>
  </main>
</div>

<script id="j22-payload" type="application/json">__PAYLOAD__</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Radley:ital@0;1&display=swap');

:root { color-scheme: light; }
* { box-sizing: border-box; }
#j22-app { min-height:100vh; padding:12px 12px 28px; display:flex; flex-direction:column; align-items:center; background:#eeeeec; color:#111; font-family:"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",Arial,sans-serif; }
.controls { width:min(720px,80vw); display:flex; align-items:center; gap:8px; margin-bottom:10px; font-size:12px; color:#565656; }
.controls button { appearance:none; border:1px solid #cfcfcb; border-radius:999px; background:#fff; color:#111; padding:8px 13px; font:inherit; cursor:pointer; white-space:nowrap; }
.controls span { margin-left:4px; }
#stage { position:relative; width:min(720px,80vw); aspect-ratio:4/5; overflow:hidden; background:#fff; border:1px solid #d8d8d3; box-shadow:0 16px 44px rgba(0,0,0,.10); outline:none; }
.masthead { position:absolute; inset:0 0 auto 0; height:10.6%; display:grid; grid-template-columns:1fr auto 1fr; align-items:end; padding:0 5.2% 2.5%; border-bottom:1px solid #d7d7d3; z-index:5; background:#fff; }
.date {
  font-family: "Radley", Georgia, serif;
  font-size: clamp(15px, 2vw, 28px);
  font-style: italic;
  font-weight: 700;
  letter-spacing: 0;
  font-variant-numeric: lining-nums tabular-nums;
}

.live-time {
  font-family: "Radley", Georgia, serif;
  font-size: clamp(24px, 3vw, 42px);
  font-style: italic;
  font-weight: 700;
  letter-spacing: 0;
  font-variant-numeric: lining-nums tabular-nums;
}

.counter {
  font-family: "Radley", Georgia, serif;
  font-size: clamp(15px, 2vw, 28px);
  font-style: italic;
  font-weight: 700;
  letter-spacing: 0;
  text-align: right;
  font-variant-numeric: lining-nums tabular-nums;
}
.timeline { position:absolute; left:5.2%; right:5.2%; top:10.2%; height:5.4%; z-index:4; }
.timeline-track { position:relative; height:1px; margin-top:2.5%; background:#dadad6; }
.timeline-progress { position:absolute; left:0; top:0; width:0%; height:1px; background:#111; }
.timeline-dot { position:absolute; top:50%; left:0%; width:8px; height:8px; border-radius:50%; background:#111; transform:translate(-50%,-50%); }
.timeline-labels { position:relative; height:1.4em; margin-top:1.2%; color:#81817c; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:clamp(8px,.85vw,13px); }
.timeline-label { position:absolute; top:0; transform:translateX(-50%); white-space:nowrap; }
.timeline-label::before { content:""; position:absolute; left:50%; top:-8px; width:1px; height:5px; background:#bdbdb8; }
.timeline-label.label-start { transform:none; }
.timeline-label.label-start::before { left:0; }
.timeline-label.label-end { transform:translateX(-100%); }
.timeline-label.label-end::before { left:100%; }
.feed-wrap { position:absolute; left:5.2%; right:5.2%; top:19.2%; bottom:8.5%; overflow:hidden; }
.feed {
  position:absolute; left:0; right:0; bottom:0; margin:0;
  padding:0 0 15% 0; list-style:none; display:flex; flex-direction:column;
  gap:clamp(9px,1.15vh,16px);
}
.feed-item {
  display:grid; grid-template-columns:7.2% 9.8% 1fr; column-gap:2%; align-items:start;
  padding-bottom:clamp(7px,.8vh,12px); border-bottom:1px solid #ecece8;
  opacity:.34; transform:translateY(18px);
  transition:opacity 180ms ease, transform 240ms ease;
}
.feed-item.visible { opacity:.52; transform:translateY(0); }
.feed-item.current { opacity:1; }
.feed-num,.feed-time {
  color:#555550; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:clamp(10px,1.05vw,16px); line-height:1.45; padding-top:.15em;
}
.feed-title {
  color:#111; font-size:clamp(15px,1.8vw,27px); font-weight:430;
  line-height:1.38; letter-spacing:-.025em; word-break:keep-all; overflow-wrap:anywhere;
}
.feed-item.current .feed-num,
.feed-item.current .feed-time { color:#111; font-weight:700; }
.feed-item.current .feed-title { font-weight:760; }
.feed-fade { position:absolute; left:0; right:0; height:12%; z-index:3; pointer-events:none; }
.feed-fade-top { top:0; background:linear-gradient(#fff 8%, rgba(255,255,255,0)); }
.feed-fade-bottom { bottom:0; height:4%; background:linear-gradient(rgba(255,255,255,0), #fff 92%); }
.media-card { position:absolute; left:4.2%; right:4.2%; top:16.2%; bottom:7.2%; z-index:20; display:flex; flex-direction:column; gap:1.8%; padding:2.2%; background:rgba(255,255,255,.985); border:1px solid #111; opacity:0; visibility:hidden; transform:translateY(18px); transition:opacity 220ms ease, transform 220ms ease, visibility 0s linear 220ms; }
.media-card.show { opacity:1; visibility:visible; transform:translateY(0); transition-delay:0s; }
.media-header { display:flex; justify-content:space-between; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:clamp(12px,1.4vw,20px); font-weight:650; padding-bottom:.5%; color:#111; }
.media-viewport {
  position:relative;
  flex:1;
  overflow:hidden;
  border:1px solid #d9d9d4;
  background:#fafaf8;
  display:flex;
  align-items:center;
  justify-content:center;
}
.media-viewport img {
  position:static;
  width:auto;
  height:auto;
  max-width:540px;
  max-height:100%;
  object-fit:contain;
  display:block;
  transform:none !important;
  user-select:none;
  -webkit-user-drag:none;
}
.footer { position:absolute; left:5.2%; right:5.2%; bottom:3.2%; display:flex; justify-content:space-between; color:#777772; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:clamp(7px,.75vw,11px); letter-spacing:.05em; }
.end-card {
  position:absolute;
  left:0;
  right:0;
  top:10.65%;
  bottom:0;
  z-index:35;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  padding:5% 8% 8%;
  background:#fff;
  color:#090909;
  opacity:0;
  visibility:hidden;
  transform:translateY(12px);
  transition:
    opacity 520ms ease,
    transform 520ms ease,
    visibility 0s linear 520ms;
  pointer-events:none;
  text-align:center;
}

.end-card.show {
  opacity:1;
  visibility:visible;
  transform:translateY(0);
  transition-delay:0s;
}

.end-count {
  font-family:"Radley", Georgia, serif;
  font-style:italic;
  font-weight:700;
  font-size:clamp(68px,10vw,104px);
  line-height:.86;
  font-variant-numeric:lining-nums tabular-nums;
}

.end-label {
  margin-top:1.8%;
  font-family:"Radley", Georgia, serif;
  font-style:italic;
  font-weight:700;
  font-size:clamp(20px,3vw,34px);
  letter-spacing:.08em;
}

.end-rule {
  width:44px;
  height:1px;
  margin:5.5% 0 4.5%;
  background:#111;
}

.end-date,
.end-time {
  font-family:"Radley", Georgia, serif;
  font-style:italic;
  font-weight:700;
  font-variant-numeric:lining-nums tabular-nums;
}

.end-date {
  font-size:clamp(23px,3.4vw,38px);
}

.end-time {
  margin-top:.8%;
  font-size:clamp(16px,2.1vw,24px);
}

.end-title {
  margin-top:5%;
  font-size:clamp(18px,2.4vw,27px);
  font-weight:700;
  letter-spacing:-.035em;
}

.end-info {
  margin-top:1.2%;
  color:#555550;
  font-size:clamp(12px,1.55vw,18px);
  letter-spacing:.02em;
}

.end-credit {
  margin-top:6%;
  color:#777772;
  font-family:"Radley", Georgia, serif;
  font-style:italic;
  font-size:clamp(10px,1.2vw,14px);
  letter-spacing:.08em;
}
#stage:fullscreen { width:min(80vw,64vh); height:auto; max-width:none; aspect-ratio:4/5; border:none; box-shadow:none; }
@media (max-width:700px) { #j22-app { padding:6px 3px 20px; } .controls { width:80vw; flex-wrap:wrap; font-size:10px; } .controls span { width:100%; } #stage { width:80vw; } }
</style>

<script>
(() => {
  "use strict";
  if (window.__j22Timeline && typeof window.__j22Timeline.destroy === "function") window.__j22Timeline.destroy();

  const payload = JSON.parse(document.getElementById("j22-payload").textContent);
  const articles = payload.articles;
  const specialMedia = payload.specialMedia || {};
  const ACTIVE_SECONDS = payload.activeSeconds;
  const LEAD_IN = payload.leadInSeconds;
  const DAY_MINUTES = 24 * 60;

  const stage = document.getElementById("stage");
  const feed = document.getElementById("feed");
  const liveTime = document.getElementById("live-time");
  const counter = document.getElementById("counter");
  const progress = document.getElementById("timeline-progress");
  const dot = document.getElementById("timeline-dot");
  const mediaCard = document.getElementById("media-card");
  const mediaNum = document.getElementById("media-num");
  const mediaTime = document.getElementById("media-time");
  const mediaViewport = document.getElementById("media-viewport");
  const mediaImage = document.getElementById("media-image");
  const endCard = document.getElementById("end-card");
  const startButton = document.getElementById("start");
  const replayButton = document.getElementById("replay");
  const pauseButton = document.getElementById("pause");
  const fullscreenButton = document.getElementById("fullscreen");

  const events = articles.map(article => ({
    ...article,
    eventTime: (article.minute / DAY_MINUTES) * ACTIVE_SECONDS,
  }));

  let rafId = null, previousTimestamp = null, wallElapsed = 0, activeElapsed = 0, nextIndex = 0;
  let userPaused = false, started = false, specialRemaining = 0, currentSpecial = null, scrollMax = 0, finished = false, post176Blank = false, destroyed = false;
  let renderedItems = [];

  function pad3(v) { return String(v).padStart(3, "0"); }
  function minuteToClock(x) {
    const minute = Math.max(0, Math.min(DAY_MINUTES, Math.floor(x + 1e-9)));
    if (minute === DAY_MINUTES) return "24:00";
    return `${String(Math.floor(minute / 60)).padStart(2, "0")}:${String(minute % 60).padStart(2, "0")}`;
  }
  function updateClock() {
    const ratio = Math.max(0, Math.min(1, activeElapsed / ACTIVE_SECONDS));
    liveTime.textContent = minuteToClock(ratio * DAY_MINUTES);
    progress.style.width = `${ratio * 100}%`;
    dot.style.left = `${ratio * 100}%`;
  }
  function addFeedItem(article) {
    for (const item of renderedItems) item.classList.remove("current");
    const li = document.createElement("li");
    li.className = "feed-item";
    li.innerHTML = `<span class="feed-num">${pad3(article.num)}</span><span class="feed-time">${article.time}</span><span class="feed-title"></span>`;
    li.querySelector(".feed-title").textContent = article.title;
    feed.appendChild(li);
    renderedItems.push(li);
    while (renderedItems.length > 7) renderedItems.shift().remove();
    requestAnimationFrame(() => li.classList.add("visible", "current"));
    counter.textContent = pad3(article.num);
  }
  function recomputeScrollMax() {
    scrollMax = Math.max(0, mediaImage.getBoundingClientRect().height - mediaViewport.clientHeight);
  }
  mediaImage.addEventListener("load", () => { scrollMax = 0; });
  window.addEventListener("resize", recomputeScrollMax);
  function showSpecial(article, config) {
    currentSpecial = { article, duration: config.duration, scroll: false };
    specialRemaining = config.duration;
    mediaNum.textContent = pad3(article.num);
    mediaTime.textContent = article.time;
    mediaImage.src = config.src;
    
    mediaCard.classList.add("show");
    requestAnimationFrame(recomputeScrollMax);
  }
  function hideSpecial() {
    specialRemaining = 0;
    currentSpecial = null;
    mediaCard.classList.remove("show");
    
  }
  function updateSpecialAnimation() {
    // 모든 기사 캡처는 001번과 같은 크기로 상단 고정한다.
  }
  function processEvents() {
    while (nextIndex < events.length && events[nextIndex].eventTime <= activeElapsed + 1e-9) {
      const article = events[nextIndex];

      // 특수 기사 화면이 등장할 때 타이머를 발행 시각에 정확히 맞춘다.
      if (specialMedia[article.num]) {
        activeElapsed = article.eventTime;
        updateClock();

        if (article.num === 176) {
          // 마지막 기사는 제목 목록에 추가하지 않고 캡처만 보여준다.
          counter.textContent = pad3(article.num);
          showSpecial(article, specialMedia[article.num]);
          post176Blank = true;
          nextIndex += 1;
          return;
        }

        addFeedItem(article);
        showSpecial(article, specialMedia[article.num]);
        nextIndex += 1;
        return;
      }

      addFeedItem(article);
      nextIndex += 1;
    }
  }
  function reset() {
    wallElapsed = 0; activeElapsed = 0; nextIndex = 0; userPaused = false; started = false;
    specialRemaining = 0; currentSpecial = null; scrollMax = 0; finished = false; post176Blank = false; previousTimestamp = null;
    feed.innerHTML = ""; renderedItems = []; counter.textContent = "000"; liveTime.textContent = "00:00";
    progress.style.width = "0%"; dot.style.left = "0%"; hideSpecial();
    endCard.classList.remove("show");

    // 첫 화면부터 001번 기사와 캡처를 보여준다.
    const firstArticle = events[0];
    addFeedItem(firstArticle);
    showSpecial(firstArticle, specialMedia[firstArticle.num]);
    specialRemaining = specialMedia[firstArticle.num].duration;
    nextIndex = 1;

    pauseButton.textContent = "일시정지 · Space"; startButton.textContent = "재생 시작";
  }
  function startPlayback() {
    if (!started) {
      started = true;
      wallElapsed = LEAD_IN;
      endCard.classList.remove("show");
      startButton.textContent = "재생 중";
      stage.focus();
    }
  }
  function replayNow() { reset(); startPlayback(); }
  function togglePause() { if (!started) startPlayback(); userPaused = !userPaused; pauseButton.textContent = userPaused ? "재생 · Space" : "일시정지 · Space"; }
  async function toggleFullscreen() { try { if (!document.fullscreenElement) await stage.requestFullscreen(); else await document.exitFullscreen(); } catch (_) {} }
  function frame(timestamp) {
    if (destroyed) return;
    if (previousTimestamp === null) previousTimestamp = timestamp;
    const dt = Math.min((timestamp - previousTimestamp) / 1000, 0.1);
    previousTimestamp = timestamp;
    if (!userPaused && started) {
      wallElapsed += dt;
      if (wallElapsed >= LEAD_IN) {
        if (specialRemaining > 0) {
          specialRemaining -= dt;
          updateSpecialAnimation();
          if (specialRemaining <= 0) {
            specialRemaining = 0;
            const was176 = currentSpecial && currentSpecial.article && currentSpecial.article.num === 176;
            hideSpecial();

            if (was176) {
              feed.innerHTML = "";
              renderedItems = [];
              post176Blank = true;
            }
          }
        } else if (!finished && activeElapsed < ACTIVE_SECONDS) {
          let remaining = dt;

          while (remaining > 0 && !finished && specialRemaining <= 0) {
            const nextEventTime = nextIndex < events.length
              ? events[nextIndex].eventTime
              : ACTIVE_SECONDS;

            if (activeElapsed + remaining >= nextEventTime - 1e-9) {
              const used = Math.max(0, nextEventTime - activeElapsed);
              activeElapsed = nextEventTime;
              remaining -= used;
              updateClock();
              processEvents();

              // 기사 한 건을 화면에 그린 뒤 다음 프레임에서 다음 기사로 넘어간다.
              // 동일한 발행 시각의 기사도 타이머는 그대로 둔 채 빠르게 한 단씩 올라간다.
              remaining = 0;
              break;
            } else {
              activeElapsed = Math.min(ACTIVE_SECONDS, activeElapsed + remaining);
              remaining = 0;
              updateClock();
            }
          }

          if (activeElapsed >= ACTIVE_SECONDS - 1e-9) {
            activeElapsed = ACTIVE_SECONDS;
            updateClock();
            finished = true;
            counter.textContent = "176";
            startButton.textContent = "재생 완료";
            feed.innerHTML = "";
            renderedItems = [];
            hideSpecial();
            endCard.classList.add("show");
          }
        }
      }
    }
    rafId = requestAnimationFrame(frame);
  }
  function onKeydown(event) {
    if (event.key === "r" || event.key === "R") replayNow();
    else if (event.key === " ") { event.preventDefault(); togglePause(); }
    else if (event.key === "f" || event.key === "F") toggleFullscreen();
  }
  startButton.addEventListener("click", startPlayback);
  replayButton.addEventListener("click", replayNow);
  pauseButton.addEventListener("click", togglePause);
  fullscreenButton.addEventListener("click", toggleFullscreen);
  stage.addEventListener("dblclick", toggleFullscreen);
  window.addEventListener("keydown", onKeydown);
  window.__j22Timeline = {
    destroy() {
      destroyed = true;
      if (rafId) cancelAnimationFrame(rafId);
      window.removeEventListener("keydown", onKeydown);
      window.removeEventListener("resize", recomputeScrollMax);
      startButton.removeEventListener("click", startPlayback);
      replayButton.removeEventListener("click", replayNow);
      pauseButton.removeEventListener("click", togglePause);
      fullscreenButton.removeEventListener("click", toggleFullscreen);
      stage.removeEventListener("dblclick", toggleFullscreen);
    }
  };
  reset();
  rafId = requestAnimationFrame(frame);
})();
</script>
"""
html = html.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
components.html(html, height=1280, scrolling=False)
