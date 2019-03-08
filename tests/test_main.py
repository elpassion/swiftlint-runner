
from slrunner.main import SLRunnerTest

def test_slrunner(tmp):
    with SLRunnerTest() as app:
        res = app.run()
        print(res)
        raise Exception

def test_command1(tmp):
    argv = ['command1']
    with SLRunnerTest(argv=argv) as app:
        app.run()
