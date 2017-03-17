# import threading
#
# def test():
#     i = 1
#     while True:
#         i += 1
#         print(i)
#
# thread = threading.Thread(target=test, args=())
# thread.daemon = True
# thread.start()


# thread.join()


# s1 = 'test'
# s2 = 'test'
#
# if s1 == s2:
#     print(True)
# else:
#     print(False)

def makebold(fn):
    def wrapped():
        return "<b>" + fn() + "</b>"

    return wrapped


def makeitalic(fn):
    def wrapped():
        return "<i>" + fn() + "</i>"

    return wrapped


@makebold
@makeitalic
def hello():
    return "hello habr"


print(hello())  ## выведет <b><i>hello habr</i></b>