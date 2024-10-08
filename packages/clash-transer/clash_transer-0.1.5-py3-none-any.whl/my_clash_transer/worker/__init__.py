from ..downloader import Downloader, DownloadRequest, DownloadText
from ..config import CONFIG
from ..log import LOGGER
from ..parse import Parse
from typing import Iterable
import datetime
import re
from .vars import servers_v, rules_v
from yaml import dump
from .detail import get as get_proxy_groups


class Worker:
    def __init__(self) -> None:
        self.configs = CONFIG.configs

    def download(self) -> Iterable[DownloadText]:
        downloader = Downloader(default_store_path=self.configs["store_path"])
        d = [i for i in CONFIG.configs["subscriptions"]]
        s = [
            DownloadRequest(i["url"], i["dist"], datetime.timedelta(i["expire"]))
            for i in d
        ]
        download_resps: Iterable[DownloadText] = downloader.downloads(s)
        return download_resps

    def parse(self, download_resps):
        servers = []
        rules = []
        for resp in download_resps:
            suffix = resp.dist.suffix.strip(".")
            if suffix.lower() == "list":
                for i in Parse.parse(resp.text, suffix).res:
                    rules.append(i)
            else:
                for i in Parse.parse(resp.text, suffix).res:
                    i["name"] = i["name"].replace(" ", "")
                    servers.append(i)

        store_map = {
            "DST-PORT": 10,
            "SRC-IP-CIDR": 20,
            "IP-CIDR": 30,
            "DOMAIN": 40,
            "DOMAIN-KEYWORD": 60,
            "DOMAIN-SUFFIX": 50,
        }
        rules = sorted(rules, key=lambda x: store_map[x[0]])
        exclude_server_regex = re.compile(
            r"|".join(
                [re.escape(keyword) for keyword in self.configs["servers"]["exclude"]]
            )
        )
        # LOGGER.debug(servers)
        servers = [
            server
            for server in servers
            if not re.findall(exclude_server_regex, server["name"])
        ]
        return servers, rules

    def check(self, proxy_group, rules):
        action_set = set()
        group_set = set()
        for _, _, action in rules[:-1]:
            action_set.add(action)
        for group in proxy_group:
            group_set.add(group["name"])
        action_set.remove("DIRECT")
        diffs = action_set.difference(group_set)
        if diffs:
            LOGGER.error("这些转发组没有设置：%s", ",".join(list(diffs)))
            raise TypeError()

    def combine(self):
        res = {
            "port": 10809,
            "authentication": [],
            "allow-lan": True,
            "mode": "Rule",
            "log-level": "error",
            "experimental": {"ignore-resolve-fail": True},
            "ipv6": False,
            # 'routing-mark': 255,
            "proxies": self.server,
            "proxy-groups": self.proxy_groups,
            "rules": self.rules,
            "dns": {
                "default-nameserver": ["120.53.53.101"],
                "enable": True,
                "enhanced-mode": "fake-ip",
                "ipv6": False,
                "listen": "0.0.0.0:7874",
                "nameserver": ["tls://dot-91b555fc.dot.pub", "tls://106895.alidns.com"],
                "fake-ip-range": "198.18.0.1/16",
                "fake-ip-filter": [
                    "*.alidns.com",
                    "*.dot.pub",
                    "+.anyunb.top",
                    "*.lan",
                    "*.localdomain",
                    "*.example",
                    "*.invalid",
                    "*.localhost",
                    "*.test",
                    "*.local",
                    "*.home.arpa",
                    "time.*.com",
                    "time.*.gov",
                    "time.*.edu.cn",
                    "time.*.apple.com",
                    "time-ios.apple.com",
                    "time1.*.com",
                    "time2.*.com",
                    "time3.*.com",
                    "time4.*.com",
                    "time5.*.com",
                    "time6.*.com",
                    "time7.*.com",
                    "ntp.*.com",
                    "ntp1.*.com",
                    "ntp2.*.com",
                    "ntp3.*.com",
                    "ntp4.*.com",
                    "ntp5.*.com",
                    "ntp6.*.com",
                    "ntp7.*.com",
                    "ntp.aliyun.com",
                    "*.time.edu.cn",
                    "*.ntp.org.cn",
                    "+.pool.ntp.org",
                    "time1.cloud.tencent.com",
                    "music.163.com",
                    "*.music.163.com",
                    "*.126.net",
                    "musicapi.taihe.com",
                    "music.taihe.com",
                    "songsearch.kugou.com",
                    "trackercdn.kugou.com",
                    "*.kuwo.cn",
                    "api-jooxtt.sanook.com",
                    "api.joox.com",
                    "joox.com",
                    "y.qq.com",
                    "*.y.qq.com",
                    "streamoc.music.tc.qq.com",
                    "mobileoc.music.tc.qq.com",
                    "isure.stream.qqmusic.qq.com",
                    "dl.stream.qqmusic.qq.com",
                    "aqqmusic.tc.qq.com",
                    "amobile.music.tc.qq.com",
                    "*.xiami.com",
                    "*.music.migu.cn",
                    "music.migu.cn",
                    "+.msftconnecttest.com",
                    "+.msftncsi.com",
                    "msftconnecttest.com",
                    "msftncsi.com",
                    "localhost.ptlogin2.qq.com",
                    "localhost.sec.qq.com",
                    "+.srv.nintendo.net",
                    "*.n.n.srv.nintendo.net",
                    "+.stun.playstation.net",
                    "xbox.*.*.microsoft.com",
                    "*.*.xboxlive.com",
                    "xbox.*.microsoft.com",
                    "xnotify.xboxlive.com",
                    "+.battlenet.com.cn",
                    "+.wotgame.cn",
                    "+.wggames.cn",
                    "+.wowsgame.cn",
                    "+.wargaming.net",
                    "proxy.golang.org",
                    "stun.*.*",
                    "stun.*.*.*",
                    "+.stun.*.*",
                    "+.stun.*.*.*",
                    "+.stun.*.*.*.*",
                    "+.stun.*.*.*.*.*",
                    "heartbeat.belkin.com",
                    "*.linksys.com",
                    "*.linksyssmartwifi.com",
                    "*.router.asus.com",
                    "mesu.apple.com",
                    "swscan.apple.com",
                    "swquery.apple.com",
                    "swdownload.apple.com",
                    "swcdn.apple.com",
                    "swdist.apple.com",
                    "lens.l.google.com",
                    "stun.l.google.com",
                    "+.nflxvideo.net",
                    "*.square-enix.com",
                    "*.finalfantasyxiv.com",
                    "*.ffxiv.com",
                    "*.ff14.sdo.com",
                    "ff.dorado.sdo.com",
                    "*.mcdn.bilivideo.cn",
                    "+.media.dssott.com",
                    "shark007.net",
                    "+.cmbchina.com",
                    "+.cmbimg.com",
                    "local.adguard.org",
                    "+.dns.google",
                ],
            },
            "ebpf": {"redirect-to-tun": ["eth0"]},
        }
        return res
        # cellphone_rule = {
        #     "name": "ssid-group",
        #     "type": "select",
        #     "proxies": ["PROXY", "DIRECT"],
        #     "ssid-policy": {
        #         "ChinaNet-Tn9y_5G": "DIRECT",
        #         "aaaTop1_5G": "DIRECT",
        #         "a13101_5G": "DIRECT",
        #         "cellular": "PROXY",
        #         "default": "PROXY",
        #     },
        # }
        # res["proxy-groups"].append(cellphone_rule)
        # return yaml.dump(res, allow_unicode=True)

    def do(self):
        download_resps = self.download()
        servers, rules = self.parse(download_resps)
        servers_v.set(servers)
        rules_v.set(rules)

        self.proxy_groups = get_proxy_groups()
        self.server = servers
        _rules = (
            [i.split(",") for i in self.configs["rules"]["add_before"]]
            + rules
            + [i.split(",") for i in self.configs["rules"]["add_last"]]
        )
        self.check(self.proxy_groups, _rules)
        self.rules = [",".join(rule) for rule in _rules]
        res = self.combine()
        with open(self.configs.get("dist_file"), "w") as f:
            dump(res, f, allow_unicode=True)
