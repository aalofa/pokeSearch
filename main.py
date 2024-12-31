import eel

eel.init("app")

@eel.expose
def test():
    print('test() called')
    return 'test() called'

eel.start('../index.html')