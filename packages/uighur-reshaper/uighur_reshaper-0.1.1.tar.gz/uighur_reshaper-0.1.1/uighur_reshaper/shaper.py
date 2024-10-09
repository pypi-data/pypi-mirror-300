class Syn:
    def __init__(self, code, alone, head, center, rear, link_type):
        # 直接处理 code 为字符串的情况
        self.code = code if isinstance(code, str) else chr(code)
        self.alone = chr(alone)
        self.head = chr(head)
        self.center = chr(center)
        self.rear = chr(rear)
        self.link_type = link_type

class uighur_reshaper:
    LINK_REJECT = 0
    LINK_RIGHT = 1
    LINK_LEFT = 2
    LINK_BOTH = LINK_RIGHT | LINK_LEFT

    def __init__(self):
        self.unicode_map = {}
        self.extend_map = {}

        # Initialize the unicode_map with Syn instances
        self.put(Syn(0x0627, 0xFE8D, 0xFE8D, 0xFE8D, 0xFE8E, self.LINK_RIGHT))
        self.put(Syn(0x06D5, 0xFEE9, 0xFEE9, 0xFEE9, 0xFEEA, self.LINK_RIGHT))
        self.put(Syn(0x0628, 0xFE8F, 0xFE91, 0xFE92, 0xFE90, self.LINK_BOTH))
        self.put(Syn(0x067E, 0xFB56, 0xFB58, 0xFB59, 0xFB57, self.LINK_BOTH))
        self.put(Syn(0x062A, 0xFE95, 0xFE97, 0xFE98, 0xFE96, self.LINK_BOTH))
        self.put(Syn(0x062C, 0xFE9D, 0xFE9F, 0xFEA0, 0xFE9E, self.LINK_BOTH))
        self.put(Syn(0x0686, 0xFB7A, 0xFB7C, 0xFB7D, 0xFB7B, self.LINK_BOTH))
        self.put(Syn(0x062E, 0xFEA5, 0xFEA7, 0xFEA8, 0xFEA6, self.LINK_BOTH))
        self.put(Syn(0x062F, 0xFEA9, 0xFEA9, 0xFEAA, 0xFEAA, self.LINK_RIGHT))
        self.put(Syn(0x0631, 0xFEAD, 0xFEAD, 0xFEAE, 0xFEAE, self.LINK_RIGHT))
        self.put(Syn(0x0632, 0xFEAF, 0xFEAF, 0xFEB0, 0xFEB0, self.LINK_RIGHT))
        self.put(Syn(0x0698, 0xFB8A, 0xFB8A, 0xFB8B, 0xFB8B, self.LINK_RIGHT))
        self.put(Syn(0x0633, 0xFEB1, 0xFEB3, 0xFEB4, 0xFEB2, self.LINK_BOTH))
        self.put(Syn(0x0634, 0xFEB5, 0xFEB7, 0xFEB8, 0xFEB6, self.LINK_BOTH))
        self.put(Syn(0x063A, 0xFECD, 0xFECF, 0xFED0, 0xFECE, self.LINK_BOTH))
        self.put(Syn(0x0641, 0xFED1, 0xFED3, 0xFED4, 0xFED2, self.LINK_BOTH))
        self.put(Syn(0x0642, 0xFED5, 0xFED7, 0xFED8, 0xFED6, self.LINK_BOTH))
        self.put(Syn(0x0643, 0xFED9, 0xFEDB, 0xFEDC, 0xFEDA, self.LINK_BOTH))
        self.put(Syn(0x06AF, 0xFB92, 0xFB94, 0xFB95, 0xFB93, self.LINK_BOTH))
        self.put(Syn(0x06AD, 0xFBD3, 0xFBD5, 0xFBD6, 0xFBD4, self.LINK_BOTH))
        self.put(Syn(0x0644, 0xFEDD, 0xFEDF, 0xFEE0, 0xFEDE, self.LINK_BOTH))
        self.put(Syn(0x0645, 0xFEE1, 0xFEE3, 0xFEE4, 0xFEE2, self.LINK_BOTH))
        self.put(Syn(0x0646, 0xFEE5, 0xFEE7, 0xFEE8, 0xFEE6, self.LINK_BOTH))
        self.put(Syn(0x06BE, 0xFBAA, 0xFBAA, 0xFBAD, 0xFBAD, self.LINK_BOTH))
        self.put(Syn(0x0648, 0xFEED, 0xFEED, 0xFEEE, 0xFEEE, self.LINK_RIGHT))
        self.put(Syn(0x06C7, 0xFBD7, 0xFBD7, 0xFBD8, 0xFBD8, self.LINK_RIGHT))
        self.put(Syn(0x06CB, 0xFBDE, 0xFBDE, 0xFBDF, 0xFBDF, self.LINK_RIGHT))
        self.put(Syn(0x0649, 0xFEEF, 0xFBE8, 0xFBE9, 0xFEF0, self.LINK_BOTH))
        self.put(Syn(0x064A, 0xFEF1, 0xFEF3, 0xFEF4, 0xFEF2, self.LINK_BOTH))
        self.put(Syn(0x0626, 0xFE8B, 0xFE8B, 0xFE8C, 0xFB8C, self.LINK_BOTH))
        self.put(Syn(0x06C6, 0xFBD9, 0xFBD9, 0xFBDA, 0xFBDA, self.LINK_RIGHT))
        self.put(Syn(0x06C8, 0xFBDB, 0xFBDB, 0xFBDC, 0xFBDC, self.LINK_RIGHT))
        self.put(Syn(0x06D0, 0xFBE4, 0xFBE6, 0xFBE7, 0xFBE5, self.LINK_BOTH))
        # self.put(Syn("synLa", 0xFEFB, 0xFEFB, 0xFEFC, 0xFEFC, self.LINK_RIGHT))


        # 特殊 Syn 实例
        self.synA = self.unicode_map.get(chr(0x0627))  # 'ا'
        self.synL = self.unicode_map.get(chr(0x0644))  # 'ل'
        self.synLa = Syn("specialLa", 0xFEFB, 0xFEFB, 0xFEFC, 0xFEFC, self.LINK_RIGHT) # 特殊情况，根据需要调整


        # 填充 extend_map
        for char, syn in self.unicode_map.items():
            self.extend_map[syn.alone] = char
            self.extend_map[syn.head] = char
            self.extend_map[syn.center] = char
            self.extend_map[syn.rear] = char

    def put(self, syn):
        if syn.code != "synLa":
            self.unicode_map[syn.code] = syn

    def basic2extend(self, text):
        sb = []
        prev = None

        for i, c in enumerate(text):
            cur = self.unicode_map.get(c)

            if cur is None:
                sb.append(c)
                prev = None
                continue

            if prev and self.support_link(prev, self.LINK_LEFT) and self.support_link(cur, self.LINK_RIGHT):
                pi = len(sb) - 1
                p_char = sb[pi]

                if p_char == prev.alone:
                    sb[pi] = prev.head
                elif p_char == prev.head:
                    sb[pi] = prev.rear
                elif p_char == prev.rear:
                    sb[pi] = prev.center

                if c == self.synA.code and text[i - 1] == self.synL.code:
                    if p_char in [prev.alone, prev.head]:
                        sb[pi] = self.synLa.alone
                    elif p_char in [prev.center, prev.rear]:
                        sb[pi] = self.synLa.rear
                    continue

                sb.append(cur.rear)
            else:
                sb.append(cur.alone)

            prev = cur

        return ''.join(sb)

    def extend2basic(self, text):
        sb = []

        for c in text:
            if c == self.synLa.alone or c == self.synLa.rear:
                sb.append(self.synL.code)
                sb.append(self.synA.code)
                continue

            converted = self.extend_map.get(c, c)
            sb.append(converted)

        return ''.join(sb)

    def support_link(self, syn, link):
        if syn is None:
            return False
        return (syn.link_type & link) > 0

    # Additional methods if needed
