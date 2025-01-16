# Dropbox de rede interna

_Projeto da matéria redes de computadores, 2024.2 - UnB_

## Descrição do projeto

Este é um sistema distribuído que atua como um “dropbox” de rede interna, possibilitando colaboração e troca de arquivos de forma simples e direta.

## Como funciona

- O servidor integra um banco SQLite para cadastrar usuários, armazenar metadados de arquivos e gerenciar permissões.
- O cliente faz solicitações para o servidor (upload, download, listagem e remoção de arquivos), além de criação e remoção de usuários, por meio de requisições HTTP simplificadas que funcionam com a administração de sockets.

## O que faz

- Permite registrar, logar e deletar usuários.
- Realiza upload, download e deleção de arquivos, mostrando a lista de arquivos disponíveis na rede.
- Assista o [vídeo de demonstração do projeto](https://youtu.be/2H6uyJMo8C0) para entender melhor o funcionamento dele.

## Como rodar

1. Clone o repositório e instale as dependências necessárias.
2. No seu computador, abra o terminal e digite "ipconfig" ou "ifconfig" para encontrar o seu endereço IPv4, de rede local
3. Tenha garantido que ambos servidor e cliente estejam na mesma rede local
4. No servidor, execute:

```bash
python server.py
```

5. No cliente, execute:

```bash
python main.py
```

6. Aproveite!

## Licença

Este projeto não tem licença registrada. Sinta-se à vontade para usar, modificar e distribuir os arquivos da forma que quiser!
