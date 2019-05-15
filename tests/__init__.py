SOURCE = ".test_cork"
SOURCE_SPECFILE = "{}.spec".format(SOURCE)


CORKFILE_KWARGS = {
    "force": False,
    "browser": "browsh",
    "app": "app",
    "starting_port": 5000,
    "teardown_route": "teardown",
    "teardown_function": "teardown"
}
