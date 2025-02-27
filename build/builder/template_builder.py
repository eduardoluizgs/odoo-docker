import logging
import prettyformatter
import re
import os
import shutil

from argparse import ArgumentParser, OPTIONAL


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')


def _get_file_content(file_path: str) -> str:
    """Captura o conteúdo de um arquivo.

    Args:
        file_path (str): Informe o caminho do arquivo a ser lido.

    Returns:
        str: Conteúdo do arquivo.
    """
    with open(file_path, 'r') as f:
        return f.read()


def _make_backup_file(file_path: str) -> None:
    """Realiza o backup de um arquivo conforme caminho informado.

    Args:
        file_path (str): Informa o caminho do arquivo a ser backapeado.
    """

    # define o nome do arquivo de backup
    file_path_backup = os.path.join(
        os.path.dirname(file_path),
        f'{os.path.basename(file_path)}.backup'
    )

    # verifica se o arquivo já existe e remove
    if os.path.exists(file_path_backup):
        os.remove(file_path_backup)

    # realiza o backup do arquivo atual
    shutil.copy(
        file_path,
        file_path_backup
    )


def _get_template(model_template: str) -> str:
    """Captura o conteúdo de um template.

    Args:
        model_template (str): Informa o nome do arquivo de template a ser retornado.

    Returns:
        str: Conteúdo do arquivo de template.
    """
    with open(os.path.join(TEMPLATE_PATH, model_template), 'r') as f:
        return f.read()


def _get_long_model_name(module_name: str, model_name: str) -> str:
    """Captura o nome completo do modelo do modelo.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Nome do modelo.
e
    Returns:
        str: Nome longo/completo do modelo.
            Exemplo: module_name.model_name
    """
    app_name = model_name.split('_')[0]
    if app_name:
        return f'{app_name}.{module_name.replace(f"{app_name}_", "")}.{model_name}'
    else:
        return f'{module_name}.{model_name}'


def _get_table_model_name(module_name: str, model_name: str) -> str:
    """Captura o nome da tabela para o modelo.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Nome completo do modelo.

    Returns:
        str: Nome longo/completo do modelo com underlines.
            Exemplo: module_name_model_name
    """
    return f'{module_name}_{model_name}'


def _get_capitalized_model_name(value: str) -> str:
    """Transforma o nome do modelo para o estilo capitalizado.

    Necessário para gerar o nome da classe do modelo.

    Args:
        value (str): _description_

    Returns:
        str: _description_
    """

    value = re.sub(r'\w+', lambda m:m.group(0).capitalize(), value.replace('.', ' ').replace('_', ' '))
    value = re.sub("[^a-zA-Z0-9]", "", value)

    return value


def _write_file(
        file_path: str,
        content: str,
        overwrite: bool = False,
        mode='w'
    ) -> None:
    """Realiza gravação do arquivo de texto no disco conforme caminho e conteudo.

    Args:
        file_path (str): Informa o caminho do arquivo a ser escrito.
        content (str): Informa o conteúdo do arquivo a ser escrito.
        overwrite (bool): Informe se o arquivo pode ser sobrescrito.
        mode (str): Informa o mode de escrita do arquivo.
    """

    # verifica se a pasta existe, se não, cria a pasta
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # REVIEW : Remove
    # verifica se o arquivo existe
    # if not overwrite and os.path.exists(file_path):
    #     raise Exception(
    #         f'Arquivo `{file_path}` já existe! '\
    #         f'Faça a exclusão do arquivo e tente novamente!'
    #     )

    # escreve o arquivo
    with open(file_path, mode, encoding='UTF-8') as f:
        f.write(content)


def _write_init(
        module_name: str,
        model_name: str,
        output_folder: str
    ) -> None:
    """Escreve o arquivo de inicialização do módulo.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do arquivo a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """

    file_path = os.path.join(
        output_folder,
        module_name,
        'models',
        'business_entities',
        model_name,
        '__init__.py'
    )

    _write_file(file_path, '')


def _write_model(
        module_name: str,
        model_name: str,
        model_description: str,
        output_folder: str
    ) -> None:
    """Escreve o arquivo de modelo do módulo.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do arquivo a ser gerado.
        model_description (str): Informa a descrição do modelo a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """

    content = _get_template('model.py.template')

    content = (content
        .replace('{{long_model_name}}', _get_long_model_name(module_name, model_name))
        .replace('{{model_description}}', model_description)
        .replace('{{capitalized_model_name}}', _get_capitalized_model_name(model_name))
    )

    file_path = os.path.join(
        output_folder,
        module_name,
        'models',
        'business_entities',
        model_name,
        'model.py'
    )

    _write_file(file_path, content)


def _write_business_logic(
        module_name: str,
        model_name: str,
        output_folder: str
    ) -> None:
    """Escreve o arquivo de arquivo de lógica do módulo.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do arquivo a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """

    content = _get_template('business_logic.py.template')

    content = (content
        .replace('{{long_model_name}}', _get_long_model_name(module_name, model_name))
        .replace('{{capitalized_model_name}}', _get_capitalized_model_name(model_name))
    )

    file_path = os.path.join(
        output_folder,
        module_name,
        'models',
        'business_entities',
        model_name,
        'business_logic.py'
    )

    _write_file(file_path, content)


def _import_model(
        module_name: str,
        model_name: str,
        output_folder: str
    ) -> None:
    """Realiza importação dos arquivos do modelo no arquivo de inicialização
    do módulo Python.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do modelo a ser importado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """

    # captura o conteúdo do arquivo de inicialização do módulo models
    file_path = os.path.join(
        output_folder,
        module_name,
        'models',
        'business_entities',
        '__init__.py'
    )

    # faz backup do arquivo atual, para evitar perda dos dados
    _make_backup_file(file_path)

    # captura o conteúdo do arquivo
    content = _get_file_content(file_path)

    # ajusta o conteúdo do arquivo
    model_import = f'from .{model_name} import model, business_logic'
    if model_import not in content:
        content += model_import + '\n'

    # escreve o novo arquivo
    _write_file(file_path, content, overwrite=True)


def _write_view(
        module_name: str,
        model_name: str,
        model_description: str,
        output_folder: str
    ) -> None:
    """Escreve o arquivo de view para o modelo informado.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do arquivo a ser gerado.
        model_description (str): Informa a descrição da view a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """

    content = _get_template('view.xml.template')

    content = (content
        .replace('{{long_model_name}}', _get_long_model_name(module_name, model_name))
        .replace('{{table_model_name}}', _get_table_model_name(module_name, model_name))
        .replace('{{model_description}}', model_description)
        .replace('{{model_name}}', model_name)
        .replace('{{module_name}}', module_name)
    )

    file_path = os.path.join(
        output_folder,
        module_name,
        'views',
        'business_entities',
        f'{model_name}_view.xml'
    )

    _write_file(file_path, content)


def _import_view(
        module_name: str,
        model_name: str,
        output_folder: str
    ) -> None:
    """Realiza importação dos arquivos do view no arquivo de manifest do módulo odoo.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome da view a ser importada.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """

    # captura o conteúdo do arquivo de inicialização do módulo models
    file_path = os.path.join(
        output_folder,
        module_name,
        '__manifest__.py'
    )

    # faz backup do arquivo atual, para evitar perda dos dados
    _make_backup_file(file_path)

    # ajusta o conteúdo do arquivo
    content = _get_file_content(file_path)

    # converte o conteúdo do arquivo em um objeto python
    settings =  eval(content)

    # adiciona arquivo da view nas configurações se ainda não existir
    file_name = f'{model_name}_view.xml'
    if file_name not in settings['data']:
        settings['data'].append(file_name)

    # converte novas configurações para formato de dicionário
    content = prettyformatter.pformat(
        settings,
        depth=0,
        indent=4,
        shorten=False,
    )

    # escreve o novo arquivo
    _write_file(file_path, content, overwrite=True)


def _write_security(
        module_name: str,
        model_name: str,
        model_description: str,
        output_folder: str
    ) -> None:
    """Adiciona o modelo no arquivo de permissões e segurança do Odoo.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do modelo a ser importado.
        model_description (str): Informa a descrição do modelo a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """

    # captura o conteúdo do arquivo de inicialização do módulo models
    file_path = os.path.join(
        output_folder,
        module_name,
        'security',
        'ir.model.access.csv'
    )

    # faz backup do arquivo atual, para evitar perda dos dados
    _make_backup_file(file_path)

    # captura o conteúdo do arquivo
    content = _get_file_content(file_path)

    # ajusta o conteúdo do arquivo
    model_content = f'access_{_get_table_model_name(module_name, model_name)}_group_user,{model_description} - Grupo Usuários,model_{_get_table_model_name(module_name , model_name)},base.group_user,1,1,1,1'
    if model_content not in content:
        content += model_content + '\n'

    # escreve o novo arquivo
    _write_file(file_path, content, overwrite=True)


def _build_template_model_and_view(
        module_name: str,
        model_name: str,
        model_description: str,
        output_folder: str
    ):
    """Realiza geração de um template com Model + View.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do arquivo a ser gerado.
        model_description (str): Informa a descrição do modelo a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """
    _write_init(module_name, model_name, output_folder)
    _write_model(module_name, model_name, model_description, output_folder)
    _write_business_logic(module_name, model_name, output_folder)
    _import_model(module_name, model_name, output_folder)
    _write_view(module_name, model_name, model_description, output_folder)
    _import_view(module_name, model_name, output_folder)
    _write_security(module_name, model_name, model_description, output_folder)


def _build_template_model(
        module_name: str,
        model_name: str,
        model_description: str,
        output_folder: str
    ):
    """Realiza geração de um template com Model.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do arquivo a ser gerado.
        model_description (str): Informa a descrição do modelo a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """
    _write_init(module_name, model_name, output_folder)
    _write_model(module_name, model_name, model_description, output_folder)
    _write_business_logic(module_name, model_name, output_folder)
    _import_model(module_name, model_name, output_folder)
    _write_security(module_name, model_name, model_description, output_folder)


def _build_template_view(
        module_name: str,
        model_name: str,
        model_description: str,
        output_folder: str
    ):
    """Realiza geração de um template com View.

    Args:
        module_name (str): Informa o nome do modulo a ser gerado o arquivo.
        model_name (str): Informa o nome do arquivo a ser gerado.
        model_description (str): Informa a descrição do modelo a ser gerado.
        output_folder (str): Informa a pasta de saída do arquivo gerado.
    """
    _write_view(module_name, model_name, model_description, output_folder)
    _import_view(module_name, model_name, output_folder)
    _write_security(module_name, model_name, model_description, output_folder)


def _parse_args():
    """Captura os argumentos informados pelo usuário na chamada do aplicativo.

    Returns:
        object: Objeto contendo os argumentos passados pelo usuário.
    """

    parser = ArgumentParser()

    parser.add_argument('--template_type', help='Tipo do template a ser gerado.')
    parser.add_argument('--output_folder', help='Diretório utilizado para geração do template.')
    parser.add_argument('--module_name', help='Nome do módulo Odoo.')
    parser.add_argument('--model_name', help='Nome do modelo a ser gerado.')
    parser.add_argument('--model_description', nargs=OPTIONAL, help='Descrição do modelo a ser gerado.')
    # parser.add_argument('--param', nargs=OPTIONAL, help='')

    return parser.parse_args()


def execute(args):
    """Executa a geração do template com base nos argumentos informados.

    Args:
        args (object): Objeto contendo os argumentos passados pelo usuário.
    """

    logging.info('Iniciando geração do template...')

    if args.template_type == 'model-and-view':
        _build_template_model_and_view(
            args.module_name,
            args.model_name,
            args.model_description,
            args.output_folder
        )
    elif args.template_type == 'model':
        _build_template_model(
            args.module_name,
            args.model_name,
            args.model_description,
            args.output_folder
        )
    elif args.template_type == 'view':
        _build_template_view(
            args.module_name,
            args.model_name,
            args.model_description,
            args.output_folder
        )
    else:
        logging.info(f'Tipo de template não localizado {args.template_type or "?"}...')

    logging.info('Concluído...')


if __name__ == '__main__':
    execute(_parse_args())
