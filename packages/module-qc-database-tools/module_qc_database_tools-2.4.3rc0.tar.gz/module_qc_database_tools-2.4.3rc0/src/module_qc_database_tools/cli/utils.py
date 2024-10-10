from __future__ import annotations

import itkdb


def get_itkdb_client(
    *, access_code1: str | None = None, access_code2: str | None = None
) -> itkdb.Client:
    """
    Create an itkdb client using access codes (if provided).

    Args:
        access_code1 (:obj:`str` or :obj:`None`): access code 1
        access_code2 (:obj:`str` or :obj:`None`): access code 2

    Returns:
        client (:obj:`itkdb.Client`): an itkdb client
    """
    if access_code1 and access_code2:
        user = itkdb.core.User(access_code1=access_code1, access_code2=access_code2)
        return itkdb.Client(user=user)
    return itkdb.Client()
