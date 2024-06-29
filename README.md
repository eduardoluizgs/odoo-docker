# Odoo 17 - Docker Development

Este projeto é baseado na plataforma [Odoo](https://www.odoo.com/pt_BR), e contém um repositório com estrutura de projeto `Docker` para desenvolvimento e debug com o `VSCode`.

![Odoo Logo](https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo.png?a=b)

![Odoo Image](https://odoocdn.com/openerp_website/static/src/img/2020/home/screens-mockup.png)

## Introdução

### O que é o `Odoo`?

Odoo é uma solução de gestão empresarial `ERP` completo, com um sistema `CRM` integrado. É baseado na arquitetura `MVC` e implementa um cliente `Java Script` e um servidor `Python`, sendo a comunicação entre o cliente e o servidor por interface `XML-RPC` ou `JSON`. O Software é open source e disponível sob a GNU General Public License ([Wikipédia](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjptvip19D6AhWmRLgEHVhPBDEQmhN6BAhaEAI&url=https%3A%2F%2Fpt.wikipedia.org%2Fwiki%2FOdoo&usg=AOvVaw2UJfVSdjkBb5s0pc_ur5A6)).

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
  - Pode ser executado sobre WSL2. Verifique instruções de instalação [aqui](https://github.com/codeedu/wsl2-docker-quickstart?tab=readme-ov-file#docker-engine-docker-nativo-diretamente-instalado-no-wsl2).
- [Docker](https://www.docker.com/products/docker-desktop/)
  - Docker Engine (Docker Nativo) diretamente instalado no WSL2. Verifique instruções de instalação [aqui](https://github.com/codeedu/wsl2-docker-quickstart?tab=readme-ov-file#docker-engine-docker-nativo-diretamente-instalado-no-wsl2)
- [VSCode](https://code.visualstudio.com/Download)
  - Extensões:
    - [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
    - [Remote WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
      - _Necessário caso esteja executando o projeto dentro do WSL2._

Primeiro, realize o clone deste [repositório](https://github.com/eduardoluizgs/odoo-docker) para a sua pasta de `projetos`:

```shell
git clone https://github.com/eduardoluizgs/odoo-docker -b 17.0
```

Em seguinda clone o repositório oficial do [Odoo 17](https://github.com/odoo/odoo/tree/17.0) para a pasta raiz do projeto:

```shell
git clone https://github.com/odoo/odoo.git -b 17.0
```

Em seguida, clone os repositórios customizados (se existir) para a pasta `./addons`:

```shell
cd ./addons
git clone <url-do-repositorio>.git
```

Em seguinda, copie os arquivos de `addons auxiliares` no arquivo `./addons.zip`, `./addons.rar` ou `./addons.tar.gz` (se existir) para a pasta `./addons`.

Em seguida, crie a rede que irá conectar os containers:

```shell
docker network create --driver bridge containers-network
```

Em seguida, forneça as permissões aos arquivos e pastas:

```shell
sudo chmod 777 ./storage

sudo chmod +x ./build/odoo/odoo
sudo chmod +x ./build/odoo/entrypoint.sh
sudo chmod +x ./build/odoo/wait-for-psql.py

sudo chmod +x ./run-debug.sh
sudo chmod +x ./run-init-database.sh
sudo chmod +x ./run-update-all.sh
sudo chmod +x ./run-update.sh
sudo chmod +x ./run.sh
```

Se for a primeira vez que você está iniciando o projeto, execute:

```shell
make configure
```

Caso contrário, execute:

```shell
make run
```

Teste o acesso a aplicação acessando o endereço [http://localhost:8069](http://localhost:8069) com o usuário `admin` e senha `admin`.

Para finalizar, existe um bug no `odoo` que ao inicializar a aplicação o menu de `Configurações` não é carregado. Assim, ao entrar na aplicação, instale/ative oo módulo `Calendar/Calendário` para resolver o problema.

## Instalando módulos customizados

Em seguida, acesse `Menu Principal > Settings` e clique no link `Activate the developer mode` no final da página. Em seguida, acesse `Menu Principal > Apps > Update App List`. Em seguida, procure pelos módulos do `customizados` e faça a instalação destes.

## Criando o backup do Postgres

Para criar um backup do banco de dados do `odoo` a partir do container, execute o comando abaixo:

```shell
docker exec -i postgres pg_dump -F c -b -v -U odoo -d odoo > .backup/odoo-appname-backup.dump
```

## Restaurando o backup do Postgres

Pare o container da aplicação (container `odoo`).

Acesse o `shell` do container do `Postgres` e execute os comentos a seguir para preparar a restauração:

```shell
psql -U odoo -d postgres

DROP DATABASE odoo;
CREATE DATABASE odoo OWNER odoo;
```

Em seguida, saia do container do banco de dados.

Solicite um arquivo de backup do banco para a equipe de desenvolvimento. Copie o arquivo fornecido para a pasta `.tmp/` e execute:

```shell
docker exec -i postgres pg_restore --no-owner --role=odoo -U odoo -d odoo < .backup/odoo-appname-backup.dump
```

Em seguida, acesse o `shell` do container da aplicação e execute os comandos a seguir para trocar senha do usuário `Admin`:

```python
odoo shell -d

>>> user = env['res.users'].search([('login', '=', 'admin')])
>>> user.login = 'admin'
>>> user.password = 'admin'
>>> self.env.cr.commit()
>>> quit()
```

Em seguida, realiza uma atualizaçào completa do `Odoo`:

```shell
make update-all
```

Em seguida, testar acesso a aplicação acessando o endereço [http://localhost:8069](http://localhost:8069) logando com as credenciais novas.

Caso a aplicação não seja carregado com os erros no console do navegador `jQuery is not a function`, execute o comando a seguir via utilitário `psql` no container de banco de dados:

```sql
DELETE FROM ir_attachment WHERE url LIKE '/web/content/%'
DELETE FROM ir_attachment WHERE url LIKE '/web/assets/%'
```

Caso existe erros de compilação dos assets ou attachments, execute o comando a seguir no banco de dados:

```shell
  ...
  File "/opt/bitnami/odoo/lib/odoo-17.0.post20230815-py3.10.egg/odoo/addons/web/controllers/binary.py", line 109, in content_assets
    stream = request.env['ir.binary']._get_stream_from(record, 'raw', filename)
  File "/opt/bitnami/odoo/lib/odoo-17.0.post20230815-py3.10.egg/odoo/addons/base/models/ir_binary.py", line 129, in _get_stream_from
    stream = self._record_to_stream(record, field_name)
  File "/opt/bitnami/odoo/lib/odoo-17.0.post20230815-py3.10.egg/odoo/addons/base/models/ir_binary.py", line 73, in _record_to_stream
    return Stream.from_attachment(record)
  File "/opt/bitnami/odoo/lib/odoo-17.0.post20230815-py3.10.egg/odoo/http.py", line 473, in from_attachment
    stat = os.stat(self.path)
FileNotFoundError: [Errno 2] No such file or directory: '/bitnami/odoo/data/filestore/odoo_future_prd/c4/c4a07f0cce7c9f19e94878dbf426741253ec45a1'
2024-05-23 20:48:01,049 1 INFO odoo_future_prd werkzeug: 10.244.0.0 - - [23/May/2024 20:48:01] "GET /web/assets/54-bb08df2/web.assets_frontend.min.css HTTP/1.1" 500 - 9 0.014 0.042

```

```sql
DELETE FROM ir_attachment WHERE store_fname LIKE '%<the ending hash>%'
```

## Desinstalar Módulo Manualmente

Caso existam erros de instalação de algum módulo que impeça a execução do `Odoo`, execute o comando a seguir via utilitário `psql` no container de banco de dados:

```shell
# método 1
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'module_name';

# método 2
UPDATE ir_module_module SET state = 'uninstalled' WHERE name = 'module_name';
```

## Estrutura das Pastas

```
project                                : Pasta root/raiz/principal do projeto.
├── .backup                            : Pasta para armazenar arquivos de backup.
├── .vscode                            : Arquivos de configuração do VSCode
├── .tmp                               : Arquivos temporários
├── Makefile                           : Arquivo com comandos do ambiente de desenvolvimento.
├── README.md                          : Arquivo com instruções do repositório.
├── addons                             : Pasta dos módulos customizados.
├── build                              : Pasta com arquivos de build do ambiente Docker.
│   └── odoo                           : Pasta com arquivos de build da aplicação Odoo.
│       ├── Dockerfile                 : Arquivo de construção da imagem Docker.
│       ├── entrypoint.sh              : Arquivo com comandos de inicialização do container de aplicação do Odoo.
│       ├── odoo                       : Arquivo de inicialização da aplicação Odoo.
│       ├── odoo.conf                  : Arquivo de configuração da aplicação Odoo.
│       ├── requirements.txt           : Arquivo de bibliotecas Python a serem instaladas no build da imagem.
│       └── wait-for-psql.py           : Arquivo para verificar se o banco de dados já está em execução.
├── docker-compose-debug-vscode.yml    : Arquivo docker compose para subida do ambiente de debug com VSCode.
├── docker-compose.yml                 : Arquivo docker compose para subida do ambiente de desenvolvimento.
└── storage                            : Pasta para armazenar arquivos persistentes do sistema.
```

## Manipulando a Aplicação

O arquivo `./Makefile` possui uma série de comandos auxiliares para manipular o ambiente. É válida verificar este arquivo para maiores detalhes.

A seguir segue uma lista de comandos adicionais úteis para manipulação do ambiente:

```shell
# subir a aplicação
docker-compose up
# ou
make run

# subir a aplicação em background
docker-compose up -d

# subir a aplicação em modo DEBUG (exclusivo do VSCode)
make debug

# subir a aplicação inicializando um novo banco de dados
make init-database

# subir a aplicação atualizando os módulos do projeto
make update

# subir a aplicação atualizando todos os móudlos do projeto
make update-all

# parar o container da aplicação
make stop

# remover e limpar todos os containers
docker-compose down
```

## Gerando código automaticamente

Este repositório contém um gerador de código automático. Para utilizar o gerador basta utilizar o atalho `CTRL+SHIFT+P` e escolher `Tasks: Run Task > odoo-build-model-and-view`. Siga os passos do assistente e ao final verifique os arquivos gerados na pasta `./addons/<module_name>/models` e `./addons/<module_name>/views`.

Caso queira customizar o gerador, basta alterar o arquivo [./build/builder/template_builder.py](./build/builder/template_builder.py).

## Links

* Essencial para trabalhar bem como Odoo:
  * [Odoo ORM API](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html)
  * [Odoo View](https://www.odoo.com/documentation/17.0/developer/reference/backend/views.html)
  * [Odoo Actions](https://www.odoo.com/documentation/17.0/developer/reference/backend/actions.html)
* Instalação:
  * [Odoo Get Starter Repository](https://github.com/eduardoluizgs/OdooGetStarter)
  * [Odoo Docker Hub](https://hub.docker.com/_/odoo)
  * [Odoo Standalone Install](https://www.odoo.com/documentation/17.0/administration/install.html)
  * [Install Odoo 16 using Docker, Nginx on Ubuntu 22.04](https://www.cloudbooklet.com/install-odoo-16-using-docker-nginx-on-ubuntu-22-04/)
* Documentação:
  * [Odoo Docs](https://www.odoo.com/documentation/17.0/developer.html)
