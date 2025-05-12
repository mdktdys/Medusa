def get_number_para_emoji(number: int | None) -> str:
    return ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", ""][number if number is not None else -1]
