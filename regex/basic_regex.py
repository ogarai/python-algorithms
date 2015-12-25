#!/usr/bin/env python

"""
This is a basic regex checker.

===SPECIFICATIONS===
'*' matches 0 or more characters
'+' matches 1 or more characters
'?' matches exactly one character

===IMPLEMENTATION SUMMARY===
The regex check is performed by the 'match' method.
It returns True or False depending on whether a match exists.

Running this script executes all tests.
The tests are generated from the 'TESTS' list.

===ALGORITHM STRATEGY===
STEP 0: First split the regex by the first wildcard.
STEP 1: Find the substring on the left of the wildcard.
STEP 2: If found, then make a recursive call to match the
        part to the right of the wildcard, forming a new
        challenge with all characters after the last character
        of the left substring.
STEP 3: If the right side matches, set result to True. Otherwise,
        find  the next occurrence of the left substring and
        go back to STEP 2.
        The loop continues until the entire text is traversed.

"""

__author__ = 'Orko Garai (orko.garai@gmail.com)'

import warnings
warnings.filterwarnings("ignore")

import timeit
import sys

WILDCARDS = ['*', '+', '?']

TESTS = [
        ## Format: [regex, challenge, result]

        ['*', 'a', True],
        ['*', '', True],
        ['+', 'a', True],
        ['+', '', False],
        ['?', 'a', True],
        ['?', '', False],
        ['a*d', 'abcd', True],
        ['a*d', 'ad', True],
        ['a+d', 'ad', False],
        ['a*d', 'abcde', True],
        ['a*d', 'babcd', True],
        ['a?c', 'abcd', True],
        ['a?d', 'abd', True],
        ['a?d', 'ad', False],
        ['a*', 'abcd', True],
        ['*b', 'abcd', True],
        ['+b', 'abcd', True],
        ['?b', 'abcd', True],
        ['a*', 'fff', False],
        ['a+', 'fff', False],
        ['a?', 'fff', False],
        ['a*d', 'abc', False],
        ['a?d', 'abcd', False],
        ['a?d', 'abcd', False],
        ['a*b*d', 'abcde', True],
        ['lmno*stu', 'abcdefghijklmnopqrstuvwxyz', True],
        ['lmno*stu*', 'abcdefghijklmnopqrstuvwxyz', True],
        ['*lmno*stu*', 'abcdefghijklmnopqrstuvwxyz', True],
        ['*lmno*stu*', 'lmnoabcdefghijklmnopqrstuvwxyz', True],
        ['*lmno+stu*', 'abcdefghijklmnopqrstuvwxyz', True],
        ['a+', 'abcd', True],
        ['a?', 'abcd', True],
        ['a*b*d+', 'abcde', True],
        ['*lmno*stu+', 'abcdefghijklmnopqrstuvwxyz', True],
        ['*lmno*stu?', 'abcdefghijklmnopqrstuv', True],
        ['*a', 'fff', False],
        ['+a', 'fff', False],
        ['?a', 'fff', False],
        ['*lmno?stu*', 'abcdefghijklmnopqrstuvwxyz', False],
        ['*lmno*stu+', 'abcdefghijklmnopqrstu', False],
        ['*lmno*stu?', 'abcdefghijklmnopqrstu', False],
        ['*b', 'fff', False],
        ['a?b', 'abbcd', True],
        ['a?b*d', 'abbcd', True],
        ['a+b*d', 'abbcd', True],
        ['a?d', 'abcad', False],
        ['abc?d', 'abc', False],
        ['abc?d', 'abcabc', False],
        ['*lmno*stu*', 'lmnoabcdefghijklmnopqrvwxyz', False],
    ]


class SplitRegexByLeftMostWildCard:
    """
    Splits a string by wildcard
    """
    def __init__(self, regex):
        self.left = None
        self.right = None
        self.wildcard = None
        pos = 0
        for ch in regex:
            if ch in WILDCARDS:
                self.wildcard = ch
                self.left = regex[0:pos]
                if pos < (len(regex) - 1):
                    self.right = regex[pos + 1:]
                break
            pos += 1
        else:
            self.left = regex

    def __str__(self):
        return ("left: %s, wildcard: %s, right: %s" % (self.left, self.wildcard, self.right))

# This variable is used to set the result of match, as we are calling the match method inside
# timeit and then accumulating the results
result = False

indentation=''

def log(txt):
    print indentation + txt

def match(regex, challenge, match_first_pos_only=False):
    """
    Checks if a match exists.
    Sets the result in the global 'result' variable.
    Logs the status to the console, with the indentation level indicating the
    recursion depth.

    @param regex: The regular expression
    @param challenge: The text in which the expression is expected to match
    @param match_first_pos_only: If True, indicates this is a recursive call from
                                 the right hand side of a '?' wildcard
    @return: Either the result or the position in the case of a plain substring match

    """

    global indentation
    indentation = '%(indentation)s    ' % globals()
    try:
        # source the global result var
        global result

        split_regex = SplitRegexByLeftMostWildCard(regex)
        log( 'Split Regex: ' + str(split_regex))
        log( 'Challenge: ' + challenge)
        log( 'Match First Position Only: %s' % match_first_pos_only)


        if split_regex.wildcard:
            while True:
                find_next_left_match = False
                log( "Searching for '%s' ..." % split_regex.left)
                left_match_start = match(split_regex.left, challenge) if split_regex.left else 0
                if (left_match_start is not 0) and (not left_match_start):
                    log( "'%s' not found!" % split_regex.left)
                    result = False
                    return False
                log( ("'%s' found ! start position: %s" % (split_regex.left, left_match_start)))
                if (match_first_pos_only) and (left_match_start < 1):
                    log( "Matched less than one character before '%s'! Need to look for more" % split_regex.left)
                    match_first_pos_only = False      # Re-allow multiple iteration from the next iteration
                    find_next_left_match = True
                elif (match_first_pos_only) and (left_match_start > 1):
                    log( "Matched more than one character before '%s'! No match!!" % split_regex.left)
                    result = False
                    return False
                else:
                    if split_regex.right:
                        log( 'Finding right side match: %s' % split_regex.right)
                        if split_regex.wildcard == '*':
                            right_challenge_start = left_match_start + len(split_regex.left)
                        elif split_regex.wildcard == '+' or split_regex.wildcard == '?':
                            right_challenge_start = left_match_start + len(split_regex.left) + 1
                        if (right_challenge_start >= len(challenge)):
                            log( 'Not enough characters left to form right side challenge')
                            result = False
                            return False
                        if (split_regex.wildcard == '?'):
                            # Should iterate only once because it should match only one character
                            match(split_regex.right, challenge[right_challenge_start:], match_first_pos_only=True)
                        else:
                            match(split_regex.right, challenge[right_challenge_start:])
                        if result is True:
                            log( 'Right side match found !')
                            return True
                        else:
                            log( "Right side match not found. Need to look for the next '%s' match" % split_regex.left)
                            find_next_left_match = True
                    else:
                        # This means the regex ends in the wildcard
                        if split_regex.wildcard == '*':
                            # Since the left side matched no need to check further as * matches 0 or more
                            result = True
                            return True
                        elif split_regex.wildcard == '+' or split_regex.wildcard == '?':
                            # the challenge should have at least one more character after left sequence
                            if (left_match_start + len(split_regex.left)) >= len(challenge):
                                result = False
                                return False
                            else:
                                result = True
                                return True
                    if find_next_left_match:
                        if not split_regex.left:
                            log( "Regex starts with wildcard and right side doesn't match")
                            result = False
                            return False
                        new_challenge_start = (left_match_start + len(split_regex.left))
                        if new_challenge_start >= len(challenge):
                            # In theory, we should never get here, so test coverage won't show this as executed
                            log("Not enough characters in challenge to look for next '%s'" % split_regex.left)
                            result = False
                            return False
                        challenge = challenge[new_challenge_start:]
                        log( 'Finding next left match for new challenge: ' + challenge)
        else:
            # Base case where we should simply find if the string is a substring of another
            for i in xrange(len(challenge)):
                end_pos = i + len(split_regex.left)
                if end_pos > len(challenge):
                    result = False
                    return False
                if challenge[i : end_pos] == split_regex.left:
                    result = True
                    return i
                if match_first_pos_only:
                    result = False
                    return False
            result = False
            return False
    finally:
        indentation = indentation[4:]



item = None

def test():
    global item
    num_passed = 0
    num_failed = 0
    for item in TESTS:
        print '-----------------------------------------------------------'
        print 'Starting Test: %s' % item
        print
        time = timeit.timeit(
                'match(item[0], item[1])',
                setup="from __main__ import *",
                number=1)
        if result is item[2]:
            verdict = '\033[102m' + "PASS" + '\033[0m'
            num_passed += 1
        else:
            verdict = '\033[101m' + "FAIL" + '\033[0m'
            num_failed += 1
        print
        print 'Test: %s\nResult: %s\nTime Taken: %s' % (item, verdict, time)
        print

    print '-----------------------------------------------------------'
    if num_failed:
        msg = '\033[91m' + "Failures encountered!!"
    else:
        msg = '\033[92m' + "Success!!"
    print '\033[1m%s Test Score: %s/%s\033[0m' % (
            msg, num_passed, num_passed+num_failed)
    print


if __name__ == "__main__":
    test()
