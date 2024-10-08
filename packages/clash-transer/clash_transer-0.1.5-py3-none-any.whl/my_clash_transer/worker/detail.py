from .vars import servers_v
from funcy import group_by
from ..log import LOGGER


def group(seq, f):
    _tmp = group_by(f, seq)
    return _tmp[True], _tmp[False]


def get():
    servers = servers_v.get()
    # rules = rules_v.get()
    proxy_names = [server["name"] for server in servers]
    proxy_names.sort()
    LOGGER.info("共 %d 个服务器信息", len(proxy_names))
    HK, remain = group(
        proxy_names,
        lambda name: (
            name.find("香港") > -1 or name.find("HK") > -1 or name.find("HongKong") > -1
        ),
    )
    TW, remain = group(
        remain,
        lambda name: (
            name.find("台湾") > -1 or name.find("TW") > -1 or name.find("Taiwan") > -1
        ),
    )
    SG, remain = group(
        remain,
        lambda name: (
            name.find("新加坡") > -1
            or name.find("SG") > -1
            or name.find("Singapore") > -1
        ),
    )
    RUS_AUS, remain = group(
        remain,
        lambda name: (
            name.find("RUS") > -1
            or name.find("俄") > -1
            or name.find("AUS") > -1
            or name.find("澳大利亚") > -1
            or name.find("Russia") > -1
            or name.find("Australia") > -1
        ),
    )
    US, remain = group(
        remain,
        lambda name: (
            name.find("USA") > -1 or name.find("US") > -1 or name.find("美国") > -1
        ),
    )
    JP, remain = group(
        remain,
        lambda name: (
            name.find("日本") > -1 or name.find("JP") > -1 or name.find("Japan") > -1
        ),
    )
    KR, remain = group(
        remain,
        lambda name: (
            name.find("韩国") > -1
            or name.find("KOR") > -1
            or name.find("KR") > -1
            or name.find("Korea") > -1
        ),
    )
    EU, remain = group(
        remain,
        lambda name: (
            name.find("UK") > -1
            or name.find("GBR") > -1
            or name.find("英国") > -1
            or name.find("DNK") > -1
            or name.find("NLD") > -1
            or name.find("Netherlands") > -1
            or name.find("POL") > -1
            or name.find("西班牙") > -1
            or name.find("ESP") > -1
            or name.find("法国") > -1
            or name.find("FRA") > -1
            or name.find("德国") > -1
            or name.find("DEU") > -1
            or name.find("Germany") > -1
            or name.find("France") > -1
            or name.find("Switzerland") > -1
            or name.find("Sweden") > -1
            or name.find("Austria") > -1
            or name.find("Ireland") > -1
            or name.find("Hungary") > -1
            or name.find("Ireland") > -1
            or name.find("Ireland") > -1
        ),
    )
    remain.extend(RUS_AUS)
    Others = remain
    proxy_groups = [
        {
            "name": "PROXY",
            "type": "select",
            "proxies": [
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "DIRECT",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇯🇵JP-hash",
                "🇯🇵JP-round",
                "🇯🇵JP_S",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
#        {
#            "name": "HOME",
#            "type": "select",
#            "proxies": [
#                "PROXY",
#                "DIRECT",
#                "🇭🇰HK_M",
#                "🇭🇰HK_M_S",
#                "🇭🇰HK",
#                "🇹🇼TW",
#                "🇸🇬SG",
#                "🇸🇬SG_M",
#                "🇸🇬SG_M_S",
#                "🇯🇵JP",
#                "🇰🇷KR",
#                "🇪🇺EU",
#                "🇪🇺EU_S",
#                "👀Others",
#            ],
#        },
        {
            "name": "学术网站",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
            ],
        },
        {
            "name": "🐳DOCKER",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇯🇵JP-hash",
                "🇯🇵JP-round",
                "🇯🇵JP_S",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Apple",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Apple Domestic",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Apple Music",
            "type": "select",
            "proxies": [
                "PROXY",
                "DIRECT",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Apple OutSide",
            "type": "select",
            "proxies": [
                "PROXY",
                "DIRECT",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "BiliBili",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇹🇼TW",
            ],
        },
        {
            "name": "DisneyPlus",
            "type": "select",
            "proxies": [
                "🇹🇼TW",
                "🇹🇼TW_S",
                "🇸🇬SG_S",
                "🇭🇰HK_S",
                "PROXY",
            ],
        },
        # {
        #     "name": "EMBY",
        #     "type": "select",
        #     "proxies": [
        #         "🇸🇬SG_M",
        #         "🇸🇬SG",
        #         "🇸🇬SG_M_S",
        #         "🇭🇰HK_M",
        #         "🇭🇰HK_M_S",
        #         "🇭🇰HK",
        #         "🇪🇺EU",
        #         "🇪🇺EU_S",
        #         "👀Others",
        #         "PROXY",
        #     ],
        # },
        {
            "name": "Google",
            "type": "select",
            "proxies": [
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Google Domestic",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Microsoft",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Microsoft Domestic",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Netflix",
            "type": "select",
            "proxies": [
                "🇹🇼TW",
                "🇹🇼TW_S",
                "🇸🇬SG_S",
                "🇭🇰HK_S",
                "PROXY",
            ],
        },
        {
            "name": "OpenAI",
            "type": "select",
            "proxies": [
                "🇺🇸US_S",
                "🇺🇸US",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Sony",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Steam",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "Telegram",
            "type": "select",
            "proxies": [
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇯🇵JP-hash",
                "🇯🇵JP-round",
                "🇯🇵JP_S",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "YouTube",
            "type": "select",
            "proxies": [
                "🇹🇼TW",
                "🇹🇼TW_S",
                "🇸🇬SG_S",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "PROXY",
            ],
        },
        {
            "name": "直连",
            "type": "select",
            "proxies": [
                "DIRECT",
                "PROXY",
                "🇭🇰HK",
                "🇭🇰HK_S",
                "🇭🇰HK-hash",
                "🇭🇰HK-round",
                "🇹🇼TW",
                "🇸🇬SG",
                "🇸🇬SG_S",
                "🇯🇵JP",
                "🇰🇷KR",
                "🇺🇸US",
                "🇺🇸US_S",
                "🇪🇺EU",
                "🇪🇺EU_S",
                "👀Others",
            ],
        },
        {
            "name": "禁连",
            "type": "select",
            "proxies": ["REJECT", "DIRECT"],
        },
        #    {
        #    "name": "HYMAC",
        #    "type": "select",
        #    "tolerance": 100,
        #    "lazy": False,
        #    "url": 'http://wifi.vivo.com.cn/generate_204',
        #    "interval": 300,
        #    "disable-udp": True,
        #    "proxies": ["HY", "PASS"]
        # },
        {
            "name": "🇭🇰HK",
            "type": "url-test",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 300,
            "strategy": "consistent-hashing",
            "disable-udp": False,
            "proxies": HK,
        },
        {"name": "🇭🇰HK_S", "type": "select", "proxies": HK},
        {
            "name": "🇭🇰HK-hash",
            "type": "load-balance",
            "strategy": "consistent-hashing",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            "proxies": HK,
        },
        {
            "name": "🇭🇰HK-round",
            "type": "load-balance",
            "strategy": "round-robin",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            "proxies": HK,
        },
        {
            "name": "🇹🇼TW",
            "type": "url-test",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 300,
            "disable-udp": False,
            "proxies": TW,
        },
        {"name": "🇹🇼TW_S", "type": "select", "proxies": TW},
        {
            "name": "🇸🇬SG",
            "type": "url-test",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            "proxies": SG,
        },
        {"name": "🇸🇬SG_S", "type": "select", "proxies": SG},
        {
            "name": "🇺🇸US",
            "type": "url-test",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            "proxies": US,
        },
        {"name": "🇺🇸US_S", "type": "select", "proxies": US},
        {
            "name": "🇯🇵JP-hash",
            "type": "load-balance",
            "strategy": "consistent-hashing",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            # "proxies": [name for name in JP if name.find("JPN") > -1],
            "proxies": JP,
        },
        {
            "name": "🇯🇵JP-round",
            "type": "load-balance",
            "strategy": "round-robin",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            # "proxies": [name for name in JP if name.find("JPN") > -1],
            "proxies": JP,
        },
        {"name": "🇯🇵JP_S", "type": "select", "proxies": JP},
        {
            "name": "🇯🇵JP",
            "type": "url-test",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            "proxies": JP,
        },
        {
            "name": "🇰🇷KR",
            "type": "url-test",
            "tolerance": 100,
            "lazy": True,
            "url": "https://i.ytimg.com/generate_204",
            "interval": 900,
            "disable-udp": False,
            "proxies": KR,
        },
        {
            "name": "🇪🇺EU",
            "type": "url-test",
            "tolerance": 100,
            "lazy": True,
            "url": "https://www.google.co.uk/generate_204",
            "interval": 900,
            "disable-udp": True,
            "proxies": EU,
        },
        {"name": "🇪🇺EU_S", "type": "select", "proxies": EU},
        {"name": "👀Others", "type": "select", "proxies": Others},
    ]
    return proxy_groups
