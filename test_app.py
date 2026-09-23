from unittest.mock import MagicMock, patch

import app as app_module


def test_health_returns_healthy_when_mongodb_responds():
    fake_client = MagicMock()
    fake_client.admin.command.return_value = {"ok": 1}

    with patch.object(app_module, "client", fake_client):
        response = app_module.app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy",
        "database": "connected"
    }


def test_health_returns_unhealthy_when_mongodb_is_unavailable():
    fake_client = MagicMock()
    fake_client.admin.command.side_effect = Exception("MongoDB unavailable")

    with patch.object(app_module, "client", fake_client):
        response = app_module.app.test_client().get("/health")

    assert response.status_code == 503
    assert response.get_json() == {
        "status": "unhealthy",
        "database": "disconnected"
    }