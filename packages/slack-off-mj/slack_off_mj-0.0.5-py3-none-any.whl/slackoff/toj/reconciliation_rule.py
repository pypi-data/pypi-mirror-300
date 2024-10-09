# 把表格数据解析成json数据
# 步骤：解析规则 -> 执行解析 -> 合并解析结果
from abc import ABC, abstractmethod
from collections.abc import Iterator
from .reconciliation_source import DataSource
from .reconciliation_exper_processor import NifiExpression, DefaultCalcExpression


# 规则的行为
class Rule(ABC):
    # 规则解析
    @abstractmethod
    def parse(self, ctx):
        pass


class OrganizationMergeRule:
    def __init__(self):
        self.merges = [DictMerge(), StringMerge(), IntegerMerge(), FloatMerge()]

    @abstractmethod
    def merge(self, args):
        if not isinstance(args, list):
            raise Exception()
        for merge in self.merges:
            if merge.check(args):
                return merge.merge(args)
        return None


class DictMerge:
    def merge(self, args):
        if self.check(args=args):
            result = {}
            for arg in args:
                result.update(arg)
            return result
        return None

    @staticmethod
    def check(args):
        if not isinstance(args, list):
            raise Exception()
        return all(isinstance(item, dict) for item in args)


class StringMerge:
    def merge(self, args):
        if self.check(args):
            result = ""
            for arg in args:
                result = result.join(arg)
            return result
        return None

    @staticmethod
    def check(args):
        if not isinstance(args, list):
            raise Exception()
        return all(isinstance(item, str) for item in args)


class IntegerMerge:
    def merge(self, args):
        if self.check(args):
            result = 0
            for arg in args:
                result += arg
            return result
        return None

    @staticmethod
    def check(args):
        return all(isinstance(item, int) for item in args)


class FloatMerge:
    def merge(self, args):
        if self.check(args):
            result = 0
            for arg in args:
                result += arg
            return result
        return None

    @staticmethod
    def check(args):
        return all(isinstance(item, float) for item in args)


# 一、组织数据
# 1. 按照组织规则去生成对应的json
class AbsOrganizationExperRule(Rule, ABC):
    def __int__(self, rules, process, merge):
        if not isinstance(rules, BaseProcess):
            Exception()
        self.rules = rules
        self.process = process
        self.key_level = {}  # 健映射层级
        self.merge = merge  # 合并规则
        self.KEY_ROW = "row"
        self.KEY_THIS = "this"
        self.KEY_MOUNT = "mount"

    # 深度优先
    def parse(self, ctx):
        if self.KEY_ROW not in ctx:
            raise Exception("table数据未定义")
        tables = ctx[self.KEY_ROW]
        if not isinstance(tables, Iterator):
            raise Exception()
        # 解析后的结果
        table_result = {}
        for row in tables:
            ctx[self.KEY_ROW] = row
            ctx[self.KEY_THIS] = table_result
            ctx[self.KEY_MOUNT] = {}  # 数据挂载
            frame = {
                "rules": self.rules,  # 规则
                "ctx": ctx,           # 给规则执行时，需要用到的上下文
                "part": {             # 局部
                    "this": table_result
                }
            }
            table_result = self.doParse(frame)
        return table_result

    def doParse(self, frame):
        rules = frame["rules"]
        children = "children"
        mount = frame["ctx"][self.KEY_MOUNT]

        filter_result = getattr(self.process, "filter", None)(self.rules, frame["ctx"])  # 过滤
        if filter_result:
            # 如果过滤掉，就返回原值
            return frame["part"]["this"]

        # 回复为当前局部的挂载
        frame["ctx"][self.KEY_MOUNT] = mount

        # 1. 生成键值对的键
        returned_rule = getattr(self.process, "rule", None)(rules, frame["ctx"])
        if children not in rules:
            return returned_rule

        self.doExecute(frame=frame)

        # 局部上下文：已经解析好的，同级别的上下文
        part_context = frame["part"]["this"]

        merge_work = {}  # 合并的工作区
        this = {}  # 对象上下文
        if returned_rule in part_context:
            merge_work = part_context
            this = part_context[returned_rule]
        vals = []

        # 2. 解析值，无限套娃children
        if children in rules and len(rules[children]) > 0:
            frame["ctx"][self.KEY_THIS] = this
            for rule in rules[children]:
                val = self.doParse({
                    "rules": rule,
                    "ctx": frame["ctx"],
                    "part": {
                        "top_val": returned_rule,
                        "this": this
                    }
                })
                vals.append(val)

        # 3. 合并值
        # 合并自定义规则之后的值
        merge_vals = getattr(self.merge, "merge", None)(vals)

        # 合并同一父级的值
        if returned_rule in merge_work:
            origin_vals = merge_work[returned_rule]
            merge_work[returned_rule] = getattr(self.merge, "merge", None)([merge_vals, origin_vals])
            return merge_work
        # 如果没有共同父级，直接赋值
        else:
            part_context[returned_rule] = merge_vals
            return part_context

    # 规则扩展
    @abstractmethod
    def doExecute(self, frame):
        pass


# 二、合并
# 组织数据合并规则
class OrganizationRule(AbsOrganizationExperRule):
    def __init__(self, rules, data):
        self.__int__(rules, OrganizationProcess(data), OrganizationMergeRule())

    def doExecute(self, frame):
        pass


# 通用的规则处理器
class BaseProcess:
    # source数据源
    def __init__(self, source):
        if not isinstance(source, DataSource):
            raise Exception()
        self.source = source
        self.exper_processor = NifiExpression(DefaultCalcExpression())

    @staticmethod
    def filter(regulation, data):
        handle_name = "filter"
        if handle_name not in regulation:
            return False
        returned = Utils.handle(regulation[handle_name], handle_name, data)
        if returned is None:
            raise Exception("filter只支持函数或对象，并且必须返回bool类型")
        return returned

    @staticmethod
    def children(regulation, stack):
        children = "children"
        if children in regulation and isinstance(regulation[children], list):
            for child in regulation[children]:
                stack.append(child)

    def rule(self, regulation, ctx):
        rule = "rule"
        ctx["filename"] = getattr(self.source, "filename", None)()
        if isinstance(rule, str):
            return self.rule_str(rule, ctx)
        if rule not in regulation:
            raise Exception("唯一标识rule没有定义")
        returned = Utils.handle(regulation[rule], rule, ctx)
        if returned is None:
            raise Exception("rule没有返回值")
        if isinstance(returned, str) and "exper:" in returned:
            return self.rule_str(rule, ctx)
        return returned

    def rule_str(self, rule, ctx):
        # 判断是否是表达式
        if "exper:" not in rule:
            return rule
        else:
            return self.exper_processor.processor(exper_=rule.replace("exper:", ""), context_=ctx)


# 组织数据规则处理器
class OrganizationProcess(BaseProcess):
    pass


class Utils:
    @staticmethod
    def handle(call, func, data):
        if callable(call):
            return call(data)
        elif isinstance(call, dict):
            return getattr(call, func)(data)
        elif isinstance(call, str):
            return call
