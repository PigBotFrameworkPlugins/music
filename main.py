import sys, requests, re, json
import urllib.request
import urllib.error
import urllib.parse
from pyncm import apis
sys.path.append('../..')
import go

def get_all_hotSong():  # 获取热歌榜所有歌曲名称和id
    url = 'http://music.163.com/discover/toplist?id=3778678'  # 网易云云音乐热歌榜url
    header = {  # 请求头部
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=header)
    html = urllib.request.urlopen(request).read().decode('utf8')  # 打开url
    html = str(html)  # 转换成str
    pat1 = r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>'  # 进行第一次筛选的正则表达式
    result = re.compile(pat1).findall(html)  # 用正则表达式进行筛选
    result = result[0]  # 获取tuple的第一个元素

    pat2 = r'<li><a href="/song\?id=\d*?">(.*?)</a></li>'  # 进行歌名筛选的正则表达式
    pat3 = r'<li><a href="/song\?id=(\d*?)">.*?</a></li>'  # 进行歌ID筛选的正则表达式
    hot_song_name = re.compile(pat2).findall(result)  # 获取所有热门歌曲名称
    hot_song_id = re.compile(pat3).findall(result)  # 获取所有热门歌曲对应的Id

    return hot_song_name, hot_song_id


def music_hot_search(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    # data = apis.playlist.GetTopPlaylists()
    # data = requests.get(meta_data.get('botSettings').get('musicApi')+'search/hot/detail').json().get('data')
    data = get_all_hotSong()
    message = '[CQ:face,id=189] 网易云热搜列表：'
    
    limit = meta_data.get('message') or 10
    i = 0
    while i < int(limit):
        message += '\n[CQ:face,id=161] 歌曲名：'+str(data[0][i])+'\n     歌曲ID：'+str(data[1][i])
        i += 1
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