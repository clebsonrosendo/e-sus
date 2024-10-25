# Implementação do E-sus com Docker
<hr>

Esse tutorial é baseado no repo do [Flávio Souza](https://github.com/FlavioSouzaSantos/eSUS-Docker). Duas imagens são criadas, uma de banco de dados e a outra do servidor. Em cada pasta desse repo está os arquivos **Dockerfile**. Se você ainda não possui o Docker na sua máquina acesse o [site oficial](https://docs.docker.com/engine/install/) ou siga algum tutorial de instalação.

A imagem do banco de dados é baseada no PostgreSQL 9.6.13-alpine. Para construir a imagem cesse a pasta **database** e faça a build rodando o comando:

```sudo docker build -t esus_database:1.0 .```

> Lembre-se que no final do comando precisa conter um ponto (.)

Para criar a imagem do webserver, como o próprio Flávio especifica, o sitema precisa do *systemd*, um gerenciador de sistemas e serviços para o sistema operacional Linux. Por isso, a imagem criada tem como base a imagem do [**centos/systemd**](https://hub.docker.com/r/centos/systemd/). O processo é semelhante ao anterior, acesse a pasta **webserver** e rode o comando:

```sudo docker build -t esus_webserver:1.0 .```


> Lembre-se que no final do comando precisa conter um ponto (.)

Os arquivos **Dockerfile** presente nas pastas são instruções para o Docker
montar as imagens. Se você quer tem dúvida ou quer aprender mais acesse a [documentação de referência](https://docs.docker.com/reference/dockerfile/).

