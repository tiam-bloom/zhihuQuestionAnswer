# _*_ coding : UTF-8 _*_
# @Time : 2024/3/15 22:32
# @Auther : Tiam
# @File : signature
# @Project : 20240315-python查错
# @Desc :
import execjs


def x_zse_96(url):
    return execjs.compile('zhihuvmp.js.js').call('Q', url)


print(x_zse_96(
    'https://www.zhihu.com/api/v4/questions/597272501/feeds?cursor=d99f5d5d8c79f1c4c1fb7d2f12bbeb5d&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=10&order=default&platform=desktop&session_id=1710511820340323582'))
