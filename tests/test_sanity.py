import pytest


@pytest.fixture
def request_singleton():
    from software_patterns import Singleton

    from cookiecutter_python.backend.request import Request

    class RequestSingleton(Request, metaclass=Singleton):
        # use new to allow modification of singleton attributes with constructor call
        def __new__(cls, *args, **kwargs):
            print('\n NEW:', kwargs)
            # x = super().__new__(cls, **kwargs)
            x = super().__new__(cls)
            assert 'config_file' in dir(x)
            with pytest.raises(AttributeError):
                x.config_file
            assert getattr(x, 'config_file', None) is None
            return x

        # if only below constructor is implemented:
        # the metaclass gurantees below will ever be called only once
        # thus modification of singleton isntance attributes is not possible with constructor
        def __init__(self, *args, **kwargs):
            assert 'config_file' in dir(self)
            with pytest.raises(AttributeError):
                self.config_file
            print('\n INIT:', kwargs)
            super().__init__(*args, **kwargs)
            assert self.config_file in {'CF1', 'CF2', 'CF3'}

    return RequestSingleton


def test_req_singleton_sanity_check(request_singleton):
    # WHEN we invoke the Singleton Constructor once
    req1 = request_singleton(
        config_file='CF1',
        default_config=True,
        web_servers=['pypi', 'readthedocs'],
        no_input=False,
        extra_context={'extra_context': 'extra_context'},
    )
    # AND WHEN we invoke the Singleton Constructor again
    req2 = request_singleton(
        config_file='CF2',
    )
    # THEN both refs point to the same object: Constructor returns same instance
    assert req1 is req2
    assert req1.default_config is True
    # AND Constructor logic instantiates object only ONCE: only called once
    assert req1.config_file == 'CF1'
    assert req2.config_file == 'CF1'

    # AND WHEN we modify the Singleton instance
    req2.config_file = 'CF3'

    # THEN the Singleton instance should have been modified
    assert req1.config_file == 'CF3'
    assert req2.config_file == 'CF3'


def test_track_poc(request_singleton):
    req1 = request_singleton(
        config_file='CF1',
        default_config=True,
        web_servers=['pypi', 'readthedocs'],
        no_input=False,
        extra_context={'extra_context': 'extra_context'},
    )
    tracking_req_reg = request_singleton()

    # modify req
    req1.config_file = 'CF2'

    # assert tracking_req_reg.config_file == 'CF2'
    assert tracking_req_reg.config_file == 'CF2' == req1.config_file
