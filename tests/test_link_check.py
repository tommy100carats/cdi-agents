import json

from pipeline.link_check import check


def fake_fetch_factory(responses):
    def fetch(url, timeout=12):
        for k, v in responses.items():
            if k in url:
                return v
        return 200, "<html>" + "x" * 1000 + "</html>"
    return fetch


def test_ashby_id_present_and_absent():
    board = json.dumps({"jobs": [{"id": "35d21c5b-907d-4be4-a7fb-6e7bf85d4dbc"}]})
    fetch = fake_fetch_factory({"api.ashbyhq.com/posting-api/job-board/dust": (200, board)})
    ok = check("https://jobs.ashbyhq.com/dust/35d21c5b-907d-4be4-a7fb-6e7bf85d4dbc", fetch=fetch)
    assert ok["active"] is True and ok["method"] == "ashby"
    ko = check("https://jobs.ashbyhq.com/dust/00000000-0000-0000-0000-000000000000", fetch=fetch)
    assert ko["active"] is False


def test_greenhouse_and_lever():
    gh = json.dumps({"jobs": [{"id": 8592025002}]})
    lv = json.dumps([{"id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"}])
    fetch = fake_fetch_factory({"boards-api.greenhouse.io/v1/boards/gympass": (200, gh), "api.lever.co/v0/postings/brevo": (200, lv)})
    assert check("https://job-boards.greenhouse.io/gympass/jobs/8592025002", fetch=fetch)["active"] is True
    assert check("https://jobs.lever.co/brevo/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", fetch=fetch)["active"] is True
    assert check("https://jobs.lever.co/brevo/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", fetch=fetch)["active"] is False


def test_unverifiable_hosts_are_never_active():
    r = check("https://www.linkedin.com/jobs/view/123", fetch=lambda u, timeout=12: (200, "x" * 5000))
    assert r["active"] is None and r["method"] == "unverifiable"
    r = check("https://www.welcometothejungle.com/fr/companies/x/jobs/y", fetch=lambda u, timeout=12: (200, "x" * 5000))
    assert r["active"] is None


def test_http_404_and_dead_pattern():
    assert check("https://acme.com/jobs/1", fetch=lambda u, timeout=12: (404, ""))["active"] is False
    page = "<html>" + "x" * 800 + " Cette offre n'est plus disponible </html>"
    assert check("https://acme.com/jobs/2", fetch=lambda u, timeout=12: (200, page))["active"] is False


def test_empty_page_is_unknown_not_active():
    assert check("https://acme.com/jobs/3", fetch=lambda u, timeout=12: (200, "<html></html>"))["active"] is None


def test_api_down_is_unknown():
    r = check("https://jobs.ashbyhq.com/dust/35d21c5b-907d-4be4-a7fb-6e7bf85d4dbc", fetch=lambda u, timeout=12: (503, ""))
    assert r["active"] is None


def test_truncated_board_json_still_finds_id():
    # Incident du 07/09/2026 : réponse Ashby tronquée → JSON illisible → None pour toute offre Ashby
    a = "35d21c5b-907d-4be4-a7fb-6e7bf85d4dbc"; z = "00000000-0000-0000-0000-000000000000"
    body = '{"jobs":[{"id":"' + a + '","title":"RevOps"},{"id":"def-4'  # coupé
    r = check(f"https://jobs.ashbyhq.com/dust/{a}", fetch=lambda u, timeout=12: (200, body))
    assert r["active"] is True
    r2 = check(f"https://jobs.ashbyhq.com/dust/{z}", fetch=lambda u, timeout=12: (200, body))
    assert r2["active"] is None
