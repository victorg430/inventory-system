from unittest.mock import patch, Mock
import cli


@patch("cli.requests.get")
def test_view_all(mock_get, capsys):
    mock_get.return_value = Mock(json=lambda: [{"id": 1, "product_name": "Almond Milk"}])
    cli.view_all()
    out = capsys.readouterr().out
    assert "Almond Milk" in out


@patch("cli.requests.get")
def test_view_one_not_found(mock_get, capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "999")
    mock_get.return_value = Mock(status_code=404)
    cli.view_one()
    assert "not found" in capsys.readouterr().out.lower()


@patch("cli.requests.post")
def test_add_item(mock_post, monkeypatch, capsys):
    inputs = iter(["Oat Milk", "Oatly", "4.5", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    mock_post.return_value = Mock(json=lambda: {"id": 2, "product_name": "Oat Milk"})
    cli.add_item()
    mock_post.assert_called_once()
    assert "Oat Milk" in capsys.readouterr().out


@patch("cli.requests.patch")
def test_update_item(mock_patch, monkeypatch):
    inputs = iter(["1", "price", "5.99"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    mock_patch.return_value = Mock(status_code=200, json=lambda: {"id": 1, "price": 5.99})
    cli.update_item()
    mock_patch.assert_called_once_with(f"{cli.API}/1", json={"price": 5.99})


@patch("cli.requests.delete")
def test_delete_item(mock_delete, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    mock_delete.return_value = Mock(json=lambda: {"message": "Item 1 deleted"})
    cli.delete_item()
    assert "deleted" in capsys.readouterr().out.lower()


@patch("cli.requests.get")
def test_find_on_api_by_barcode(mock_get, monkeypatch, capsys):
    inputs = iter(["123", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    mock_get.return_value = Mock(status_code=200, json=lambda: {"product_name": "Oat Milk"})
    cli.find_on_api()
    assert "Oat Milk" in capsys.readouterr().out