"""
Teste de aceitação: valida o fluxo completo do ponto de vista do usuário final,
através da API HTTP (sem acessar diretamente models ou services).

Cenário: um bibliotecário cadastra um livro e um usuário, realiza um empréstimo
e depois processa a devolução, esperando que o sistema se comporte corretamente
do início ao fim (nível funcional).
"""


def test_fluxo_completo_de_emprestimo_e_devolucao(client):
    # 1. Cadastra um livro
    resposta_livro = client.post(
        "/livros/",
        json={
            "titulo": "O Programador Pragmático",
            "autor": "David Thomas",
            "isbn": "978-0135957059",
            "quantidade_total": 1,
        },
    )
    assert resposta_livro.status_code == 201
    livro_id = resposta_livro.json()["id"]

    # 2. Cadastra um usuário
    resposta_usuario = client.post(
        "/usuarios/",
        json={"nome": "Mariana Souza", "email": "mariana@example.com"},
    )
    assert resposta_usuario.status_code == 201
    usuario_id = resposta_usuario.json()["id"]

    # 3. Realiza o empréstimo
    resposta_emprestimo = client.post(
        "/emprestimos/",
        json={"livro_id": livro_id, "usuario_id": usuario_id},
    )
    assert resposta_emprestimo.status_code == 201
    emprestimo_id = resposta_emprestimo.json()["id"]
    assert resposta_emprestimo.json()["devolvido"] is False

    # 4. Verifica que o livro não está mais disponível para novo empréstimo
    resposta_livro_atualizado = client.get(f"/livros/{livro_id}")
    assert resposta_livro_atualizado.json()["quantidade_disponivel"] == 0

    resposta_segundo_emprestimo = client.post(
        "/emprestimos/",
        json={"livro_id": livro_id, "usuario_id": usuario_id},
    )
    assert resposta_segundo_emprestimo.status_code == 400

    # 5. Realiza a devolução
    resposta_devolucao = client.patch(f"/emprestimos/{emprestimo_id}/devolver")
    assert resposta_devolucao.status_code == 200
    assert resposta_devolucao.json()["devolvido"] is True

    # 6. Verifica que o livro voltou a ficar disponível
    resposta_livro_final = client.get(f"/livros/{livro_id}")
    assert resposta_livro_final.json()["quantidade_disponivel"] == 1


def test_health_check_da_aplicacao(client):
    """Teste de aceitação não funcional: verifica disponibilidade básica do serviço."""
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"
