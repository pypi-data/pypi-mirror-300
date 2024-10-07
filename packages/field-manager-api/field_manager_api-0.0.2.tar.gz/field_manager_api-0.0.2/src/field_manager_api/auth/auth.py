def set_bearer_token_header(token: str) -> None:
    """
    Set the Authorization header with the Bearer token.
    """
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def get_token_from_credentials(username: str, password: str) -> str:
    """
    Get the token from the credentials.
    """
    return
