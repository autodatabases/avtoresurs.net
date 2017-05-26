from profile.models import Profile


def parse_clients(data):
    """ parse file from media and update profile info
     :arg data is splitted lines from file """
    protocol = []
    good = 0
    bad = 0
    for line in data[1:]:
        try:
            row = line.split(';')
            login = row[0].replace('ЦБ', 'cl')
            profile = Profile.objects.get(user__username=login)
            profile.fullname = row[1]
            profile.vip_code = row[2].strip()
            profile.points = float(row[3].replace(',', '.'))
            profile.save()

            protocol.append('%s - %s' % ('OK', line.strip()))
            good += 1
        except Exception as e:
            protocol.append('%s - %s, %s' % ('ERROR', line, e))
            bad += 1
    return protocol, good, bad
