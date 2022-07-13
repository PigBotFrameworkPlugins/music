import sys, requests
from pyncm import apis
sys.path.append('../..')
import go

def music_hot_search(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    data = requests.get(meta_data.get('botSettings').get('musicApi')+'search/hot/detail').json().get('data')
    message = '[CQ:face,id=189] 网易云热搜列表：'
    for i in data:
        message += '\n[CQ:face,id=161] 搜索词：'+str(i.get('searchWord'))+'\n     搜索次数：'+str(i.get('score'))
    go.send(meta_data, message)

def play_music(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if ' ' in message:
        message = message.split(' ')
        i = 1
        try:
            page = int(message[-1])
        except Exception as e:
            page = 1
            i = 0
        if page != message[1]:
            num = len(message)-i
            songList = message[0:num]
            song = ''
            for i in songList:
                song += i+' '
        else:
            song = message[0]
    else:
        page = 1
        song = message
    
    data = apis.cloudsearch.GetSearchResult(keyword=song, limit=meta_data.get('botSettings').get('musicApiLimit'), offset=(page-1)*meta_data.get('botSettings').get('musicApiLimit'))
    go.send(meta_data, 'limit={0}, offset={1}'.format(meta_data.get('botSettings').get('musicApiLimit'), (page-1)*meta_data.get('botSettings').get('musicApiLimit')))
    
    message = '[CQ:face,id=189] 歌曲：'+str(song)+' 的搜索结果'
    for i in data.get('songs'):
        message += '\n[CQ:face,id=161] 歌曲ID：'+str(i.get('id'))+'\n     歌曲名：'+str(i.get('name'))+'\n     作者：'
        for l in i.get('ar'):
            message += str(l.get('name'))+'、'
    message += '\n\n查看下一页请发送“搜歌 '+str(song)+' '+str(page+1)+'”'
    go.send(meta_data, message)
    
def get_music_url(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if message.isdigit():
        go.send(meta_data, '[CQ:music,type=163,id='+str(message)+']')
    else:
        data = requests.get(meta_data.get('botSettings').get('musicApi')+'search?keywords='+str(message)+'&limit=1').json().get('result').get('songs')
        go.send(meta_data, '[CQ:music,type=163,id='+str(data[0]['id'])+']')