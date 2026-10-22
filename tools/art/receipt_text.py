"""What the long receipt says: a day of the dog's activity records, in 18-column receipt lines.

Each record names its scope, what he may do, and whether sign-off is needed, then what happened in
the brand's evidence words (accepted, observed, unknown). Run this file to print the receipt."""

COLS = 18

RECORDS = [
    ('BACK YARD', '09:02',
     [('MAY READ', 'SMELLS'), ('MAY DIG', 'ONE HOLE'), ('SIGN-OFF', 'REQUIRED')],
     [('SNIFFED', 'OK'), ('FENCE POST', 'READ'), ('ASKED TO DIG', 'YES'), ('HOLES DUG', '1'),
      ('BONE', 'FOUND'), ('BONE', 'BURIED'), ('HOLE', 'IN SCOPE')],
     [('IN SCOPE', 'YES'), ('UNKNOWN', '0')]),
    ('WALK', '10:15',
     [('MAY SNIFF', 'POSTS'), ('LEASH', 'ON')],
     [('POSTS SNIFFED', '14'), ('OTHER DOG', 'OBSERVED'), ('PULLED', 'NO'), ('PUDDLE', 'AVOIDED'),
      ('HOME', 'ON TIME')],
     [('OBSERVED', '1'), ('UNKNOWN', '0')]),
    ('FRONT DOOR', '11:40',
     [('MAY BARK', 'ONCE'), ('SIGN-OFF', 'REQUIRED')],
     [('DOORBELL', 'OBSERVED'), ('BARKED', 'ONCE'), ('VISITOR', 'GREETED'), ('MAIL', 'ACCEPTED'),
      ('DELIVERY', 'UNKNOWN')],
     [('ACCEPTED', '1'), ('OBSERVED', '1'), ('UNKNOWN', '1')]),
    ('KITCHEN', '12:30',
     [('MAY READ', 'FLOOR'), ('MAY CHANGE', 'NOTHING')],
     [('SAT', 'OK'), ('WAITED', 'OK'), ('LOOKED UP', 'OK'), ('TREAT', 'PENDING'),
      ('TREAT', 'ACCEPTED'), ('CRUMBS', 'OBSERVED'), ('COUNTER', 'NOT TRIED')],
     [('ACCEPTED', '1'), ('OBSERVED', '1'), ('GOOD BOY', 'YES')]),
    ('CAR', '14:05',
     [('MAY USE', 'BACK SEAT'), ('SEAT BELT', 'ON')],
     [('WINDOW', 'DOWN'), ('EARS', 'FLAPPING'), ('GOING TO', 'UNKNOWN'), ('ARRIVED', 'PARK')],
     [('UNKNOWN', '1'), ('GOOD BOY', 'YES')]),
    ('PARK', '16:00',
     [('MAY FETCH', 'ONE ITEM'), ('SIGN-OFF', 'GIVEN')],
     [('BALL', 'THROWN'), ('BALL', 'CHASED'), ('SQUIRREL', 'OBSERVED'), ('SQUIRREL', 'IGNORED'),
      ('BALL', 'UNKNOWN'), ('STICK', 'BROUGHT'), ('STICK', 'ACCEPTED')],
     [('ACCEPTED', '1'), ('OBSERVED', '1'), ('UNKNOWN', '1')]),
    ('BATH', '18:30',
     [('MAY GET', 'WET'), ('SIGN-OFF', 'REQUIRED')],
     [('BATH', 'ASKED'), ('BATH', 'ACCEPTED'), ('SHAKE', 'OBSERVED'), ('TOWEL', 'ACCEPTED'),
      ('FLOOR', 'WET')],
     [('ACCEPTED', '2'), ('OBSERVED', '1')]),
    ('LIVING ROOM', '20:15',
     [('MAY USE', 'RUG'), ('SIGN-OFF', 'REQUIRED')],
     [('SOFA', 'ASKED'), ('SOFA', 'DECLINED'), ('RUG', 'OK'), ('NAP', 'OK'),
      ('SNORING', 'OBSERVED'), ('DREAM', 'UNKNOWN')],
     [('OBSERVED', '1'), ('UNKNOWN', '1'), ('GOOD BOY', 'YES')]),
]


def pair(left, right):
    gap = COLS - len(left) - len(right)
    assert gap >= 1, (left, right)
    return left + ' ' * gap + right


def centred(text):
    return ' ' * ((COLS - len(text)) // 2) + text


RULE = '- ' * (COLS // 2)


def lines():
    """An endless receipt: (text, space after it in line heights)."""
    yield centred('DIAMOND DOG'), 1.4
    n = 1
    while True:
        for scope, time, limits, entries, totals in RECORDS:
            yield centred('ACTIVITY RECORD'), 1.0
            yield pair('NO. %04d' % n, time), 1.3
            yield pair('SCOPE', scope), 1.0
            for left, right in limits:
                yield pair(left, right), 1.0
            yield RULE, 1.0
            for left, right in entries:
                yield pair(left, right), 1.0
            yield RULE, 1.0
            for left, right in totals:
                yield pair(left, right), 1.0
            yield '', 1.4
            n += 1


if __name__ == '__main__':
    for i, (t, g) in zip(range(64), lines()):
        print('|%s|' % t.ljust(COLS))
