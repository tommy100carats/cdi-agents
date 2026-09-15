from datetime import date

from pipeline.precedence import advance, classify_email, relance_after


def test_status_never_goes_backwards():
    s, changed, _ = advance("Entretien", "accuse_reception")
    assert s == "Entretien" and not changed


def test_rejection_closes_from_any_status():
    for cur in ["À contacter", "Candidature envoyée", "Entretien", "Test / Étude de cas", "En veille"]:
        s, changed, _ = advance(cur, "refus")
        assert s == "Refusé / Clos" and changed


def test_doubt_blocks_progression():
    s, changed, why = advance("Candidature envoyée", "entretien_confirme", doubt=True)
    assert s == "Candidature envoyée" and not changed and "doute" in why


def test_slot_proposed_does_not_move_status():
    s, changed, _ = advance("Candidature envoyée", "creneau_propose")
    assert s == "Candidature envoyée" and not changed


def test_closed_file_never_reopens_automatically():
    s, changed, _ = advance("Refusé / Clos", "entretien_confirme")
    assert s == "Refusé / Clos" and not changed


def test_classify_rejection_fr_en():
    assert classify_email("Votre candidature", "Nous ne donnerons pas suite à votre candidature.").event == "refus"
    assert classify_email("Update", "Unfortunately we will not be moving forward.").event == "refus"


def test_classify_ack_is_not_first_reply():
    c = classify_email("Thank you for applying", "We received your application and will review it.")
    assert c.event == "accuse_reception" and not c.needs_review


def test_classify_confirmed_interview_needs_datetime():
    c = classify_email("Dust Interview Confirmation", "You have been scheduled: Tuesday, September 8, 2026 3:30 PM meet.google.com/abc")
    assert c.event == "entretien_confirme" and not c.needs_review
    c2 = classify_email("Interview with Dust", "We'd love to schedule a call, please book a slot on calendly")
    assert c2.event == "creneau_propose"


def test_unknown_needs_review():
    assert classify_email("Hello", "Just checking in about something else").needs_review


def test_relance_delays():
    d = date(2026, 9, 7)
    assert relance_after("accuse_reception", d) == date(2026, 9, 17)
    assert relance_after("entretien_confirme", d) == date(2026, 9, 9)
    assert relance_after("refus", d) is None
    assert relance_after("accuse_reception", d, doubt=True) is None


def test_confirmation_linkedin_vaut_accuse():
    # Incident du 14/09/2026 (Creality)
    from pipeline.precedence import classify_email
    c = classify_email("Tom, votre candidature a été envoyée à Creality", "Votre candidature a été envoyée à Creality.")
    assert c.event == "accuse_reception" and not c.needs_review
