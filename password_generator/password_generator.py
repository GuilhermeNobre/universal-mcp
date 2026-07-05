import random
import string


def generate_password(
    length: int = 12,
    include_numbers: bool = True,
    include_special_chars: bool = True,
    include_uppercase: bool = True,
) -> str:
    """Generate a random password without saving it.

    Args:
        length: Password length. Must be at least 1.
        include_numbers: Include digits from 0 to 9.
        include_special_chars: Include symbols like !, @, #, and $.
        include_uppercase: Include uppercase letters from A to Z.
    """
    if length < 1:
        return "Password length must be at least 1."

    required_chars = [random.choice(string.ascii_lowercase)]
    characters = string.ascii_lowercase

    if include_numbers:
        required_chars.append(random.choice(string.digits))
        characters += string.digits

    if include_special_chars:
        required_chars.append(random.choice(string.punctuation))
        characters += string.punctuation

    if include_uppercase:
        required_chars.append(random.choice(string.ascii_uppercase))
        characters += string.ascii_uppercase

    if length < len(required_chars):
        return (
            f"Password length must be at least {len(required_chars)} "
            "for the selected character options."
        )

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [
        random.choice(characters) for _ in range(remaining_length)
    ]
    random.shuffle(password_chars)

    return "".join(password_chars)
