# -*- coding: utf-8 -*-
"""
    Viki Downloader descarga subtitulos y videos de episodios de Viki en srt y mp4 respectivamente.
    
    Uso: vikidownloader.py url [-s] [--lang IDIOMA] [--v]
    
    positional arguments:
      url                   URL del video de Viki
    optional arguments:
      -h, --help            Muestra este mensaje y la aplicación cierra
      -s, --subs            Muestra todos los subtitulos disponibles
      --lang LANG           Codigo ISO del idioma
      -v, --video           Descarga el video

    Ejemplo:
    python vikidownloader.py http://www.viki.com/videos/1105299v-w-episode-1 --lang en -v

"""
import sys
import time
import urlparse
import argparse
import urllib2
import re
import json
import hmac
import binascii
from hashlib import sha1
import wget

class Viki():
    _APP = '65535a'
    _KEY = '-$iJ}@p7!G@SyU/je1bEyWg}upLu-6V6-Lg9VD(]siH,r.,m-r|ulZ,U4LC/SeR)'
    _APIURL = 'http://api.viki.io'
    _APIPATH = '/v4/'
    
    video_id = None
    subtitle = None
    video_title = None
    languages = {}

    def __init__(self,url=None):
        self.video_id = self.getVideoID(url)
        self.video_title = self.getVideoTitle(url)
        self.languages = self.getLanguages()

    def downloadSub(self,lang):
        """Descarga el subtitulo"""
        if lang in self.languages.keys():
            print "Descargando subtitulo"
            raw = self._APIPATH + 'videos/' + self.video_id + '/subtitles/' + lang + '.srt?app=' + self._APP + '&t=' + self.getTimestamp() + '&site=www.viki.com'
            hashed = hmac.new(self._KEY, raw, sha1)
            sub_url = self._APIURL + raw + '&sig=' + binascii.hexlify(hashed.digest())
            subtitle = self.requestURL(sub_url).read()
            subtitle = subtitle.replace('<br>','\n')

            filename = self.video_title.replace('-','_')
            
            output = file('%s_%s.srt'%(self.video_title,lang),'w')
            output.write(subtitle)
            output.close()
            print '%s Subtitulo descargado\n'%(self.video_title)
        else:
            print 'Subtitulo no disponible'
            sys.exit()

    def downloadVideo(self):
        """Descarga el video"""
        stream_url = self.getVideoStream().replace('&amp;','&')
        if stream_url:            
            try:
                print "Descargando video"                
                filename = wget.download(stream_url)
                print "%s Descargado."%(filename)
            except Exception as e:
                print e
        else:
            print "Video no Disponible"
            sys.exit()           

    def getLanguages(self):
        """Obtiene todos los idiomas disponibles"""
        json_url = self._APIURL + self._APIPATH + 'videos/' + self.video_id + '.json?app=' + self._APP + '&t=' + self.getTimestamp()
        try:
            content = json.load(self.requestURL(json_url))
            return content['subtitle_completions']
        except Exception as e:
            print e

    def getVideoStream(self):
        """Obtiene el URL del Video"""
        #http://www.viki.com/player5_fragment/1105299v-w-episode-1.1105299v
        player5_url = 'http://www.viki.com/player5_fragment/'+'%s.%s'%(self.video_title,self.video_id)
        try:
            content = self.requestURL(player5_url).read()
            if re.search('(http:\/\/v.viki.io\/.*?)(?=\">)',content):
                return re.search('(http:\/\/v.viki.io\/.*?)(?=\">)',content).group()
            return None
        except Exception as e:
            print e            

    def getTimestamp(self):
        return str(int(time.time()+1))

    def getVideoID(self,url=None):
        """Obtiene el id del video"""
        url_data = urlparse.urlparse(url)
        if url_data.hostname == 'www.viki.com':
            if re.search('([0-9]+v)',url_data.path):
                return re.search('([0-9]+v)',url_data.path).group()

        return None

    def getVideoTitle(self,url=None):
        """Obtiene el titulo del video"""
        url_data = urlparse.urlparse(url)
        if url_data.hostname == 'www.viki.com':
            if re.search('([0-9]+v.*?episode-[0-9]+)',url_data.path):
                return re.search('([0-9]+v.*?episode-[0-9]+)',url_data.path).group()

        return ''        

    def getVikiLanguage(self,lang):
        viki_languages = {"ar":"Arabic","zh":"Chinese(Simple)","zt":"Chinese(Traditional)","en":"English","fr":"French","de":"German","hu":"Hungarian","id":"Indonesian","it":"Italian","ja":"Japanese","ko":"Korean","pl":"Polish","pt":"Portuguese","ro":"Romanian","es":"Spanish","ab":"Abkhazian","aa":"Afar","af":"Afrikaans","ak":"Akan","sq":"Albanian","am":"Amharic","ag":"Anglo-Saxon","ar":"Arabic","an":"Aragonese","hy":"Armenian","ra":"Aromanian","as":"Assamese","at":"Asturian","av":"Avar","ay":"Aymara","az":"Azeri","bal":"Balochi","bm":"Bambara","ba":"Bashkir","eu":"Basque","be":"Belarusian","bn":"Bengali","bho":"Bhojpuri","bh":"Bihari","bi":"Bislama","bs":"Bosnian","br":"Breton","bg":"Bulgarian","my":"Burmese","yue":"Cantonese","ca":"Catalan","ceb":"Cebuano/Binisaya","ch":"Chamorro","ce":"Cherokee","nya":"Chewa/Nyanja","hne":"Chhattisgarhi","zh":"Chinese(Simple)","zt":"Chinese(Traditional)","ctg":"Chittagonian","kw":"Cornish","co":"Corsican","cr":"Cree","hr":"Croatian","cs":"Czech","dcc":"Dakhini","da":"Danish","dv":"Dhivehi","nl":"Dutch","dz":"Dzongkha","en":"English","eo":"Esperanto","et":"Estonian","fo":"Faroese","fj":"Fijian","fi":"Finnish","foi":"Foe","fr":"French","ful":"Fula","gl":"Galician","gan":"Gan","ka":"Georgian","de":"German","el":"Greek","kl":"Greenlandic","gn":"Guarani","gu":"Gujarati","hat":"Haitian Creole","hak":"Hakka","bgc":"Haryanvi","ha":"Hausa","he":"Hebrew","hi":"Hindi","hm":"Hmong","hru":"Hruso","huh":"Huilliche","hu":"Hungarian","is":"Icelandic","io":"Ido","ibo":"Igbo","ilo":"Ilokano","id":"Indonesian","ia":"Interlingua","ie":"Interlingue","iu":"Inuktitut","ik":"Inupiak","ga":"Irish","it":"Italian","ja":"Japanese","jv":"Javanese","xal":"Kalmyk","kn":"Kannada","mu":"Karaoke","ks":"Kashmiri","cb":"Kashubian","kk":"Kazakh","km":"Khmer","kin":"Kinyarwanda","ky":"Kirghiz","rn":"Kirundi","tm":"Klingon","kok":"Konkani","ko":"Korean","ku":"Kurdish","lo":"Lao","la":"Latin","lv":"Latvian","li":"Limburgian","ln":"Lingala","lt":"Lithuanian","jb":"Lojban","nd":"Low Saxon","lb":"Luxembourgish","mk":"Macedonian","mad":"Madurese","mai":"Maithili","mg":"Malagasy","ms":"Malay","ml":"Malayalam","mt":"Maltese","gv":"Manx","mi":"Maori","mr":"Marathi","mh":"Marshallese","mwr":"Marwari","mnp":"Min Bei","cdo":"Min Dong","zm":"Min Nan","mkj":"Mokilese","mo":"Moldovan","mn":"Mongolian","mne":"Montenegrin","mos":"Mossi","nh":"Nahuatl","na":"Nauruan","ne":"Nepali","no":"Norwegian (Bokmål)","nn":"Norwegian (Nynorsk)","oc":"Occitan","or":"Oriya","om":"Oromo","pi":"Pali","ps":"Pashto","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","qu":"Quechua","rm":"Raeto Romance","ro":"Romanian","ru":"Russian","sm":"Samoan","sg":"Sango","sa":"Sanskrit","sat":"Santhali","skr":"Saraiki","sc":"Sardinian","gd":"Scottish Gaelic","sr":"Serbian","sh":"Serbo-Croatian","tn":"Setswana","sn":"Shona","sb":"Sicilian","sd":"Sindhi","si":"Sinhalese","sk":"Slovak","sl":"Slovenian","so":"Somali","st":"Southern Sotho","es":"Spanish","su":"Sundanese","sw":"Swahili","ss":"Swati","sv":"Swedish","syl":"Sylheti","tl":"Tagalog","tg":"Tajik","ta":"Tamil","tt":"Tatar","te":"Telugu","th":"Thai","bo":"Tibetan","ti":"Tigrinya","kim":"Tofa","tp":"Tok Pisin","tq":"Tokipona","to":"Tongan","ts":"Tsonga","tr":"Turkish","tk":"Turkmen","tw":"Twi","udm":"Udmurt","uk":"Ukrainian","ur":"Urdu","ug":"Uyghur","uz":"Uzbek","vi":"Vietnamese","vo":"Volapük","wa":"Walloon","cy":"Welsh","fy":"WestFrisian","wnw":"Winnemem Wintu","wo":"Wolof","xh":"Xhosan","han":"Xiang","yi":"Yiddish","tzx":"Yokoim","yo":"Yoruba","za":"Zhuang","zom":"Zomi","zu":"Zulu","lol":"Lolspeak"}
        return viki_languages[lang]

    def lista(self):
        """Muestra todos los subtítulos disponibles"""
        for key, value in self.languages.iteritems():
            print "%s : %s : %s%%"%(key,self.getVikiLanguage(key),value)

    def requestURL(self, url):
        """Realiza la peticion http"""
        req = urllib2.Request(url)
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        return urllib2.urlopen(req)
    
def main():
    try:
        parser = argparse.ArgumentParser(description="Viki Downloader")
        parser.add_argument("url", help="URL del video en Viki")
        parser.add_argument("-s","--subs",action="store_true", help="Muestra todos los subtitulos disponibles")
        parser.add_argument("-lang",default="es", help="Codigo ISO del idioma")
        parser.add_argument("-v","--video",action="store_true", help="Descarga el video")
        args = parser.parse_args()

        vikidown = Viki(args.url)

        if args.subs:
            print "Subtitulos disponibles:"
            vikidown.lista()

        vikidown.downloadSub(args.lang)

        if args.video:
            vikidown.downloadVideo()
        
    except Exception as e:
        print e            

if __name__ == '__main__':
    #http://www.viki.com/videos/1105299v-w-episode-1
    reload(sys)
    sys.setdefaultencoding("utf-8")
    main()
