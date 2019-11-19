from flask import Flask, request, session
import app

app.secret_key = "asdu90vdaf87v932hiurhyuasdfoysad8uf7t3g2"


def test_up(client):
    client.get("/")
    assert client.get("/").status_code == 200
    assert b'<form method="POST" action="/guessnum">' in client.get("/").data

    test = client.post("/guessnum", data={"guessed": "-1"})
    assert request.method == "POST"
    assert b"Too Low" in test.data

    test = client.post("/guessnum", data={"guessed": "1001"})
    assert request.method == "POST"
    assert b"Too High" in test.data

    test = client.post("/guessnum", data={"guessed": session["randomNum"]})
    assert request.method == "POST"
    assert session["randomNum"] == session["randomNum"]
    assert b"Congratulations" in test.data
    # assert client.get("/guessnum").status_code == 200

    test = client.post("/nameentered", data={"name": "qazwsxedc"})
    assert b'<a href = "/"><button class="button">New Game</button></a>' in test.data

    test = client.get("/displayscores")
    assert b"<th> Place </th>" in test.data
