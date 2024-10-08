from abc import ABC, abstractmethod
from reconciliation_source import XlsxDataSource
from reconciliation_rule import OrganizationRule
from reconcilization_merge import DefaultMerge
from reconciliation_to_excel import ToExcel


# 配置整合入口
class Reconciliation(ABC):
    @abstractmethod
    def handle(self):
        pass


# 默认实现
class XlsxReconciliation(Reconciliation):
    def __init__(self, rules_):
        if "generator" not in rules_:
            raise ValueError("rules must contain 'sources'")
        if "merge" not in rules_:
            raise ValueError("rules must contain 'merge'")
        if "toXlsx" not in rules_:
            raise ValueError("rules must contain 'toXlsx'")
        self.rules = rules_

    def handle(self):
        load_sources = []
        for g in self.rules["generator"]:
            iterator = XlsxDataSource(g["source"])
            organization = OrganizationRule(g["rules"], iterator)  # 迭代器
            load_sources.append(organization.parse({
                "table": iterator  # 这个是一个迭代器
            }))
        # 合并数据
        if len(load_sources) == 0:
            raise ValueError("no sources found")
        while len(load_sources) == 1:
            load_sources.append({})
        defaultMerge = DefaultMerge(self.rules["merge"])
        mergedBefore = defaultMerge.merges(load_sources)
        to_excel = ToExcel(self.rules["toXlsx"])
        to_excel.write(mergedBefore)
