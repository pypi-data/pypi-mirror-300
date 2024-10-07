"""
#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021-2024 Marcin Orlowski <MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""


def overrides(contract) -> callable:
    """
    Introduces @overrides decorator. Source: https://stackoverflow.com/a/8313042

    :param contract: Class of method being overridden
    :return:
    """

    def overrider(method):
        assert method.__name__ in dir(contract), f"No '{method.__name__}()' to override in '{contract.__name__}' class"
        return method

    return overrider
