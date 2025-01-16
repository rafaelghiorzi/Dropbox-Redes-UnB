# Dropbox de rede interna

_Projeto da matéria redes de computadores, 2024.2 - UnB_

## Descrição do projeto

Esse projeto é uma aplicação do conteúdo ministrado na Disciplina de Redes de Computadores da [Universidade de Brasília](https://www.unb.br). O sistema aplica os conhecimentos a respeito de sockets, paradigma cliente e servidor e sistemas de redes em um projeto de *Dropbox de rede interna*.

## Tecnologias
O projeto faz uso principalmente das bibliotecas Sockets e SQLite3 do python para administração de usuários e upload e download de arquivos. Os sockets foram configurados para seguir o protocolo TCP de transporte, e as mensagens seguem o padrão de mensagens HTTP simplificadas. Na parte do cliente, foi desenvolvido, também em python, uma aplicação simples e interativa no terminal de comando do computador, em que o usuário navega pelas diferentes funcionalidades a partir de entradas numéricas no teclado.

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

*Observação: para realizar o upload de arquivos, basta copiar um arquivo no explorador do seu computador com o atalho Ctrl+Shift+C se estiver no Windows. Isso copiará o caminho do arquivo, que você pode então enviar para o servidor*.

## Licença

Este projeto não tem licença registrada. Sinta-se à vontade para usar, modificar e distribuir os arquivos da forma que quiser!
