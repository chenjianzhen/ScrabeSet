import requests
from loguru import logger
import re


class BilibiliDownload:
    def __init__(self, header=None, bvid=None, download_with=None):
        if header:
            self.header = header
        else:
            self.header = {
                'referer': 'https://www.bilibili.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            }

        if bvid:
            bv_pattern = r'(BV|AV)[a-zA-Z0-9]{10}'
            match = re.search(bv_pattern, bvid)
            if match:
                self.bvid = match.group(0)
                logger.success("匹配到的AV|BV号为:%s" % self.bvid)
            else:
                logger.error("未能匹配到AV|BV号")
            logger.info("视频id:%s" % self.bvid)
        else:
            logger.error("bvid must be valid!")
            raise TypeError("bvid must be valid!")

        if download_with:
            self.download_with = download_with

        self.cid = None

    def get_cid(self):
        if self.bvid.startswith("AV"):
            cid_url = 'https://api.bilibili.com/x/player/pagelist?avid=%s' % self.bvid
        else:
            cid_url = 'https://api.bilibili.com/x/player/pagelist?bvid=%s' % self.bvid
        response = requests.get(url=cid_url, headers=self.header)
        self.cid = response.json()['data'][0]['cid']

    def get_video_url(self):
        if not self.cid:
            self.get_cid()

        if self.bvid.startswith("AV"):
            video_url = 'https://api.bilibili.com/x/player/playurl?avid=%s&cid=%s&qn=16&type=mp4&platform=html5' % (
            self.bvid, self.cid)
        else:
            video_url = 'https://api.bilibili.com/x/player/playurl?bvid=%s&cid=%s&qn=16&type=mp4&platform=html5' % (
                self.bvid, self.cid)
        response = requests.get(url=video_url, headers=self.header)
        logger.info(response.json())

    def get_video_msg(self):
        if self.bvid.startswith("AV"):
            video_msg = 'https://api.bilibili.com/x/web-interface/view?avid=%s&cid=%s' % (self.bvid, self.cid)
        else:
            video_msg = 'https://api.bilibili.com/x/web-interface/view?bvid=%s&cid=%s' % (self.bvid, self.cid)
        response = requests.get(url=video_msg, headers=self.header)
        logger.info(response.json())

    def download(self):
        if not self.download_with:
            self.__download_default()
        else:
            self.__download_with_aria2c()

    def __download_default(self):
        pass

    def __download_with_aria2c(self):
        pass

    def __str__(self):
        if self.bvid:
            return "视频ID:%s" % self.bvid
        else:
            return "还未获得视频ID"


if __name__ == "__main__":
    download = BilibiliDownload(bvid="https://www.bilibili.com/video/BV1rT411m7ug?p=5&spm_id_from=pageDriver&vd_source=1bfe10eb480a3b3197328425fc4c53b9")
    download.get_video_url()
    logger.info(download)
