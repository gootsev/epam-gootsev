import random
import statistics

# If you read that comment, here's an additional link for you: https://pyformat.info/


class Metrics:
    """Don't worry about classes for now. We just need the data"""

    def __init__(self):
        self.cpu_data = [random.randint(0, 100) for _ in range(8)]
        self.memory_used = random.randint(300, 2048)
        self.memory_total = 2048
        self.load_avg = (
            statistics.mean(self.cpu_data) * 1.0054
        )  # just to have more digits
        self.agent = "metric-gatherer.%s" % random.randint(1000, 9999)
        self.agent_address = random.choice([16384, 32768, 4096])


def format_with_fstring(data: Metrics):
    cpu_1 = data.cpu_data[1]
    mem_used = data.memory_used
    load_avg = data.load_avg
    tmp = f"CPU #1: {cpu_1}%, Memory used: {mem_used}, Load avg: {load_avg:.{4}}"
    return f"{tmp:*^64}"


def format_with_format(data: Metrics):

    """Return a string that is formatted with `data` by using a "format" method
    that would have the following format:
      [3124] CPU #7: 25%, Memory used: 450, Load avg: 3.23
    where:
        3124 -- is a pid of gatherer agent from metrics data (the digits after "metric-gatherer." in data.agent,
        for example if data.agent is "metric-gatherer.3124")
        25 - is the stat for 5th CPU in data
        450 - is a used memory metric from data
        3.23 - is a load_avg from data limited to two digits after decimal (3.2345 -> 3.23)

    Requirements:
        * The string should limit all floats to two digits after decimal (e.g. 3.1415 -> 3.14)
        * The text format should be exactly as in comment (tests would check for that)
        * The string should be right aligned and padded with dashes ("-") to have a total length of 64.
    For example:
        "[3124] CPU #7: 25%, Memory used: 450, Load avg: 3.23"
    should become
        "------------[3124] CPU #7: 25%, Memory used: 450, Load avg: 3.23"

    Args:
        data (Metrics): Data you have to format

    Links:
        https://docs.python.org/3/library/string.html#format-examples
    """
    pid = data.agent[-4:]
    cpu_7 = data.cpu_data[7]
    mem_used = data.memory_used
    load_avg = data.load_avg
    tmp = "[{!s}] CPU #7: {!s}%, Memory used: {!s}, Load avg: {:.4}".format(pid,cpu_7,mem_used,load_avg)
    return f"{tmp:->64}"


def format_with_percent(data: Metrics):
    """Return a string that is formatted with `data` by using a "%" formatting
    that would have the following format:
      [0x4000] CPU #7: 87%, Memory used: 900, Load avg: 1.25
    where:
        0x4000 -- is an adress of agent in memory from data.agent_address converted to hexadecimal
        87 - is the stat for 7th CPU in data
        900 - is a used memory metric from data
        1.25 - is a load_avg from data limited to two digits after decimal (1.2489 -> 1.25)

    Requirements:
        * The string should limit all floats to two digits after decimal (e.g. 3.1415 -> 3.14)
        * The text format should be exactly as in comment (tests would check for that)
        * The string should be left aligned and padded with spaces (" ") to have a total length of 64.
    For example:
        "[0x4000] CPU #7: 87%, Memory used: 900, Load avg: 1.25"
    should become
        "'          [0x4000] CPU #7: 87%, Memory used: 900, Load avg: 1.25'"

    Args:
        data (Metrics): Data you have to format

    Links:
        https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
    """
    address = data.agent_address
    cpu_7 = data.cpu_data[7]
    mem_used = data.memory_used
    load_avg = data.load_avg
    tmp = "[0x%(address)x] CPU #7: %(cpu)i%%, Memory used: %(mem_used)i, Load avg: %(load_avg)0.2f" % {'address': address, 'cpu': cpu_7, 'mem_used': mem_used, 'load_avg':load_avg}
    return f"{tmp:>64}"


#### Tests ####

import unittest
from string import Template


class TestStringFormatters(unittest.TestCase):
    def get_data(self):
        return Metrics()

    def get_pid(self, agent: str) -> str:
        acc = ""
        found_dot = False
        for char in agent:
            if found_dot:
                acc += char
            if char == ".":
                found_dot = True
        assert len(acc) == 4, acc
        return acc

    def test_fstring(self):
        """
        For example:
            "CPU #1: 10%, Memory used: 450, Load avg: 3.23"
        should become
            "*********CPU #1: 10%, Memory used: 450, Load avg: 3.23**********"
        """
        data = self.get_data()
        fstring_template = Template(
            "CPU #1: $cpu_1%, Memory used: $mem_used, Load avg: $load_avg"
        )
        templated = fstring_template.substitute(
            cpu_1=data.cpu_data[1],
            mem_used=data.memory_used,
            load_avg=round(data.load_avg, 2),
        )
        formatted = templated.center(64, "*")

        user_result = format_with_fstring(data)
        self.assertEqual(user_result, formatted)

    def test_format_method(self):
        """
        For example:
            "[3124] CPU #7: 25%, Memory used: 450, Load avg: 3.23"
        should become
            "------------[3124] CPU #7: 25%, Memory used: 450, Load avg: 3.23"
        """
        data = self.get_data()
        fstring_template = Template(
            "[$pid] CPU #7: $cpu_7%, Memory used: $mem_used, Load avg: $load_avg"
        )
        templated = fstring_template.substitute(
            pid=self.get_pid(data.agent),
            cpu_7=data.cpu_data[7],
            mem_used=data.memory_used,
            load_avg=round(data.load_avg, 2),
        )
        formatted = templated.rjust(64, "-")

        user_result = format_with_format(data)
        self.assertEqual(user_result, formatted)

    def test_format_percent(self):
        """
        For example:
            "[0x4000] CPU #7: 87%, Memory used: 900, Load avg: 1.25"
        should become
            "'          [0x4000] CPU #7: 87%, Memory used: 900, Load avg: 1.25'"
        """
        data = self.get_data()
        fstring_template = Template(
            "[$hex] CPU #7: $cpu_7%, Memory used: $mem_used, Load avg: $load_avg"
        )
        templated = fstring_template.substitute(
            hex=hex(data.agent_address),
            cpu_7=data.cpu_data[7],
            mem_used=data.memory_used,
            load_avg=round(data.load_avg, 2),
        )
        formatted = templated.rjust(64, " ")

        user_result = format_with_percent(data)
        self.assertEqual(user_result, formatted)


if __name__ == "__main__":
    unittest.main()
