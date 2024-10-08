from dataclasses import dataclass, field
import re


@dataclass
class NegexResult:
    match: bool = False
    tokens: list[tuple[str, str, int, int]] = field(default_factory=list)

    def __iter__(self):
        """
        Allows iteration over the tokens in the NegexResult instance.

        :yields: Each token from the tokens list one by one.
        """
        for token in self.tokens:
            yield token


def splitseps(string: str, separators: list[str]) -> list[tuple[str, int, int]]:
    """
    Splits the string based on the list of separators, returning a list of tuples.
    Each tuple contains a substring from the string and its start and end index.

    :param string: The string to be split.
    :param separators: A list of separator strings to split the string.
    :returns: A list of tuples (substring, start_index, end_index).
    """
    # Escape separators for regex
    escaped_separators = [re.escape(sep) for sep in separators]

    # Create the regex pattern to match any of the separators
    pattern = f"({'|'.join(escaped_separators)})"

    # Find all matches and split the string
    matches = list(re.finditer(pattern, string))

    # List to store the result
    result = []

    last_end = 0

    for match in matches:
        start, end = match.span()

        # Add non-separator substring if it exists
        if start > last_end:
            result.append((string[last_end:start], last_end, start - 1))

        # Add the separator
        result.append((string[start:end], start, end - 1))

        last_end = end

    # Add the final non-separator substring if it exists
    if last_end < len(string):
        result.append((string[last_end:], last_end, len(string) - 1))

    return result


def _remove_consecutive_splits(splits, strings_to_check: list[str] = None) -> list[tuple[str, int, int]]:
    """
    Removes all but the first occurrence of each section of consecutive duplicate tuples 
    based on the first element of the tuple. If strings_to_check is provided, only those 
    strings will be checked for consecutive duplicates.

    :param data: List of tuples where each tuple contains a string as its first element.
    :param strings_to_check: List of strings for which consecutive duplicates should be removed.
    :returns: A list with consecutive duplicates removed based on the provided strings_to_check.
    """
    if not splits:
        return []

    if strings_to_check is None:
        strings_to_check = set(tup[0] for tup in splits)

    result = [splits[0]]  # Start with the first item
    for i in range(1, len(splits)):
        if splits[i][0] != splits[i-1][0] or splits[i][0] not in strings_to_check:
            result.append(splits[i])

    return result


def parse(string: str, pattern: str) -> NegexResult:
    special_symbols = ["*", "~"]
    splits = splitseps(pattern, special_symbols)
    splits = _remove_consecutive_splits(splits, special_symbols)

    # Process splits into tokens
    merged_splits = []
    tilde_mode = False
    tilde_text = ''
    for split in splits:
        token_text = split[0]
        if token_text == '~':
            if tilde_mode:
                # End of tilde section
                merged_splits.append(('~', tilde_text))
                tilde_text = ''
                tilde_mode = False
            else:
                # Start of tilde section
                tilde_mode = True
        elif token_text == '*':
            merged_splits.append(('*', None))
        else:
            if tilde_mode:
                tilde_text += token_text
            else:
                merged_splits.append(('', token_text))

    # Now attempt to match these tokens against the string
    index = 0
    result_tokens = []
    match = True
    string_length = len(string)
    for i, (token_type, token_value) in enumerate(merged_splits):
        if token_type == '*':
            # Match any text up to the next token
            if i + 1 < len(merged_splits):
                next_token_type, next_token_value = merged_splits[i + 1]
                if next_token_type == '':
                    # Look for the next literal text
                    idx = string.find(next_token_value, index)
                    if idx == -1:
                        # Can't find the next literal text; match fails
                        matched_substring = string[index:]
                        result_tokens.append(
                            ('*', matched_substring, index, string_length - 1))
                        index = string_length
                        match = False
                        result_tokens.append(('', None, -1, -1))
                        break
                    else:
                        matched_substring = string[index:idx]
                        result_tokens.append(
                            ('*', matched_substring, index, idx - 1))
                        index = idx
                elif next_token_type == '~':
                    # Consume the rest of the string
                    matched_substring = string[index:]
                    result_tokens.append(
                        ('*', matched_substring, index, string_length - 1))
                    index = string_length
            else:
                # '*' at the end; consume the rest of the string
                matched_substring = string[index:]
                result_tokens.append(
                    ('*', matched_substring, index, string_length - 1))
                index = string_length
        elif token_type == '~':
            # Ensure that token_value is present anywhere in the string
            found_idx = string.find(token_value)
            if found_idx != -1:
                result_tokens.append(
                    ('~', token_value, found_idx, found_idx + len(token_value) - 1))
            else:
                match = False
                result_tokens.append(('~', None, -1, -1))
        elif token_type == '':
            literal_text = token_value
            if i == len(merged_splits) - 1:
                # Last token; literal text must be at the end
                if string.endswith(literal_text):
                    start_index = string_length - len(literal_text)
                    end_index = string_length - 1
                    result_tokens.append(
                        ('', literal_text, start_index, end_index))
                    index = string_length
                else:
                    match = False
                    result_tokens.append(('', None, -1, -1))
                    break
            else:
                # Match literal text at the current index
                if string.startswith(literal_text, index):
                    start_index = index
                    end_index = index + len(literal_text) - 1
                    result_tokens.append(
                        ('', literal_text, start_index, end_index))
                    index += len(literal_text)
                else:
                    match = False
                    result_tokens.append(('', None, -1, -1))
                    break

    return NegexResult(tokens=result_tokens, match=match)


def match(string: str, pattern: str) -> bool:
    result = parse(string, pattern)
    return result.match


def parse_multiple(strings: list[str], pattern: str):
    for string in strings:
        yield parse(string, pattern)


def match_multiple(strings: list[str], pattern: str):
    for string in strings:
        yield match(string, pattern)
