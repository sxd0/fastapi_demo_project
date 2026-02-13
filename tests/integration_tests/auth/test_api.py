

import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("k0t@pes.com", "1234", 200),
    ("k0t1@pes.com", "1235", 200),
])
async def test_auth_flow(email: str, password: str, status_code: int, ac):
    resp_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert resp_register.status_code == status_code


    resp_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert resp_login.status_code == status_code
    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()
    

    resp_me = await ac.post("/auth/me")
    assert resp_me.status_code == status_code
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user


    resp_logout = await ac.post("/auth/logout")
    assert resp_logout.status_code == status_code

    assert "access_token" not in ac.cookies
