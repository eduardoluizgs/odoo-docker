# Odoo 19.0 - Docker Development

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

Caso queira executar rapidamente o `Odoo` para testes de interface, [clique aqui](https://hub.docker.com/_/odoo).:

## Configuração do Ambiente

Pré-Requisitos:
- [Ubuntu 22.04](https://ubuntubr.com.br/download/) ou [WSL2](https://learn.microsoft.com/pt-br/windows/wsl/install) se você estiver no Windows.
- [Docker Engine](#docker)
- [VSCode](https://code.visualstudio.com/Download)
  - [Remote WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
    - _Necessário caso esteja executando o projeto dentro do WSL_

## Preparando o ambiente

**ATENÇÃ0:** _Caso você esteja utilizando `WSL2` recomenda-se instalar o docker nativamente dentro do próprio WSL. Não utilizar `Docker Desktop`._

```shell
# atualizando o sistema
sudo apt update && sudo apt upgrade -y
sudo apt install ca-certificates curl gnupg lsb-release make -y

# instalação do Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo docker ps # verifique se o docker está rodando

# adicione o usuário docker ao grupo docker
sudo groupadd docker
sudo usermod -aG docker $USER

# reinicie o sistema e veja se o docker ja roda em o sudo
docker ps
```

## Preparando o projeto

Realize o clone deste repositório para a sua pasta de `projetos/`.

```shell
git clone https://github.com/eduardoluizgs/odoo-docker -b 19.0
```

Após builda a imagem e suba o projeto:

```shell
make build-image
docker compose up -d
make init-database
```

Internal Server Error
KeyError: 'ir.http'

Para finalizar, teste o acesso a aplicação acessando o endereço [http://localhost:8069](http://localhost:8069) com o usuário `admin` e senha `admin`.

## Links

* Essencial para trabalhar bem como Odoo:
  * [Odoo ORM API](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html)
  * [Odoo View](https://www.odoo.com/documentation/19.0/developer/reference/backend/views.html)
  * [Odoo Actions](https://www.odoo.com/documentation/19.0/developer/reference/backend/actions.html)
* Instalação:
  * [Odoo Get Starter Repository](https://github.com/eduardoluizgs/OdooGetStarter)
  * [Odoo Docker Hub](https://hub.docker.com/_/odoo)
  * [Odoo Standalone Install](https://www.odoo.com/documentation/19.0/administration/install.html)
  * [Install Odoo 16 using Docker, Nginx on Ubuntu 22.04](https://www.cloudbooklet.com/install-odoo-16-using-docker-nginx-on-ubuntu-22-04/)
* Documentação:
  * [Odoo Docs](https://www.odoo.com/documentation/19.0/developer.html)
* Leitura:
  * [Cybrosys Blog](https://www.cybrosys.com/blog/)
