from abc import ABCMeta, abstractmethod
from functools import reduce
from operator import add, sub, mul, truediv, floordiv
from typing import Callable, Iterable, Optional, Union, overload
import bisect
import xml.etree.ElementTree as ET
from feasytools.pq import PQueue

class TimeFunc(metaclass=ABCMeta):
    '''时变函数'''
    @abstractmethod
    def __call__(self,time:int)->float: ...
    @abstractmethod
    def __str__(self)->str: ...
    def __add__(self,other:'FloatLike')->'TimeFunc':
        return calcFunc(self,other,'+')
    def __sub__(self,other:'TimeFunc')->'TimeFunc':
        return calcFunc(self,other,'-')
    def __mul__(self,other)->'TimeFunc':
        return calcFunc(self,other,'*')
    def __truediv__(self,other)->'TimeFunc':
        return calcFunc(self,other,'/')
    def __floordiv__(self,other)->'TimeFunc':
        return calcFunc(self,other,'//')

_oper_trans = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '//': floordiv
}
_Oper = Callable[[float,float],float]
FloatLike = Union[TimeFunc,float,int]

class OverrideFunc(TimeFunc):
    '''覆盖函数. 正常情况下返回原始时间函数的值, 当设置了覆盖值时返回覆盖值'''
    def __init__(self,default:TimeFunc,override_val:Optional[float] = None):
        self._val:TimeFunc=default
        self._override:Optional[float] = override_val
    
    def __call__(self,t:int)->float:
        if self._override is not None: return self._override
        return self._val(t)
    
    def setOverride(self,overval:float):
        '''设置覆盖值'''
        self._override=overval
    
    def clearOverride(self):
        '''清除覆盖值'''
        self._override=None
    
    def __repr__(self):
        if self._override is None: return f"OverrideF<{self._val}>"
        return f"OverrideF<O={self._override}>"

    def __str__(self):
        if self._override is None: return str(self._val)
        return str(self._override)+"(Override)"

class PlusFunc(TimeFunc):
    '''和函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)+self._f2(_t)
    def __repr__(self)->str: return f"PlusFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class QuickSumFunc(TimeFunc):
    '''快速求和函数'''
    def __init__(self,funcs:'list[TimeFunc]'): self._fs=funcs
    def __call__(self,_t:int)->float: return sum(f(_t) for f in self._fs)
    def __repr__(self)->str: return f"QuickSumFunc({self._fs})"
    def __str__(self)->str: return repr(self)

class MinusFunc(TimeFunc):
    '''差函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)-self._f2(_t)
    def __repr__(self)->str: return f"MinusFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class MulFunc(TimeFunc):
    '''积函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)*self._f2(_t)
    def __repr__(self)->str: return f"MulFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class QuickMulFunc(TimeFunc):
    '''快速求积函数'''
    def __init__(self,funcs:'list[TimeFunc]'): self._fs=funcs
    def __call__(self,_t:int)->float: return reduce(mul, (f(_t) for f in self._fs))
    def __repr__(self)->str: return f"QuickMulFunc({self._fs})"
    def __str__(self)->str: return repr(self)

class TrueDivFunc(TimeFunc):
    '''商函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)/self._f2(_t)
    def __repr__(self)->str: return f"TrueDivFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class FloorDivFunc(TimeFunc):
    '''整除函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)//self._f2(_t)
    def __repr__(self)->str: return f"FloorDivFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class ConstFunc(TimeFunc):
    '''常数函数'''
    def __init__(self,const:float): self._val:float=const
    def __call__(self,time:int)->float: return self._val
    def __repr__(self)->str: return f"ConstFunc({self._val})"
    def __str__(self)->str: return str(self._val)

class SegFunc(TimeFunc):
    '''分段常数函数'''
    _tl:'list[int]'
    _d:'list[float]'
    
    @overload
    def __init__(self,time_line:'list[int]', data:'list[float]'): ...
    @overload
    def __init__(self,time_line:'list[tuple[int,float]]'): ...
    @overload
    def __init__(self): ...

    def __init__(self,time_line:'Union[list[int],tuple[int,float]]'=[], data:'list[float]' = []):
        if len(data) == 0:
            self.__init1(time_line)
        else:
            self.__init0(time_line,data)

    def __init0(self, time_line:'list[int]', data:'list[float]'):
        if len(time_line) != len(data):
            raise ValueError(f"Time line length {len(time_line)} is not equal to data length {len(data)}.")
        for i in range(1,len(time_line)):
            if time_line[i]<=time_line[i-1]:
                raise ValueError(f"Time must be strictly increasing: [{i}]={time_line[i]}<=[{i-1}]={time_line[i-1]}")
        self._tl = time_line
        self._d = data
    
    def __init1(self,time_line:'list[tuple[int,float]]'):
        self._tl = [t for t,_ in time_line]
        self._d = [d for _,d in time_line]
        for i in range(1,len(self._tl)):
            if self._tl[i]<=self._tl[i-1]:
                raise ValueError(f"Time must be strictly increasing: [{i}]={self._tl[i]}<=[{i-1}]={self._tl[i-1]}")
    
    def __len__(self)->int: return len(self._d)

    def __iter__(self): return zip(self._tl,self._d)

    def __call__(self,time:int)->float:
        if time < self._tl[0]:
            raise ValueError(f"Time {time} must be later than the start time {self._tl[0]}.")
        return self._d[bisect.bisect_right(self._tl, time) - 1]
    
    def __repr__(self)->str:
        return f"SegFunc({[(t,d) for t,d in self]})"

    def __str__(self)->str:
        return str([(t,d) for t,d in self])
    
    def to_xml(self, tag_name:str="seg", tag_item:str="item", 
               attr_time:str="time", attr_value:str="val",) -> str:
        return ET.tostring(self.to_xml_elem(tag_name,tag_item,attr_time,attr_value), "unicode")
        
    def to_xml_elem(self, tag_name:str="seg", tag_item:str="item", 
                    attr_time:str="time", attr_value:str="val") -> ET.Element:
        e = ET.Element(tag_name)
        for t, d in self:
            e.append(ET.Element(tag_item,{attr_time:str(t),attr_value:str(d)}))
        return e
    
    def add(self, time:int, val:float):
        assert len(self._tl) == 0 or time > self._tl[-1]
        self._tl.append(time)
        self._d.append(val)

    def repeat(self, times:int, period:int)->'SegFunc':
        if len(self._tl) == 0: return SegFunc()
        if times == 1: return SegFunc(self._tl,self._d)
        if times < 1: raise ValueError(f"times must be greater than 0, but got {times}.")
        if period <= self._tl[-1]: raise ValueError(f"period {period} must be greater than the last time {self._tl[-1]}.")
        ret = SegFunc()
        for i in range(times):
            for t,d in self:
                ret.add(t+i*period,d)
        return ret
    
    @staticmethod
    def qs(v:'list[SegFunc]') -> 'SegFunc':
        ret = SegFunc()
        pq:'PQueue[tuple[int, int]]' = PQueue()
        sum = 0
        n = len(v)
        for i in range(n):
            if len(v[i]) > 0: pq.push(v[i]._tl[0], (i, 0))
        ctime = -1
        while not pq.empty():
            htime, (idx, prog) = pq.top
            pq.pop()
            if ctime != htime:
                if ctime >= 0:
                    ret.add(ctime, sum)
                ctime = htime
            if prog > 0:
                sum = sum - v[idx]._d[prog - 1] + v[idx]._d[prog]
            else:
                sum += v[idx]._d[prog]
            if prog < len(v[idx]) - 1:
                pq.push(v[idx]._tl[prog + 1], (idx, prog + 1))
        if len(ret._tl) == 0:
            ret.add(0, sum)
        elif ctime >= 0 and ctime != ret._tl[-1]:
            ret.add(ctime, sum)
        return ret

    def __neg__(self)->'SegFunc':
        return SegFunc(self._tl,[-d for d in self._d])
    
    def __add__(self,other:'FloatLike')->'SegFunc':
        if isinstance(other,(float,int)):
            return SegFunc(self._tl,[d + other for d in self._d])
        elif isinstance(other,ConstFunc):
            return SegFunc(self._tl,[d + other._val for d in self._d])
        elif isinstance(other,SegFunc):
            return SegFunc.qs([self, other])
        else:
            return PlusFunc(self, other)
    
    def __sub__(self,other:'FloatLike')->'SegFunc':
        if isinstance(other,(float,int)):
            return SegFunc(self._tl,[d - other for d in self._d])
        elif isinstance(other,ConstFunc):
            return SegFunc(self._tl,[d - other._val for d in self._d])
        elif isinstance(other,SegFunc):
            return SegFunc.qs([self, -other])
        else:
            return MinusFunc(self, other)


class TimeImplictFunc(TimeFunc):
    '''隐式时变函数, 即调用的时机决定了时间, 而无需在__call__时指定。__call__的参数time无效'''
    def __init__(self,func:'Callable[[],float]'):self._f=func
    def __call__(self,time:int)->float:return self._f()
    def __repr__(self)->str:return f"TimeImplictFunc({self._f})"
    def __str__(self)->str: return repr(self)


class ComFunc(TimeFunc):
    '''将普通Python函数包装成可运算函数'''
    def __init__(self,func:'Callable[[int],float]'):self._f=func
    def __call__(self,time:int)->float:return self._f(time)
    def __repr__(self)->str:return f"ComFunc({self._f})"
    def __str__(self)->str: return repr(self)


class ManualFunc(TimeFunc):
    '''手动指定常数函数'''
    def __init__(self,init_val:float):self._v=init_val
    def setManual(self,val:float):self._v=val
    def __call__(self,time:int)->float:return self._v
    def __repr__(self)->str:return f"ManualFunc({self._v})"
    def __str__(self)->str: return str(self._v)+"(Manual)"

def __calc_c0(f1:Union[ConstFunc,float],f2:float,op:_Oper)->float:
    if isinstance(f1,float): return op(f1,f2)
    elif isinstance(f1,ConstFunc): return op(f1._val,f2)
    else: raise TypeError(f1)

def __calc_c1(f1:SegFunc,f2:float,op:_Oper)->SegFunc:
    return SegFunc(f1._tl,[op(d,f2) for d in f1._d])

def __calc_c2(f1:TimeImplictFunc,f2:float,op:_Oper)->TimeImplictFunc:
    return TimeImplictFunc(lambda: op(f1._f(),f2))

def quicksum(funcs:Iterable[TimeFunc])->TimeFunc:
    '''快速求和'''
    ret = list(funcs)
    if len(ret)==0: return ConstFunc(0)
    consts = []
    segs = []
    others = []
    for f in ret:
        if isinstance(f,ConstFunc): consts.append(f._val)
        elif isinstance(f,SegFunc): segs.append(f)
        else: others.append(f)
    if len(others)==0:
        if len(segs)==0: return ConstFunc(sum(consts))
        else: return SegFunc.qs(segs) + sum(consts)
    if len(segs)==0 and len(consts)==0:
        return QuickSumFunc(others)
    elif len(segs)==0:
        others.append(ConstFunc(sum(consts)))
        return QuickSumFunc(others)
    elif len(consts)==0:
        others.append(SegFunc.qs(segs))
        return QuickSumFunc(others)
    else:
        s = SegFunc.qs(segs) + sum(consts)
        others.append(s)
        return QuickSumFunc(others)

def quickmul(funcs:Iterable[TimeFunc])->TimeFunc:
    '''快速求积'''
    ret = list(funcs)
    if len(ret)==0: return ConstFunc(1)
    if len(ret)==1: return ret[0]
    if len(ret)==2: return MulFunc(ret[0],ret[1])
    return QuickMulFunc(ret)

def calcFunc(f1:FloatLike,f2:FloatLike,op:str)->TimeFunc:
    _op = _oper_trans[op]
    if isinstance(f2,ConstFunc): f2=f2._val
    if isinstance(f2,(float,int)):
        if isinstance(f1,(ConstFunc,float,int)): return ConstFunc(__calc_c0(f1,f2,_op))
        elif isinstance(f1,SegFunc): return __calc_c1(f1,f2,_op)
        elif isinstance(f1,TimeImplictFunc): return __calc_c2(f1,f2,_op)
        else: f2 = ConstFunc(f2)
    if isinstance(f1,(float,int)): f1 = ConstFunc(f1)
    if isinstance(f1,ConstFunc) and op in ['+','*']:
        if isinstance(f2,SegFunc): return __calc_c1(f2,f1._val,_op)
        elif isinstance(f2,TimeImplictFunc): return __calc_c2(f2,f1._val,_op)
    assert isinstance(f1,TimeFunc) and isinstance(f2,TimeFunc)
    if op=='+': return PlusFunc(f1,f2)
    elif op=='-': return MinusFunc(f1,f2)
    elif op=='*': return MulFunc(f1,f2)
    elif op=='/': return TrueDivFunc(f1,f2)
    elif op=='//': return FloorDivFunc(f1,f2)
    else: raise ValueError(op)

def makeFunc(time_line:'list[int]',data:list)->TimeFunc:
    '''生成分段常数函数或常数函数'''
    if len(time_line)!=len(data):
        raise ValueError(f"Time line length {len(time_line)} is not equal to data length {len(data)}.")
    if len(data)==1: return ConstFunc(data[0])
    else: return SegFunc(time_line,data)
