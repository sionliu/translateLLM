"""
离线词典模块 - 使用 NLTK WordNet 获取词性、例句
使用 NLTK CMUdict 获取音标（覆盖几乎所有英语单词）
"""
import re
from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict

# 加载 CMU 发音词典
try:
    cmu = cmudict.dict()
except Exception:
    cmu = {}

# 词性缩写映射
POS_MAP = {
    'n': 'n.', 'v': 'v.', 'a': 'adj.', 's': 'adj.',
    'r': 'adv.', 'c': 'conj.', 'p': 'prep.', 'pron': 'pron.',
    'num': 'num.', 'int': 'int.'
}

def arpabet_to_ipa(phones):
    """将 ARPAbet 音标转换为 IPA 音标（简化版）"""
    mapping = {
        'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ',
        'AW': 'aʊ', 'AY': 'aɪ', 'EH': 'ɛ', 'ER': 'ɜr',
        'EY': 'eɪ', 'IH': 'ɪ', 'IY': 'i', 'OW': 'oʊ',
        'OY': 'ɔɪ', 'UH': 'ʊ', 'UW': 'u',
        'B': 'b', 'CH': 'tʃ', 'D': 'd', 'DH': 'ð',
        'F': 'f', 'G': 'ɡ', 'HH': 'h', 'JH': 'dʒ',
        'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
        'NG': 'ŋ', 'P': 'p', 'R': 'r', 'S': 's',
        'SH': 'ʃ', 'T': 't', 'TH': 'θ', 'V': 'v',
        'W': 'w', 'Y': 'j', 'Z': 'z', 'ZH': 'ʒ',
    }
    ipa_parts = []
    for phone in phones:
        # 去掉数字后缀（重音标记）
        base = re.sub(r'\d$', '', phone)
        if base in mapping:
            ipa_parts.append(mapping[base])
        else:
            ipa_parts.append(phone.lower())
    return '/' + ''.join(ipa_parts) + '/'

def get_phonetic(word):
    """使用 CMUdict 获取音标"""
    w = word.lower()
    if w in cmu:
        # 取第一个发音
        phones = cmu[w][0]
        return arpabet_to_ipa(phones)
    return ""

def get_pos(word):
    """获取词性"""
    synsets = wn.synsets(word)
    if not synsets:
        return ""
    pos_set = set()
    for syn in synsets:
        pos = syn.pos()
        if pos in POS_MAP:
            pos_set.add(POS_MAP[pos])
    if pos_set:
        return "/".join(sorted(pos_set))
    return ""

def get_example(word):
    """获取例句（从WordNet中提取）
    优先选择包含原单词的例句，确保例句与单词相关
    """
    w = word.lower()
    synsets = wn.synsets(w)
    
    # 第一遍：找包含原单词的例句
    for syn in synsets:
        examples = syn.examples()
        for ex in examples:
            if w in ex.lower():
                return ex
    
    # 第二遍：找第一个有例句的
    for syn in synsets:
        examples = syn.examples()
        if examples:
            return examples[0]
    
    return ""


def lookup_dict(word):
    """
    查询单词的详细信息
    返回: (phonetic, pos, example_en, example_zh)
    """
    w = word.strip().lower()
    if not w:
        return "", "", "", ""

    phonetic = get_phonetic(w)
    pos = get_pos(w)
    example_en = get_example(w)
    example_zh = ""

    return phonetic, pos, example_en, example_zh
