from datetime import datetime, timedelta

from .cache import britive


def test_fields():
    fields = britive.audit_logs.fields()
    assert isinstance(fields, dict)
    assert len(fields.keys()) == 18


def test_operators():
    operators = britive.audit_logs.operators()
    assert isinstance(operators, dict)
    assert len(operators.keys()) == 3


def test_query_json():
    events = britive.audit_logs.query(from_time=datetime.now() - timedelta(7), to_time=datetime.now())
    assert isinstance(events, list)
    assert isinstance(events[0], dict)
    assert len(events) % 100 != 0  # v2.8.1 - adding check due to pagination bug not including the last page


def test_query_csv():
    csv = britive.audit_logs.query(from_time=datetime.now() - timedelta(7), to_time=datetime.now(), csv=True)
    assert '"timestamp","actor.display_name"' in csv
