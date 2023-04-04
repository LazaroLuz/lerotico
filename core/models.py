import peewee

db = peewee.SqliteDatabase('comic.db')


class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        database = db


class Login(BaseModel):
    nome = peewee.CharField(unique=True)
    password = peewee.CharField(unique=True)


class Comic(BaseModel):
    """ Classe que representa a tabela Author """
    # A tabela possui apenas o campo 'name', que receberá o nome do autor sera unico
    name = peewee.CharField(unique=True)


class Link(BaseModel):
    """ Classe que representa a tabela Book """

    # A tabela possui apenas o campo 'title', que receberá o nome do livro
    urls = peewee.CharField(unique=True)

    # Chave estrangeira para a tabela Author
    comic = peewee.ForeignKeyField(Comic)


class Videos(BaseModel):
    imagem = peewee.CharField()
    link = peewee.CharField()


if __name__ == '__main__':
    try:
        Comic.create_table()
        print('Tabela Comic criada com sucesso!!!')
    except peewee.OperationalError:
        print('Tabelas Comic ja existente!!!')
    try:
        Link.create_table()
        print('Tabela Link criada com sucesso!!!')
    except peewee.OperationalError:
        print('Tabelas Link ja existente!!!')
    try:
        Login.create_table()
        print('Tabela Login criada com sucesso!!!')
    except peewee.OperationalError:
        print('Tabelas Login ja existente!!!')
    try:
        Videos.create_table()
        print('Tabela Videos criada com sucesso!!!')
    except peewee.OperationalError:
        print('Tabelas Videos ja existente!!!')