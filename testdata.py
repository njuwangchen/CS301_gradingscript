# [ method, inputs, expected_output, expected_return, scores ]
test_data = [
    [reverse, ["abcdefg"], None, "gfedcba", 1.0, "Reverse Function didn't return the expected value"],
    [flip_vowel_case, ["OMG this is the worst"], None, "oMG thIs Is thE wOrst", 1.0, "Flip not correct"],
    [count_words, ["hello world"], None, 2, 1.0, "Normal case count not correct"],
    [count_words, ["   whoa this-is tricksy   "], None, 3, 1.0, "non-standard spacing not correct"],
    [equals, ['Hello World', 'Hi Word', 'eilo'], None, True, 1.0, "with ignore, equals not correct"],
    [equals, ['hello world', 'Hello World', ''], None, False, 1.0, "without ignore, equals not correct"],
    [source_code_match, [main, lambda s: "reverse(" in s or "count_words(" in s], None, True, 1.0, "main not calling other functions"],
    [feed_data_from_stdin, [main, [], "1\n'abc'\n5\n"], r'.*Reverse*', None, 1.0, "main menu display not correct"],
    [feed_data_from_stdin, [main, [], "'asdf'"], r'.*valid*', None, 1.0, "main not handle invalid option"],
    [has_doc, [main], None, True, 1.0, "No doc string"]
]

