
import pytest
import responses

import ropeclient as rc
rc.auth_token = 'fc691de5178f41f939bcb0f649002c17fb009dae'

@pytest.mark.realserver
def test_get_bot():
    """
    Test that the Works server returns a real Flight when one is requested.
    :return:
    """

    resp = rc.Bot.retrieve(1)
    assert type(resp) is dict
    print(resp)
    assert resp['id'] == 1


@pytest.mark.realserver
def test_post_record():
    """
    Test that the Works server returns a real Flight when one is requested.
    :return:
    """
    import os
    img_path = os.path.expanduser('~/rope/test_data/img.jpg')
    with open(img_path, 'rb') as img_bytes:
        files = {'jpg': img_bytes.read()}
        data = {'bot': 1,
                'time': 123,
                'user_throttle': .123,
                'user_steering': .444
                }

        resp = rc.Record.create(data=data, files=files)
        assert type(resp) is dict
        print(resp)
        assert 'id' in resp.keys()