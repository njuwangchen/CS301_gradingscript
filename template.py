import sys
import StringIO
import inspect
import re

# in case someone forgets to import...
import random
import math

def has_doc(method):
    return len(method.__doc__) > 0

def source_code_match(method, condition):
    return condition(inspect.getsource(method))

def feed_data_from_stdin(method, args, data, times=1):
    sys.stdin = StringIO.StringIO(data * times)
    try:
        method(*args)
    except:
        pass
    sys.stdin = sys.__stdin__

def idle():
    pass

def check_output(actual, expected):
    actual, expected = actual.strip.replace(' ', ''), expected.strip.replace(' ', '')
    return actual == expected

def test(debug=True):
    tot_score = 0.
    stdout_ = sys.stdout
    stream = StringIO.StringIO()
    sys.stdout = stream
    for test_item in test_data:
        desc = ''
        if len(test_item) == 5:
            method, ituple, ostr, retval, score = test_item
        elif len(test_item) == 6:
            method, ituple, ostr, retval, score, desc = test_item
        else:
            continue
        try:
            ret = None
            ret = method(*ituple)
            if ostr:
                if re.search(ostr.lower(), stream.getvalue().strip().lower()):# == ostr:
                    tot_score += score
            else:
                if ret == retval:
                    tot_score += score
        except Exception as e:
            print e
        if debug:
            sys.stdout = stdout_
            if ostr:
                if re.search(ostr.lower(), stream.getvalue().strip().lower()) is None:# != ostr:
                    print >> sys.stderr, '------------------------'
                    print >> sys.stderr, test_item
                    print >> sys.stderr, 'student output:\n', stream.getvalue().strip()
                    print >> sys.stderr, 'expected output:\n', ostr
                    if desc:
                        print >> sys.stderr, 'reason:\n', desc
            else:
                if ret != retval:
                    print >> sys.stderr, '------------------------'
                    print >> sys.stderr, test_item
                    print >> sys.stderr, 'student return:\n', ret
                    print >> sys.stderr, 'expected return:\n', retval
                    if desc:
                        print >> sys.stderr, 'reason:\n', desc
            sys.stdout = stream
        stream.truncate(0)
    sys.stdout = stdout_
    print '------------------------'
    print "Final score: "
    print tot_score
