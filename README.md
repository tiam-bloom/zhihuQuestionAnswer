
# 仅供学习


























----------------


## 要求

问题链接：
https://www.zhihu.com/question/597272501
https://www.zhihu.com/question/601307254
https://www.zhihu.com/question/605656495

https://www.zhihu.com/question/606309719
https://www.zhihu.com/question/609890590
http://www.zhihu.com/question/610276483

http://www.zhihu.com/question/610276645
http://www.zhihu.com/question/610276645
http://www.zhihu.com/question/610393993

http://www.zhihu.com/question/610963260
http://www.zhihu.com/question/614881513
http://www.zhihu.com/question/623287280

http://www.zhihu.com/question/646529705
http://www.zhihu.com/question/647322856

然后需要爬取的字段包括：回答内容；作者name, ip,时间，赞同数，评论

## 通过ajax

https://www.zhihu.com/question/597272501

- /api/v4/questions/597272501/feeds

> 它直接从第二页开始请求，没找到第一页的数据在哪里

```js
	data.data.map(item => {const { id,author:{name,id:author_id},created_time,voteup_count,excerpt,content,comment_count } = item.target; return { id,name,author_id,created_time,voteup_count,excerpt,content,comment_count };})
```

```json
    {
        "id": 2997543151,
        "name": "江左梅郎",
        "author_id": "20d53f4539836859255161cccb8a2b1f",
        "created_time": 1682255115,
        "voteup_count": 148,
        "excerpt": "所谓的“全职儿女”，其实反映的是 代际收入倒挂的现象，说到底是个分配问题。看过一个网友说，自己全家三代人，最年轻的自己，是收入最少的。 爷爷奶奶，爸爸妈妈，或者是公务员，或者是教师、事业单位，拿工资的拿工资，拿退休金的也有七八千。 只有自己打工，一个月三千。 爸爸妈妈如果正当年倒没啥，但年轻人初入社会就被退休人士秒，再加上现今的人口结构，未来就堪忧了… 你说要是换我是这个网友，我还出去打啥工啊，爷爷…",
        "content": "<p data-pid=\导致的求职怪相。</p>",
        "comment_count": 44
    },
```

```json
data.paging
{
    "page": 2,
    "is_end": false,
    "next": "https://www.zhihu.com/api/v4/questions/597272501/feeds?cursor=4fc59e4483eeacba64228349e2e12731&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=2&order=default&platform=desktop&session_id=1710496222490587106"
}
```


URL下一页相比, 变化了三个参数

- cursor
- offset
- session_id
  但是重复请求一个URL， page会变下一页， 数据没变

签名参数`x-zse-96`
`2.0_Zp6h70+oC9x59K6=UkJ8zB+MBSYKv4XM8Ij=Cy0P58xLFpK8fwH+C51Tork0t4pZ`

```python
headers = {  
    'authority': 'www.zhihu.com',  
    'accept': '*/*',  
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',  
    'cache-control': 'no-cache',  
    # KLBRSID第二位, 当前时间戳  
    'cookie': '_xsrf=dffd11af-96c7-4e64-a5bd-87f0236e6cdf; _zap=de483e18-f5a6-4944-88b9-deb889f044f4; d_c0=AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009; YD00517437729195%3AWM_TID=yIl0kbDqFKhEVRQRRVeFOc8MDFFmX%2BLp; YD00517437729195%3AWM_NI=9X%2BrFmVsfYWtacM0JWY2mFTeC6ZO3n31MNGaIfjSVvIKiB%2FT95g0v5QQhNgqPgNHyZH7OmSX%2FLTpDkqY5cuR3UWyUNpOJredW7pyrzc%2B1vvHC1fGWPTncw%2FBasC0kUJSa2Q%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee8bf07eede8ad90f47b96a88ba6c44e939a8f82c16ef497f88ad85985afa691d72af0fea7c3b92afb88e593c56796adaabad680a3bd83d1c95d9beea3a7d76f81ea96b0b266f1ef83afc66b8bbaa6b4d57e8b95a7a3ae60fbeba9d1f53f938fa8afe67b94b982a9fc528ce9818ed254ed949c91c761b387fb84f85af18b999ad846b4918693e87095e9c09af172a1f5ff97f54481efaaa8d65c98b2ad98ae4aa3ad8dd1ea5f8a8dafd3d437e2a3; q_c1=e6dda5fd70234573a66d021b9007c6bc|1699596026000|1699596026000; z_c0=2|1:0|10:1710128054|4:z_c0|80:MS4xeHVMTkJ3QUFBQUFtQUFBQVlBSlZUVi02eldiZWU1TTlGZmZYQnUtLVV1bnRxd3VsU3V3c1lRPT0=|48e1c3a23f0be5fa53ab7a5fbb5463278eeb696c4454083f4fd4edd3badd8c33; KLBRSID=37f2e85292ebb2c2ef70f1d8e39c2b34|1710506575|1710504773',  
    'pragma': 'no-cache',  
    'referer': 'https://www.zhihu.com/question/597272501',  
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',  
    'sec-ch-ua-mobile': '?0',  
    'sec-ch-ua-platform': '"Windows"',  
    'sec-fetch-dest': 'empty',  
    'sec-fetch-mode': 'cors',  
    'sec-fetch-site': 'same-origin',  
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',  
    'x-requested-with': 'fetch',  
    'x-zse-93': '101_3_3.0',  
    'x-zse-96': '2.0_xtrmYKADSJDo1w=j7Yq51TIb+j=v46Io1t4FVPB1ioZO2DZ2g2yUIWXITemFLT=R',  # 签名算法  
}  
  
params = (  
    ('cursor', '5f6b4e190cef4a5d6a32da2e279ef1db'),  # 游标  
    ('include',  
     'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled'),  
    ('limit', '5'),  
    ('offset', '1'),  
    ('order', 'default'),  
    ('platform', 'desktop'),  
    ('session_id', '1710506575278007877'),   # 会话ID  
)
```



![[Pasted image 20240316110827.png]]

![[Pasted image 20240316101424.png]]


tO
'=07zUvPYov64ypbLQcQrYZUHeJlWuzKb8bf9y+WH0=25d8bUgYx3uj=c7q1+VfaR'
![[Pasted image 20240316102127.png]]


```JavaScrip
(0,tJ(ti).encrypt)(ty()(tp))




tp: '101_3_3.0+/api/v3/entity_word?type=answer&token=3000598929+AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009'

ty()(tp):   md5加密tp   =>  2a2f73d510e97331c53c98234f6be305

encrypt(MD5(tp))



```


看tp有什么组成
![[Pasted image 20240316103656.png]]


tp:   version+path+dc0


dc0:   'AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009'

 AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|{时间戳}

![[Pasted image 20240316111622.png]]

![[Pasted image 20240316121450.png]]


不同的question

- question_id
- cursor
- session_id
- cookie时间戳
- refer
- x-zse-96

---


| https://www.zhihu.com/question/ | 实有回答数 | 应有回答数 |
| ------------------------------- | ---------- | ---------- |
| 597272501                       | 560        | 583        |
| 601307254                       | 5          | 5          |
| 605656495                       | 414        | 432        |
| 606309719                       | 13         | 13         |
| 609890590                       | 208        | 212        |
| 610276483                       | 222        | 228        |
| 610276645                       | 250        | 256        |
| 610276645                       |            |            |
| 610393993                       | 2          | 2          |
| 610963260                       | 1          | 1          |
| 614881513                       | 6          | 6          |
| 623287280                       | 7          | 7          |
| 646529705                       | 22         | 22         |
| 647322856                       | 11         | 13         |


## 评论

回答评论URL:

/api/v4/comment_v5/answers/2997543151/root_comment


data.data.map(item => item.content);

data.data.map(item => {let {content,child_comment_count,child_comments} = item; child_comments = child_comments.map(item => item.content);return {content,child_comment_count, child_comments}})


```json
    {

        "content": "朝九晚五，周末双休，公款看病，包吃包住。你就说吧，哪点不符合？",

        "child_comment_count": 14,

        "child_comments": [

            "<p>说不定还能考个本科研究生呢……[大笑]</p>",

            "在职研究生[doge]"

        ]

    },

    {

        "content": "囚犯是真有工作，还有工资[惊喜]",

        "child_comment_count": 7,

        "child_comments": [

            "生病免费医疗。去医院专人看护。超国民待遇。",

            "<p>有，很低而已，但正经的工作时间真是8小时，剩下的时候是学习 跑操 看新闻联播 等等。颇有一种7 80年代上班之余上夜校充电的感觉。</p>"

        ]

    },
```