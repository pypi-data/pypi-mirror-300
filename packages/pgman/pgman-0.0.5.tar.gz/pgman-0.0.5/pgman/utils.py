import re


def make_result(**kwargs) -> dict:
    result = dict(**kwargs)
    return result


def reduce_sql(sql: str) -> str:
    sql = re.sub("\s+", ' ', sql).strip()
    return sql


def getfv(data: dict | list) -> tuple:
    item = data if isinstance(data, dict) else data[0]
    fs = []
    vs = []
    for k in item.keys():
        fs.append('"{}"'.format(k))
        vs.append('%s')
    fileds = ', '.join(fs)
    values = ', '.join(vs)
    return fileds, values


def check(many: list, must_exist: str):
    fields = None
    for one in many:
        assert one, Exception("Data is empty")
        if fields is None:
            fields = set(one)
            continue
        assert must_exist in fields, Exception("Missing name field")
        assert fields == set(one), Exception("The structure of the data is different")
