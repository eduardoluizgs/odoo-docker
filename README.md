# Odoo 15 - Docker Development

Este repositório possui uma estrutura `Docker` para desenvolvimento e degub com o `VSCode`.

Este projeto é baseado no [Odoo](https://www.odoo.com/pt_BR).

![Odoo Logo](https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo.png?a=b)

![Odoo Image](https://odoocdn.com/openerp_website/static/src/img/2020/home/screens-mockup.png)

## Introdução

### O que é o `Odoo`?

Odoo é uma solução de gestão empresarial `ERP` completo, com um sistema `CRM` integrado. É baseado na arquitetura `MVC` e implementa um cliente (`javascript`) e um servidor (`python`), sendo a comunicação entre o cliente e o servidor por interface `XML-RPC` ou `JSON`. O Software é open source e disponível sob a GNU General Public License ([Wikipédia](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjptvip19D6AhWmRLgEHVhPBDEQmhN6BAhaEAI&url=https%3A%2F%2Fpt.wikipedia.org%2Fwiki%2FOdoo&usg=AOvVaw2UJfVSdjkBb5s0pc_ur5A6)).


### Por que escolher `Odoo`?

A seguir algumas características interessantes do por que utilizar `Odoo` nos seus projetos de sistemas web:

* Oferece uma plataforma/estrutura de sistema web pronta para uso. Você não precisa se preocupar em construir uma infraestrutura de código para suportar a aplicação.
* Ideal para projetos rápidos, onde você quer se concentrar na lógica de negócios.
* Possui diversos módulos já prontos que podem ser re-utilizados e customizados.
* Possui um framework próprio, mas simples, que acelera a criação do aplicativo.
* Você pode construir seus próprios módulos do zero.
* Possui uma larga comunidade.
* Possui uma excelente documentação.
* Apesar de ser open source, possui versão enterprise pagas que garantem a continuidade da ferramenta.


## Execução Rápida

Caso queira executar rapidamente o `Odoo` para testes de interface, execute:

```
# init database
docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:13

# init odoo
docker run -p 8069:8069 --name odoo --link db:db -t odoo
```

Mais detalhes [clique aqui](https://hub.docker.com/_/odoo).

## Configuração do Ambiente

Pré-Requisitos:
- [Ubuntu 22.04](https://ubuntubr.com.br/download/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [VSCode](https://code.visualstudio.com/Download)
  - [Remote WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
    - _Necessário caso esteja executando o projeto dentro do WSL_

Primeiro, realize o clone deste repositório para a sua pasta de `projetos`.

Em seguinda clone o [repositório oficial do Odoo 15](https://github.com/odoo/odoo/tree/15.0) para a pasta `root > project`.

```shell
cd root/project
git clone https://github.com/odoo/odoo.git -b 15.0
```

Em seguida, clonar os repositórios customizados para a pasta `addons`:

```shell
cd root/project/addons

git clone https://github.com/eduardoluizgs/Odoo-15-Docker
```

Em seguinda, copie os arquivos de `addons auxiliares` disponível no arquivo `addons.rar` para a pasta `root/project/addons`.

Em seguida, crie a rede que irá conectar os conatainers:

```shell
docker network create --driver bridge containers-network
```

Em seguida, crie a imagem base do `Odoo 15`:

```shell
docker build -t odoo15:20221005 .
```

Em seguida, suba o docker-compose do `Postgres`:

```shell
cd compose/odoo15_db

docker-compose up -d
```

Se for a primeira vez que você está iniciando o projeto, inicializa o banco de dados:

```shell
cd compose/odoo15_db

docker-compose --env-file .env-init-database up
```

Em seguda, suba o docker-compose da aplicação:

```shell
cd compose/odoo15_app

docker-compose up -d
```

Em seguida, forneça as permissões aos arquivos e pastas:

```shell
sudo chmod 777 odoo
sudo chmod 777 entrypoint.sh
sudo chmod 777 root/storage/files/
```

Para finalizar, teste o acesso a aplicação acessando o endereço [http://localhost:8069](http://localhost:8069) com o usuário `admin` e senha `admin`.

## Restaurando o backup

Pare a aplicação:

```shell

docker-compose stop
```

Acesse o `shell` do container do `Postgres` e execute os comentos a seguir para preparar a restauração:

```shell
psql -U odoo -d postgres

postgres=# DROP DATABASE odoo15;
postgres=# CREATE DATABASE odoo15 OWNER odoo;
```

Em seguida, saia do container do banco de dados.

Solicite um arquivo de backuo do banco para a equipe de desenvolvimento. Copie o arquivo fornecido para a pasta `/tmp` e execute:

```shell
docker exec -i odoo15_db pg_restore --no-owner --role=odoo -U odoo -d odoo15 < .backup/odoo15-backup.dump
```

Em seguida, acesse o `shell` do container da aplicação e execute os comandos a seguir para trocar senha do usuário `Admin`:

```
odoo shell -d odoo15

>>> user = env['res.users'].search([('login', '=', 'admin')])
>>> user.login = 'admin'
>>> user.password = 'admin'
>>> self.env.cr.commit()
>>> quit()
```

Em seguida, realiza uma atualizaçào completa do `Odoo`:

```shell
docker-compose --env-file .env-update-all up
```

Em seguida, testar acesso a aplicação acessando o endereço [http://localhost:8069](http://localhost:8069) logando com as credenciais novas.

Caso a aplicação não seja carregado com os erros no console do navegador `jQuery is not a function`, execute o comando a seguir no banco de dados:

```sql
DELETE FROM ir_attachment WHERE url LIKE '/web/content/%'
```

## Estrutura das Pastas

```
project
|_ compose
|_ root
  |_ project
    |_ addons
    |_ odoo
  |_ storage
```

* **compose**: Arquivos de inicialização das aplicações.
* **project**: Arquivos fontes do projeto.
* **addons**: Arquivos fontes dos módulos adicionais do `Odoo`.
* **odoo**: Código fonte original do `Odoo`
* **storage**: Pasta para persistência de arquivos da aplicação.

## Inicializar a Aplicação

Para inicializar a aplicação utilize alguns dos comandos a seguir:

```shell
cd compose/odoo15_app

# subir a aplicação
docker-compose up

# subir a aplicação em background
docker-compose up -d

# subir a aplicação em modo DEBUG (exclusivo do VSCode)
docker-compose --env-file .env-debug up

# subir a aplicação inicializando um novo banco de dados
docker-compose --env-file .env-init-database up

# subir a aplicação atualizando os módulos do projeto
docker-compose --env-file .env-update up

# subir a aplicação atualizando todos os móudlos do projeto
docker-compose --env-file .env-update-all up

# Inicializar a aplicação em background com Build de imagem
docker-compose -p odoo15_app up -d --build

# parar o container da aplicação
docker-compose -p odoo15_app down
```

## Links

* Essencial para trabalhar bem como Odoo:
  * [Odoo ORM API](https://www.odoo.com/documentation/15.0/developer/reference/backend/orm.html)
  * [Odoo View](https://www.odoo.com/documentation/15.0/developer/reference/backend/views.html)
  * [Odoo Actions](https://www.odoo.com/documentation/15.0/developer/reference/backend/actions.html)
* Instalação:
  * [Odoo Get Starter Repository](https://github.com/eduardoluizgs/OdooGetStarter)
  * [Odoo Docker Hub](https://hub.docker.com/_/odoo)
  * [Odoo Standalone Install](https://www.odoo.com/documentation/15.0/administration/install.html)
  * [Install Odoo 15 using Docker, Nginx on Ubuntu 22.04](https://www.cloudbooklet.com/install-odoo-15-using-docker-nginx-on-ubuntu-22-04/)
* Documentação:
  * [Odoo Docs](https://www.odoo.com/documentation/15.0/developer.html)
