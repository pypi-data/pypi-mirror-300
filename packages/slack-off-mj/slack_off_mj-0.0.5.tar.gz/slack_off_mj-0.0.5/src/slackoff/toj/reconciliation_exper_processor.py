from abc import ABC, abstractmethod
from re import findall, match
import math


# 表达式处理器
class ExperProcessor(ABC):
    @abstractmethod
    def processor(self, exper_, context_):
        pass


# 处理中缀表达式
class NifiExpression(ExperProcessor):
    def __init__(self, calc):
        if not isinstance(calc, CalcExpression):
            raise TypeError
        self.calc = calc

    def processor(self, exper_, context_):
        if isinstance(exper_, str):
            variable_exper = findall(r"\$\{([]\[a-zA-Z0-9\u4e00-\u9fff\"\']+)}", exper_)
            for i in range(len(variable_exper)):
                variable = variable_exper[i]
                exp_val = context_
                chains = findall(r"(\[[a-zA-Z0-9-\u4e00-\u9fff\"\']+]|[a-zA-Z0-9-\u4e00-\u9fff]+)", variable)
                for chain in chains:
                    if "[" in chain and "]" in chain:
                        key = findall(r"[^]\"\'\[]", chain)
                        if match(r"\d+", key[0]) is not None:
                            exp_val = exp_val[int(key[0])]
                        elif isinstance(key[0], str):
                            exp_val = exp_val[key[0]]
                    elif match("^[0-9]+$", chain) is not None:
                        exp_val = exp_val[int(chain)]
                    elif match("^[a-zA-Z0-9-\u4e00-\u9fff]+$", chain) is not None:
                        exp_val = exp_val[chain]
                if isinstance(exp_val, str) or isinstance(exp_val, int) or isinstance(exp_val, float) or isinstance(exp_val, bool):
                    exper_ = exper_.replace("${" + variable + "}", str(exp_val))

            return self.calc.calc(exper_)
        else:
            raise ValueError("表达式必须处理为数组")


class CalcExpression(ABC):
    @abstractmethod
    def calc(self, exper_):
        pass


class DefaultCalcExpression(CalcExpression):
    safe_globals = {
        '__builtins__': {},
        'math': math,
        'str': str,
        'int': int,
        'float': float
    }

    def calc(self, expression):
        try:
            compiled_code = compile(expression, "<string>", "eval")
            result = eval(compiled_code, self.safe_globals)
            return result
        except (SyntaxError, NameError, TypeError) as e:
            return f"Invalid expression: {e}"
