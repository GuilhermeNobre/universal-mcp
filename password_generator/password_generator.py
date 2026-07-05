import random
import string


def generate_password(
    length: int = 12,
    include_numbers: bool = True,
    include_special_chars: bool = True,
    include_uppercase: bool = True,
    exclude_ambiguous: bool = False,
    count: int = 1,
) -> str:
    """Generate a random password without saving it.

    Args:
        length: Password length. Must be at least 1.
        include_numbers: Include digits from 0 to 9.
        include_special_chars: Include symbols like !, @, #, and $.
        include_uppercase: Include uppercase letters from A to Z.
        exclude_ambiguous: Exclude ambiguous characters like 0, O, 1, l, and I.
        count: Number of passwords to generate. Defaults to 1.
    """
    if length < 1:
        return "Password length must be at least 1."
    if count < 1:
        return "Count must be at least 1."
    if count > 50:
        return "Count must be 50 or less."

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()-_=+[]{};:,.?/"

    if exclude_ambiguous:
        ambiguous = set("0O1lI")
        lowercase = "".join(char for char in lowercase if char not in ambiguous)
        uppercase = "".join(char for char in uppercase if char not in ambiguous)
        digits = "".join(char for char in digits if char not in ambiguous)

    groups = [lowercase]

    if include_numbers:
        groups.append(digits)

    if include_special_chars:
        groups.append(special_chars)

    if include_uppercase:
        groups.append(uppercase)

    if length < len(groups):
        return (
            f"Password length must be at least {len(groups)} "
            "for the selected character options."
        )

    characters = "".join(groups)
    passwords = []
    for _ in range(count):
        required_chars = [random.choice(group) for group in groups]
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [
            random.choice(characters) for _ in range(remaining_length)
        ]
        random.shuffle(password_chars)
        passwords.append("".join(password_chars))

    return "\n".join(passwords)
