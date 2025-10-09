from collections import Counter


def _setup(s1, s2):
    """Handles input validation and initial setup."""
    if s1 is None or s2 is None:
        raise ValueError("Inputs cannot be None.")
    if not s2:
        raise ValueError("Pattern cannot be empty.")

    n, m = len(s1), len(s2)
    if n < m:
        raise ValueError("Pattern length cannot exceed string length.")

    pat_freq = Counter(s2)
    pat_chars = set(pat_freq.keys())
    return n, m, pat_freq, pat_chars


def _find_jump(win, pat_chars):
    """Finds the distance to jump forward based on a 'bad' character."""
    for j in range(len(win) - 1, -1, -1):
        if win[j] not in pat_chars:
            return j + 1
    return 0


def _slide(s1, i, n, m, pat_freq, pat_chars):
    """Slides through a dense region of valid characters, counting matches."""
    count = 0
    win_freq = Counter(s1[i: i + m])

    while True:
        if win_freq == pat_freq:
            count += 1

        i += 1
        if i + m > n or s1[i + m - 1] not in pat_chars:
            return count, i

        new_char = s1[i + m - 1]
        old_char = s1[i - 1]

        win_freq[new_char] += 1
        win_freq[old_char] -= 1
        if win_freq[old_char] == 0:
            del win_freq[old_char]
 

def countPermStr(s1, s2):
    n, m, pat_freq, pat_chars = _setup(s1, s2)
    if n is None:
        return 0

    i = 0
    count = 0
    while i <= n - m:
        win = s1[i: i + m]
        jump = _find_jump(win, pat_chars)

        if jump > 0:
            i += jump
        else:
            block_matches, next_i = _slide(s1, i, n, m, pat_freq, pat_chars)
            count += block_matches
            i = next_i

    return count


if __name__ == "__main__":
    print(countPermStr("abab", "ab"))
    print(countPermStr("aaabaaa", "aaa"))
    print(countPermStr("ababa", "aba"))
    print(countPermStr("aabacabaa", "aab"))
    print(countPermStr("zzzyxwzzyx", "xyz"))
    print(countPermStr("", "a"))
    print(countPermStr("ab", "abc"))
    print(countPermStr("aAbB", "ab"))
    print(countPermStr("abAB", "AB"))
    print(countPermStr("a1b$c_a$b1", "$1b"))
    print(countPermStr("  ", " "))
    print(countPermStr("a" * 200_000, "a" * 10_000))
