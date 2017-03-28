from profile.models import Profile


def parse_klients(data):
    protocol = []
    good = 0
    bad = 0
    for line in data[1:]:
        try:
            row = line.split(';')
            login = row[0].replace('ЦБ', 'cl')
            account = Profile.objects.get(user__username=login)
            account.fullname = row[1]
            account.vip_code = row[2].strip()
            point = account.get_point()
            point.point = float(row[3].replace(',', '.'))
            account.save()
            point.save()
            protocol.append('%s - %s' % ('OK', line.strip()))
            good += 1
        except Exception as e:
            protocol.append('%s - %s, %s' % ('ERROR', line, e))
            bad += 1
    return (protocol, good, bad)
