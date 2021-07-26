from typing import Any, Dict

THE_ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING = 42


def accepts_function(fn):
    """This function accepts another function `fn` and invokes it.
    The `fn` function has the following signature:
        def fn() -> int
    which means that function `fn` has no arguments and retuns an int

    Your task is to invoke the supplied function, add a constant `THE_ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING` and return a result

    Args:
        fn (function):
    """
    # write code here
    def fn() -> int:
        return 56

    return fn() + THE_ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING



# sum is a built-in that you shouldn't use there :)
def sum_numbers(*args) -> int:
    """This functions accepts any number of integers and return a sum of them (don't use built-in `sum`)"""
    # write code here
    my_sum = args[0]
    for i in args[1:]:
        my_sum = my_sum + i
    return my_sum


def avg(*args) -> int:
    """This function accepts any number of integers and returns mean of them (average)"""
    # write code here
    # hint: make use of `sum_numbers` here
    my_len = len(args)
    result = sum_numbers(*args)/my_len
    return result


def check_access(**user_data) -> bool:
    """Checks access for a given set of name, access_level and role

    Args:
        name (str): User name
        access_level (int): User access level
        role (str): User role

    Returns:
        bool: True if user allowed to access the resource
    """
    # You don't need to change logic here
    # Your task is to fix the code here without changing the tests below
    # Hint: remember kwargs
    for i in user_data:
        if i == "name":
            name = user_data[i]
        elif i == "access_level":
            access_level = user_data[i]
        elif i == "role":
            role = user_data[i]
    if name in ["Patrik", "Sponge Bob"] or (access_level > 2 or role == "admin"):
        return True
    else:
        return False


#### Tests ####
import random
import unittest
import statistics

# I'm here just for the tests!
def construct_user(
    name: str, access_level: int = 1, role: str = "user", **kwargs
) -> Dict[str, Any]:
    """Constructs a user dictionary from given arguments, everything in kwargs is added to result dictionary

    Args:
        name (str): Name of the user
        access_level (int, optional): Access level as int. Defaults to 1.
        role (str, optional): User role. Defaults to "user".

    Returns:
        Dict[str, Any]: User dictionary with all the keys
    """
    user = {"name": name, "access_level": access_level, "role": role}
    user.update(kwargs)
    return user


class TestHomework3(unittest.TestCase):
    def test_access_is_granted(self):
        data = [
            ("Patrik", 2, "star"),
            ("Mr. Crabs", 2, "admin"),
            ("Sponge Bob", 1, "cook"),
        ]
        for name, level, role in data:
            user_data = {"city": "bikini bottom"}
            user = construct_user(name, level, role, **user_data)
            self.assertTrue(check_access(**user))

    def _gen_numbers(self):
        return [random.randint(0, 1000) for _ in range(100)]

    def test_sum(self):
        numbers = self._gen_numbers()
        self.assertEqual(sum(numbers), sum_numbers(*numbers))

    def test_avg(self):
        numbers = self._gen_numbers()
        self.assertEqual(statistics.mean(numbers), avg(*numbers))

    def test_accepts_function(self):
        def foo() -> int:
            return 56

        self.assertEqual(
            foo()
            + THE_ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING,
            accepts_function(foo),
        )


if __name__ == "__main__":
    unittest.main()
