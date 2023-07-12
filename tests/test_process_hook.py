from payload_example.full_payload_example import full_payload


def test_send_payload_to_webhook(client) -> None:
    response = client.post('/payload', json=full_payload)
    assert response.status_code == 200
