from typing import NamedTuple


class ClippingRange(NamedTuple):
    start: int
    end: int


def calculate_match_rate(
    range_list_true: list[ClippingRange],
    range_list_target: list[ClippingRange],
    err_start: int = 0,
    err_end: int = 0,
) -> float:
    def extract_numbers(range_list: list[ClippingRange]) -> set[int]:
        numbers: set[int] = set()
        for start, end in range_list:
            numbers.update(range(start - err_start, end + 1 + err_end))
        return numbers

    set_1 = extract_numbers(range_list_true)
    set_2 = extract_numbers(range_list_target)

    # 一致した数値を数える
    matching_numbers = set_1.intersection(set_2)

    # 一致率を計算
    match_rate = len(matching_numbers) / len(set_1) * 100
    return match_rate


range_list_true = [
    ClippingRange(1, 2),
    ClippingRange(3, 19),
    ClippingRange(20, 25),
]

range_list_target = [
    ClippingRange(4, 26),
    ClippingRange(20, 26),
]

match_rate = calculate_match_rate(
    range_list_true,
    range_list_target,
)

print(f"一致率: {match_rate:.2f}%")
