import zipfile
from io import BytesIO, TextIOWrapper
from typing import Any, TextIO, Iterable, Optional
from xml.etree.ElementTree import Element, ElementTree
from feasytools import TimeFunc, SegFunc, ConstFunc, makeFunc, FloatLike
from gurobipy import Model, GRB, quicksum, Var, Constr

FloatVar = Optional[float]
Qs = quicksum


def _float2func(v: FloatLike) -> TimeFunc:
    if isinstance(v, (float, int)):
        return ConstFunc(v)
    else:
        assert isinstance(v, TimeFunc)
        return v


def _tfv(s: FloatVar): return "<unsolved>" if s is None else str(s)

def _readVal(s: str) -> 'tuple[float, str]':
    if s.endswith("pu"):
        return float(s[:-2]), "pu"
    elif s.endswith("kVA"):
        return float(s[:-3]), "kVA"
    elif s.endswith("kvar"):
        return float(s[:-4]), "kvar"
    elif s.endswith("kW"):
        return float(s[:-2]), "kW"
    elif s.endswith("MVA"):
        return float(s[:-3]), "MVA"
    elif s.endswith("Mvar"):
        return float(s[:-4]), "Mvar"
    elif s.endswith("MW"):
        return float(s[:-2]), "MW"
    elif s.endswith("kV"):
        return float(s[:-2]), "kV"
    elif s.endswith("V"):
        return float(s[:-1]), "V"
    elif s.endswith("kA"):
        return float(s[:-2]), "kA"
    elif s.endswith("ohm"):
        return float(s[:-3]), "ohm"
    elif s.endswith("kWh"):
        return float(s[:-3]), "kWh"
    else:
        return float(s), ""

def _readPriceLike(e: Element, sb_mva:float) -> FloatLike:
    def _valconv(v:FloatLike, u:str) -> FloatLike:
        if u == "$/puh" or u == "$/puh2" or u == "$":
            return v
        elif u == "$/kWh":
            return v * (sb_mva * 1000)
        elif u == "$/MWh":
            return v * sb_mva
        elif u == "$/kWh2":
            return v * (sb_mva * 1000 * sb_mva * 1000)
        elif u == "$/MWh2":
            return v * (sb_mva * sb_mva)
        else:
            return v
    if "const" in e.attrib:
        v, u = _readVal(e.attrib["const"])
        if u == "": u = e.attrib.get("unit","$")
        return _valconv(v, u)
    else:
        repeat = int(e.attrib.get("repeat", "1"))
        period = int(e.attrib.get("period", "0"))
        sf = SegFunc()
        for itm in e:
            time = int(itm.attrib["time"])
            v, u = _readVal(itm.attrib["value"])
            sf.add(time, _valconv(v, u))
        return sf.repeat(repeat, period)

def _readFloatLike(e: Element, sb_mva:float, ub_kv:float) -> FloatLike:
    def _valconv(v:FloatLike, u:str) -> FloatLike:
        if u == "pu":
            return v
        elif u == "kVA":
            return v / (sb_mva * 1000)
        elif u == "kvar":
            return v / (sb_mva * 1000)
        elif u == "kW":
            return v / (sb_mva * 1000)
        elif u == "MVA":
            return v / sb_mva
        elif u == "Mvar":
            return v / sb_mva
        elif u == "MW":
            return v / sb_mva
        elif u == "kV":
            return v / ub_kv
        elif u == "V":
            return v / (ub_kv * 1000)
        elif u == "kA":
            return v / (sb_mva / (ub_kv * 3 ** 0.5))
        elif u == "ohm":
            return v * ub_kv ** 2 / sb_mva
        else:
            return v
    if "const" in e.attrib:
        v, u = _readVal(e.attrib["const"])
        return _valconv(v, u)
    else:
        repeat = int(e.attrib.get("repeat", "1"))
        period = int(e.attrib.get("period", "0"))
        sf = SegFunc()
        for itm in e:
            time = int(itm.attrib["time"])
            v, u = _readVal(itm.attrib["value"])
            sf.add(time, _valconv(v, u))
        return sf.repeat(repeat, period)


class Bus:
    """母线 Bus"""
    ID: str
    V: FloatVar  # pu
    Pd: TimeFunc  # pu
    Qd: TimeFunc  # pu
    ShadowPrice: FloatVar  # 该母线上的发电机的影子价格，元/pu power

    def __init__(self, id: str, p_pu: FloatLike, q_pu: FloatLike, lat: Optional[float] = None, lon: Optional[float] = None):
        self.ID = id
        self.V = None
        self.Pd = _float2func(p_pu)
        self.Qd = _float2func(q_pu)
        self.ShadowPrice = None
        self.Lat = lat
        self.Lon = lon

    def __repr__(self):
        return f"Bus[ID={self.ID}, V={_tfv(self.V)}, Pd={self.Pd}, Qd={self.Qd}, Lat={self.Lat}, Lon={self.Lon}]"

    def __str__(self):
        return repr(self)
    
    def str_t(self, _t: int):
        return f"Bus[ID={self.ID}, V={_tfv(self.V)}, Pd={self.Pd(_t)}, Qd={self.Qd(_t)}, Lat={self.Lat}, Lon={self.Lon}]"

    @staticmethod
    def fromXML(node: 'Element', Sb_MVA: float, Ub_kV: float):
        id = node.attrib["ID"]
        p = _readFloatLike(node.find("Pd"), Sb_MVA, Ub_kV)
        q = _readFloatLike(node.find("Qd"), Sb_MVA, Ub_kV)
        lat = node.attrib.get("Lat", None)
        lon = node.attrib.get("Lon", None)
        return Bus(id, p, q, lat, lon)
    
    @staticmethod
    def load(fp: TextIO, Sb: float = 1.0, loop: str = "0,0"):
        ret = loop.split(",")
        assert len(ret) == 2
        loop_period = int(ret[0])
        loop_times = int(ret[1])
        data = fp.readlines()
        hl = data[0].split(',')
        if hl[0].strip() != "time": raise ValueError("Bad format of bus CSV file")
        tl = [int(x.strip()) for x in hl[1:]]
        if loop_period > 0 and loop_times > 0:
            tl_old = tl.copy()
            for i in range(loop_times - 1):
                tl.extend([x + loop_period * (i + 1) for x in tl_old])
        else:
            tl_old = tl

        def parseline(ln: str,i:int):
            ret = ln.split(',')
            if len(ret) != len(tl_old) + 1: raise ValueError(f"Bad line length at line {i} in bus CSV file")
            p: 'list[float]' = []
            q: 'list[float]' = []
            for x in ret[1:]:
                p0, q0 = x.strip().split('|')
                p.append(float(p0) / Sb)
                q.append(float(q0) / Sb)
            if loop_period > 0 and loop_times > 0:
                p = p * loop_times
                q = q * loop_times
            bn = ret[0].strip().split('|')
            if len(bn) == 1:
                return bn[0], makeFunc(tl, p), makeFunc(tl, q)
            elif len(bn) == 3:
                return bn[0], makeFunc(tl, p), makeFunc(tl, q), float(bn[1]), float(bn[2])
            else:
                raise ValueError(f"Bad bus name format at line {i} in bus CSV file, should be 'name' or 'name|lat|lon'")

        return [Bus(*parseline(ln,i)) for i,ln in enumerate(data[1:],start=1)]


class Line:
    """线路"""
    ID: str
    fBus: str
    tBus: str
    R: float  # pu
    X: float  # pu
    P: FloatVar  # pu
    Q: FloatVar  # pu
    I: FloatVar  # pu

    def __init__(self, id: str, fbus: str, tbus: str, r_pu: float, x_pu: float):
        '''
        初始化
            id: 线路ID
            fbus: 起始母线ID
            tbus: 终止母线ID
            r_pu: 电阻, pu
            x_pu: 电抗, pu
        '''
        self.ID = id
        self.fBus = fbus
        self.tBus = tbus
        self.R = r_pu
        self.X = x_pu
        self.I = None
        self.P = None
        self.Q = None

    @property
    def pair(self):
        '''(self.fBus, self.tBus)的语法糖'''
        return (self.fBus, self.tBus)

    def __repr__(self) -> str:
        return f"Line[ID={self.ID}, fBus={self.fBus}, tBus={self.tBus}, R={self.R}, X={self.X}, I={_tfv(self.I)}, P={_tfv(self.P)}, Q={_tfv(self.Q)}]"

    def __str__(self) -> str:
        return repr(self)
    
    def str_t(self, _t: int) -> str:
        return self.__str__()

    @staticmethod
    def load(fp: TextIO, Zb: float = 1.0):
        data = fp.readlines()
        head = [x.strip() for x in data[0].split(',')]
        if head != ["id", "fBus", "tBus", "R", "X"]:
            raise ValueError("线路CSV文件格式错误: 列必须为id,fBus,tBus,R,X, 且区分大小写")

        def parseline(ln: str):
            (id, f, t, r, x) = (x.strip() for x in ln.split(','))
            return id, f, t, float(r) / Zb, float(x) / Zb

        return [Line(*parseline(ln)) for ln in data[1:]]

    @staticmethod
    def fromXML(node: 'Element', Zb_Ohm: float):
        id = node.attrib["ID"]
        f = node.attrib["From"]
        t = node.attrib["To"]
        r = float(node.attrib["R"]) / Zb_Ohm
        x = float(node.attrib["X"]) / Zb_Ohm
        return Line(id, f, t, r, x)

class Generator:
    '''发电机(火电/风电/光伏通用型)'''
    ID: str
    BusID: str
    Pmin: TimeFunc  #pu
    Pmax: TimeFunc  #pu
    P: FloatVar  #pu
    Qmin: TimeFunc  #pu
    Qmax: TimeFunc  #pu
    Q: FloatVar  #pu
    CostA: TimeFunc  #二次成本：元/(pu Power·h)**2
    CostB: TimeFunc  #线性成本：元/pu Power·h
    CostC: TimeFunc  #开机固定成本：元

    def __init__(self, id: str, busid: str, pmin_pu: FloatLike, pmax_pu: FloatLike,
                 qmin_pu: FloatLike, qmax_pu: FloatLike, costA: FloatLike, costB: FloatLike, costC: FloatLike):
        '''
        初始化
            id: 发电机ID
            busid: 发电机所在母线ID
            pmin_pu: 最小有功出力, pu
            pmax_pu: 最大有功出力, pu
            qmin_pu: 最小无功出力, pu
            qmax_pu: 最大无功出力, pu
            costA: 二次成本系数, 元/(pu Power·h)**2
            costB: 线性成本系数, 元/pu Power·h
            costC: 开机固定成本, 元
        '''
        self.ID = id
        self.BusID = busid
        self.P = None
        self.Q = None
        self.Pmin = _float2func(pmin_pu)
        self.Pmax = _float2func(pmax_pu)
        self.Qmin = _float2func(qmin_pu)
        self.Qmax = _float2func(qmax_pu)
        self.CostA = _float2func(costA)
        self.CostB = _float2func(costB)
        self.CostC = _float2func(costC)
        self.CostShadow = None

    def __repr__(self) -> str:
        return f"Generator[ID={self.ID}, Bus={self.BusID}, P={_tfv(self.P)}, Q={_tfv(self.Q)}, Pmin={self.Pmin}, Pmax={self.Pmax}, Qmin={self.Qmin}, Qmax={self.Qmax}, CostA={self.CostA}, CostB={self.CostB}, CostC={self.CostC}]"

    def __str__(self) -> str:
        return repr(self)

    def str_t(self, _t: int) -> str:
        return f"Generator[ID={self.ID}, Bus={self.BusID}, P={_tfv(self.P)}, Q={_tfv(self.Q)}, Pmin={self.Pmin(_t)}, Pmax={self.Pmax(_t)}, Qmin={self.Qmin(_t)}, Qmax={self.Qmax(_t)}, CostA={self.CostA(_t)}, CostB={self.CostB(_t)}, CostC={self.CostC(_t)}]"

    def Cost(self, _t: int, secondary: bool = True) -> FloatVar:
        '''
        获取当前发电功率下的发电成本, 元/h
            _t: 时间
            secondary: True表示使用二次函数成本模型, False表示使用一次函数成本模型
        '''
        if self.P is None: return None
        ret = self.CostB(_t) * self.P + self.CostC(_t)
        if secondary: ret += self.CostA(_t) * self.P ** 2
        return ret

    def CostPerPUPower(self, _t: int, secondary: bool = True) -> FloatVar:
        '''
        获取当前发电功率下的单位发电成本, 元/pu·h
            _t: 时间
            secondary: True表示使用二次函数成本模型, False表示使用一次函数成本模型
        '''
        if self.P is None or self.P == 0: return None
        ret = self.CostB(_t) * self.P + self.CostC(_t)
        if secondary: ret += self.CostA(_t) * self.P ** 2
        return ret / self.P

    @staticmethod
    def load(fp: TextIO, SbkW: float, Sb: float = 1.0):
        '''
        从文件中加载发电机数据
            fp: 文件指针
            SbkW: 基准功率, kW, 用于电价单位转换: 元/kWh->元/pu Power·h
            Sb: 基准功率, 单位不确定(取决于info.txt), 要求文件中的功率除以Sb后为标幺值
        '''
        data = fp.readlines()
        hl = data[0].split(',')
        if hl[0].strip() != "time": raise ValueError("发电机CSV文件格式错误")
        tl = [int(x.strip()) for x in hl[1:]]

        def parseline(ln: str):
            ret = ln.split(',')
            if len(ret) != len(tl) + 1: raise ValueError("发电机CSV文件行长度错误")
            pmin: 'list[float]' = []
            qmin: 'list[float]' = []
            pmax: 'list[float]' = []
            qmax: 'list[float]' = []
            for x in ret[1:]:
                pmin0, pmax0, qmin0, qmax0 = x.strip().split('|')
                pmin.append(float(pmin0) / Sb)
                pmax.append(float(pmax0) / Sb)
                qmin.append(float(qmin0) / Sb)
                qmax.append(float(qmax0) / Sb)
            (id, busid, ca, cb, cc) = (x.strip() for x in ret[0].strip().split("|"))
            #ca:元/(kWh)**2；cb:元/kWh；cc:元
            return (id, busid, makeFunc(tl, pmin), makeFunc(tl, pmax),
                    makeFunc(tl, qmin), makeFunc(tl, qmax), float(ca) * SbkW * SbkW, float(cb) * SbkW, float(cc))

        return [Generator(*parseline(ln)) for ln in data[1:]]

    @staticmethod
    def fromXML(node: 'Element', Sb_MVA: float, Ub_kV: float):
        id = node.attrib["ID"]
        busid = node.attrib["Bus"]
        pmin = _readFloatLike(node.find("Pmin"), Sb_MVA, Ub_kV)
        pmax = _readFloatLike(node.find("Pmax"), Sb_MVA, Ub_kV)
        qmin = _readFloatLike(node.find("Qmin"), Sb_MVA, Ub_kV)
        qmax = _readFloatLike(node.find("Qmax"), Sb_MVA, Ub_kV)
        ca = _readPriceLike(node.find("CostA"), Sb_MVA)
        cb = _readPriceLike(node.find("CostB"), Sb_MVA)
        cc = _readPriceLike(node.find("CostC"), Sb_MVA)
        return Generator(id, busid, pmin, pmax, qmin, qmax, ca, cb, cc)


BusID = str
LineID = str


class Grid:
    Sb: float  #MVA
    Ub: float  #kV

    @property
    def Sb_MVA(self) -> float:
        return self.Sb

    @property
    def Sb_kVA(self) -> float:
        return self.Sb * 1000

    @property
    def Zb(self) -> float:
        '''Zb, unit = Ohm'''
        return self.Ub ** 2 / self.Sb

    @property
    def Ib(self) -> float:
        '''Ib, unit = kA'''
        return self.Sb / (self.Ub * (3 ** 0.5))

    def __init__(self, Sb_MVA: float, Ub_kV: float, buses: 'Iterable[Bus]',
                 lines: 'Iterable[Line]', gens: 'Iterable[Generator]', holdShadowPrice: bool = False):
        '''
        初始化
            Sb_MVA: 基准功率, MVA
            Ub_kV: 基准电压, kV
            buses: 母线列表
            lines: 线路列表
            gens: 发电机列表
            holdShadowPrice: 当本次影子价格求解失败时，是否保留上次影子价格
        '''
        self.Sb = Sb_MVA
        self.Ub = Ub_kV
        self._buses = {bus.ID: bus for bus in buses}
        self._lines = {line.ID: line for line in lines}
        self._ladjfb: 'dict[str, list[Line]]' = {bus.ID: [] for bus in buses}
        self._ladjtb: 'dict[str, list[Line]]' = {bus.ID: [] for bus in buses}
        self._bnames = list(self._buses.keys())
        self._gens = {gen.ID: gen for gen in gens}
        self._gatb: 'dict[str, list[Generator]]' = {bus.ID: [] for bus in buses}
        for line in self._lines.values():
            if not line.fBus in self._bnames: raise ValueError(f"母线{line.fBus}未定义")
            if not line.tBus in self._bnames: raise ValueError(f"母线{line.tBus}未定义")
            self._ladjfb[line.fBus].append(line)
            self._ladjtb[line.tBus].append(line)
        for gen in self._gens.values():
            assert gen.BusID in self._bnames
            self._gatb[gen.BusID].append(gen)
        self.__holdShadowPrice = holdShadowPrice

    def AddGen(self, g: Generator):
        self._gens[g.ID] = g
        self._gatb[g.BusID].append(g)

    @property
    def BusNames(self) -> 'list[str]':
        return self._bnames

    def Bus(self, id: str) -> 'Bus':
        return self._buses[id]

    @property
    def Buses(self):
        return self._buses.values()

    def LinesOfFBus(self, busid: str) -> 'list[Line]':
        return self._ladjfb[busid]

    def LinesOfTBus(self, busid: str) -> 'list[Line]':
        return self._ladjtb[busid]

    def Line(self, id: str) -> 'Line':
        return self._lines[id]

    @property
    def Lines(self):
        return self._lines.values()

    def Gen(self, id: str) -> 'Generator':
        return self._gens[id]

    @property
    def GenNames(self) -> 'list[str]':
        return list(self._gens.keys())

    @property
    def Gens(self):
        return self._gens.values()

    def GensAtBus(self, busid: str) -> 'list[Generator]':
        return self._gatb[busid]

    def __repr__(self):
        b = '\n  '.join(map(str, self._buses.values()))
        l = '\n  '.join(map(str, self._lines.values()))
        g = '\n  '.join(map(str, self._gens.values()))
        return f"Buses:\n  {b}\nLines:\n  {l}\nGenerators:\n  {g}"

    def __str__(self):
        return repr(self)
    
    def str_t(self, _t: int):
        b = '\n  '.join(v.str_t(_t) for v in self._buses.values())
        l = '\n  '.join(v.str_t(_t) for v in self._lines.values())
        g = '\n  '.join(v.str_t(_t) for v in self._gens.values())
        return f"At time {_t}:\nBuses:\n  {b}\nLines:\n  {l}\nGenerators:\n  {g}"

    @staticmethod
    def fromFile(file_name:str, holdShadowPrice: bool = False):
        if file_name.lower().endswith(".zip"):
            return Grid.fromFileZIP(file_name, holdShadowPrice)
        elif file_name.lower().endswith(".xml"):
            return Grid.fromFileXML(file_name)
        else:
            raise ValueError("不支持的文件类型")
        
    @staticmethod
    def fromFileXML(xml_name: str, holdShadowPrice: bool = False):
        rt = ElementTree(file=xml_name).getroot()
        Sb, unit = _readVal(rt.attrib["Sb"])
        if unit == "MVA": pass
        elif unit == "kVA": Sb /= 1000
        else: raise ValueError(f"无效的基准功率单位{unit}")
        Ub, unit = _readVal(rt.attrib["Ub"])
        if unit == "kV": pass
        else: raise ValueError(f"无效的基准电压单位{unit}")
        buses = []
        lines = []
        gens = []
        for e in rt:
            if e.tag == "bus":
                buses.append(Bus.fromXML(e, Sb, Ub))
            elif e.tag == "line":
                lines.append(Line.fromXML(e, Ub * Ub / Sb))
            elif e.tag == "gen" or e.tag == "generator":
                gens.append(Generator.fromXML(e, Sb, Ub))
            else:
                raise ValueError(f"未知的XML节点{e.tag}")
        return Grid(Sb, Ub, buses, lines, gens, holdShadowPrice)

    @staticmethod
    def fromFileZIP(zip_name: str, holdShadowPrice: bool = False):
        zf = zipfile.ZipFile(zip_name, "r")
        with TextIOWrapper(BytesIO(zf.read("info.txt"))) as fp:
            info: dict[str, Any] = {}
            for item in [x.split(':') for x in fp.readlines()]:
                if len(item) != 2: raise ValueError("电网信息文件错误")
                info[item[0].strip()] = item[1].strip()
        Sb = float(info.pop("S_base_MVA"))
        Ub = float(info.pop("U_base_kV"))
        Zb = Ub * Ub / Sb
        with TextIOWrapper(BytesIO(zf.read("buses.csv"))) as fp:
            buses_unit = info.pop("buses_unit")
            buses_loop = info.pop("buses_loop", "0,0")
            if buses_unit == "pu":
                buses = Bus.load(fp, 1, buses_loop)
            elif buses_unit in ["kVA", "kvar", "kW"]:
                buses = Bus.load(fp, Sb * 1000, buses_loop)
            elif buses_unit in ["MVA", "Mvar", "MW"]:
                buses = Bus.load(fp, Sb, buses_loop)
            else:
                raise ValueError(f"无效的功率单位{buses_unit}")
        with TextIOWrapper(BytesIO(zf.read("lines.csv"))) as fp:
            lines_unit = info.pop("lines_unit")
            if lines_unit == "pu":
                lines = Line.load(fp)
            elif lines_unit == "ohm":
                lines = Line.load(fp, Zb)
            else:
                raise ValueError(f"无效的线路阻抗单位{lines_unit}")
        with TextIOWrapper(BytesIO(zf.read("gens.csv"))) as fp:
            gens_unit = info.pop("gens_unit")
            if gens_unit == "pu":
                gens = Generator.load(fp, Sb * 1000)
            elif gens_unit in ["kVA", "kvar", "kW"]:
                gens = Generator.load(fp, Sb * 1000, Sb * 1000)
            elif gens_unit in ["MVA", "Mvar", "MW"]:
                gens = Generator.load(fp, Sb * 1000, Sb)
            else:
                raise ValueError(f"无效的功率单位{gens_unit}")
        return Grid(Sb, Ub, buses, lines, gens, holdShadowPrice)

    def solve(self, _t: int, /, *, max_v_pu:float = 1.1, min_v_pu: float = 0.9, max_I_kA: float = 0.866) -> 'tuple[bool, float]':
        '''求解_t时刻的最优解, 返回(是否求解成功, 目标函数最优值)'''
        model = Model("model")
        max_v = max_v_pu ** 2
        min_v = min_v_pu ** 2
        max_l = (max_I_kA / self.Ib) ** 2  # 中国10kV配网限制功率15MVA，对应电流0.866kA
        # ---------------添加变量---------------
        # pg0[k]: 发电机有功
        # qg0[k]: 发电机无功
        # --> pg[j]: 节点所有发电机的有功
        # --> qg[j]: 节点所有发电机的无功
        # v[j]: 节点电压平方
        # l[i,j]: 线路电流平方
        # P[i,j] 线路有功
        # Q[i,j]: 线路无功
        pg0: dict[str, Var] = {g.ID: model.addVar(name=f"pg_{g.ID}", vtype='C', lb=g.Pmin(_t), ub=g.Pmax(_t)) for g in
                               self.Gens}
        qg0: dict[str, Var] = {g.ID: model.addVar(name=f"qg_{g.ID}", vtype='C', lb=g.Qmin(_t), ub=g.Qmax(_t)) for g in
                               self.Gens}
        pg: dict[str, list[Var]] = {bus.ID: [] for bus in self.Buses}
        qg: dict[str, list[Var]] = {bus.ID: [] for bus in self.Buses}
        for g in self.Gens:
            pg[g.BusID].append(pg0[g.ID])
            qg[g.BusID].append(qg0[g.ID])

        v = {bus.ID: model.addVar(name=f"v_{bus.ID}", vtype='C', lb=min_v, ub=max_v) for bus in self.Buses}
        l = {line.ID: model.addVar(name=f"l_{line.ID}", vtype='C', lb=0, ub=max_l) for line in self.Lines}
        P = {line.ID: model.addVar(name=f"P_{line.ID}", vtype='C', lb=-GRB.INFINITY, ub=GRB.INFINITY) for line in
             self.Lines}
        Q = {line.ID: model.addVar(name=f"Q_{line.ID}", vtype='C', lb=-GRB.INFINITY, ub=GRB.INFINITY) for line in
             self.Lines}
        Pcons: dict[str, Constr] = {}
        Qcons: dict[str, Constr] = {}

        # ---------------添加约束---------------
        # 功率平衡约束
        for bus in self.Buses:
            flow_in = self.LinesOfTBus(bus.ID)
            flow_out = self.LinesOfFBus(bus.ID)
            j = bus.ID
            Pcons[j] = model.addConstr(Qs(P[ln.ID] - ln.R * l[ln.ID] for ln in flow_in) + Qs(pg[j]) == Qs(
                P[ln.ID] for ln in flow_out) + bus.Pd(_t), f"Pcons_{j}")
            Qcons[j] = model.addConstr(Qs(Q[ln.ID] - ln.X * l[ln.ID] for ln in flow_in) + Qs(qg[j]) == Qs(
                Q[ln.ID] for ln in flow_out) + bus.Qd(_t), f"Qcons_{j}")

        # 电压和电流平衡约束
        for line in self.Lines:
            i, j = line.pair
            lid = line.ID
            model.addConstr(
                v[j] == v[i] - 2 * (line.R * P[lid] + line.X * Q[lid]) + (line.R ** 2 + line.X ** 2) * l[lid],
                f"ΔU2_cons_{lid}")
            model.addConstr(P[lid] ** 2 + Q[lid] ** 2 <= l[lid] * v[i], f"SoC_cons_{lid}")

        # 配网源节点电压固定为1pu
        model.addConstr(v['B1'] == 1, 'v_B1==1')

        # 线性发电成本目标函数
        model.setObjective(
            quicksum(g.CostA(_t) * pg0[g.ID] ** 2 + g.CostB(_t) * pg0[g.ID] + g.CostC(_t) for g in self.Gens),
            GRB.MINIMIZE)
        model.setParam('OutputFlag', 0)  # 关闭输出
        model.setParam('QCPDual', 1)  # 启用二次约束规划对偶
        model.update()
        model.optimize()
        if model.Status != GRB.Status.OPTIMAL:
            return False, 0

        for bus in self.Buses:
            j = bus.ID
            bus.V = v[j].X ** 0.5
            try:
                sp = Pcons[j].Pi
            except:
                sp = None if not self.__holdShadowPrice else bus.ShadowPrice
            bus.ShadowPrice = sp

        for line in self.Lines:
            lid = line.ID
            line.I = l[lid].X ** 0.5
            line.P = P[lid].X
            line.Q = Q[lid].X

        for gen in self.Gens:
            j = gen.ID
            gen.P = pg0[j].X
            gen.Q = qg0[j].X

        return True, model.ObjVal
