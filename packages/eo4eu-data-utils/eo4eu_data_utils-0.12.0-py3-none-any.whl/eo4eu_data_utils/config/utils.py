def _to_bool(input) -> bool:
    if isinstance(input, bool):
        return input
    if isinstance(input, str):
        input_lower = input.lower()
        if input_lower == "true" or input_lower == "1":
            return True
        else:
            return False
    if isinstance(input, int):
        return False if input == 0 else True
    return False
