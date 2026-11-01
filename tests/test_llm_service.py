from services.llm_service import LLMService


def test_generate_sends_user_message_and_returns_content(fake_nemo):
    service = LLMService("k", "m")

    assert service.generate("hi") == "reply:hi"

    client = fake_nemo.instances[0]
    assert client.api_key == "k"
    assert client.calls == [
        {"model": "m", "chat_context": [{"role": "user", "content": "hi"}]}
    ]


def test_generate_fallback_on_unexpected_response(fake_nemo):
    fake_nemo.response = {"unexpected": True}
    service = LLMService("k", "m")

    assert service.generate("hi") == str({"unexpected": True})


def test_generate_fallback_on_failed_request_payload(fake_nemo):
    # nemollm returns {"status": "fail", "msg": ...} when the HTTP call is not ok.
    fake_nemo.response = {"status": "fail", "msg": "rate limited"}
    service = LLMService("k", "m")

    assert service.generate("hi") == str({"status": "fail", "msg": "rate limited"})
