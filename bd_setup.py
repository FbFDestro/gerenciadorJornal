import psycopg2

class Database:
    def __init__(self):
        print("Open DB Connection")
        self.cnx = psycopg2.connect(host='127.0.0.1', database='jornal',
                                    user='fbfdestro ', password='1234*', port=5432)        

    def check_conection(self):
        return self.cnx.closed

    def get_cursor(self):
        cur = self.cnx.cursor()
        print("Return Cursor")
        return cur

    def close_connection(self):
        self.cnx.commit()
        self.cnx.close()
        print("Close connection")

def drop_table(cur):
    sql_command = """DROP TABLE IF EXISTS COMENTARIO;
                    DROP TABLE IF EXISTS EQUIPAMENTO_UTILIZADO;
                    DROP TABLE IF EXISTS PARTICIPA;
                    DROP TABLE IF EXISTS VIDEO;
                    DROP TABLE IF EXISTS EQUIPAMENTO;
                    DROP TABLE IF EXISTS SALA_EQUIPAMENTOS;
                    DROP TABLE IF EXISTS MATERIA_FINAL;
                    DROP TABLE IF EXISTS EPISODIO;
                    DROP TABLE IF EXISTS SALA_EDICAO;
                    DROP TABLE IF EXISTS LOCAL;
                    DROP TABLE IF EXISTS APROVACAO;
                    DROP TABLE IF EXISTS MATERIA;
                    DROP TABLE IF EXISTS LINK;
                    DROP TABLE IF EXISTS PAUTA;
                    DROP TABLE IF EXISTS CARGO_PARTICIPANTE;
                    DROP TABLE IF EXISTS PARTICIPANTE;
                    DROP TABLE IF EXISTS PRODUTOR;
                    DROP TABLE IF EXISTS JORNALISTA;
                    DROP TABLE IF EXISTS EDITOR;
                    DROP TABLE IF EXISTS PESQUISADOR;
                    DROP TABLE IF EXISTS PESSOA;"""
    cur.execute(sql_command)

def create_table(cur):
    sql_command = """
                    CREATE TABLE PESSOA (
                        CPF CHAR(11),
                        NOME VARCHAR(20) NOT NULL,
                        TEL INTEGER,

                        CONSTRAINT PK_PESSOA
                            PRIMARY KEY (CPF)
                    );

                    CREATE TABLE PESQUISADOR (
                        CPF CHAR(11),

                        CONSTRAINT PK_PESQUISADOR
                            PRIMARY KEY (CPF),
                        CONSTRAINT FK_PESQUISADOR
                            FOREIGN KEY (CPF)
                            REFERENCES PESSOA (CPF)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE EDITOR (
                        CPF CHAR(11),

                        CONSTRAINT PK_EDITOR
                            PRIMARY KEY (CPF),
                        CONSTRAINT FK_EDITOR
                            FOREIGN KEY (CPF)
                            REFERENCES PESSOA (CPF)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE JORNALISTA (
                        CPF CHAR(11),

                        CONSTRAINT PK_JORNALISTA
                            PRIMARY KEY (CPF),
                        CONSTRAINT FK_JORNALISTA
                            FOREIGN KEY (CPF)
                            REFERENCES PESSOA (CPF)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE PRODUTOR (
                        CPF CHAR(11),

                        CONSTRAINT PK_PRODUTOR
                            PRIMARY KEY (CPF),
                        CONSTRAINT FK_PRODUTOR
                            FOREIGN KEY (CPF)
                            REFERENCES PESSOA (CPF)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE PARTICIPANTE (
                        CPF CHAR(11),

                        CONSTRAINT PK_PARTICIPANTE
                            PRIMARY KEY (CPF),
                        CONSTRAINT FK_PARTICIPANTE
                            FOREIGN KEY (CPF)
                            REFERENCES PESSOA(CPF)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE CARGO_PARTICIPANTE (
                        CARGO VARCHAR(20) NOT NULL,
                        PESSOA CHAR(11) NOT NULL,

                        CONSTRAINT PK_CARGO_PARTICIPANTE
                            PRIMARY KEY (CARGO, PESSOA),
                        CONSTRAINT FK_CARGO_PARTICIPANTE
                            FOREIGN KEY (PESSOA)
                            REFERENCES PARTICIPANTE(CPF)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE PAUTA (
                        TITULO VARCHAR(100),
                        PESQUISADOR CHAR(11) NOT NULL DEFAULT 'INATIVO',
                        DATA_INCLUSAO DATE,
                        RESUMO TEXT,

                        CONSTRAINT PK_PAUTA
                            PRIMARY KEY (TITULO),
                        CONSTRAINT FK_PAUTA
                            FOREIGN KEY (PESQUISADOR)
                            REFERENCES PESQUISADOR(CPF)
                            ON DELETE SET DEFAULT
                    );

                    CREATE TABLE LINK (
                        PAUTA VARCHAR(100),
                        LINK VARCHAR(200),

                        CONSTRAINT PK_LINK
                            PRIMARY KEY(PAUTA, LINK),
                        CONSTRAINT FK_LINK
                            FOREIGN KEY (PAUTA)
                            REFERENCES PAUTA(TITULO)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE MATERIA (
                        TITULO VARCHAR(100),
                        JORNALISTA CHAR(11) NOT NULL DEFAULT 'INATIVO',
                        DATA_INCLUSAO DATE,
                        TEXTO TEXT,

                        CONSTRAINT PK_MATERIA
                            PRIMARY KEY (TITULO),
                        CONSTRAINT FK_MATERIA_PAUTA
                            FOREIGN KEY (TITULO)
                            REFERENCES PAUTA(TITULO)
                            ON DELETE CASCADE,
                        CONSTRAINT FK_MATERIA_JORNALISTA
                            FOREIGN KEY (JORNALISTA)
                            REFERENCES JORNALISTA(CPF)
                            ON DELETE SET DEFAULT
                    );

                    CREATE TABLE APROVACAO (
                        MATERIA VARCHAR(100),
                        PRODUTOR_APROVADOR CHAR(11),

                        CONSTRAINT PK_APROVACAO
                            PRIMARY KEY(MATERIA),
                        CONSTRAINT FK_APROVACAO_MATERIA
                            FOREIGN KEY (MATERIA)
                            REFERENCES MATERIA(TITULO)
                            ON DELETE CASCADE,
                        CONSTRAINT FK_APROVACAO_PRODUTOR
                            FOREIGN KEY (PRODUTOR_APROVADOR)
                            REFERENCES PRODUTOR(CPF)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE LOCAL (
                        ID SERIAL,
                        LOGRADOURO VARCHAR(100) NOT NULL,
                        NUMERO_RUA INTEGER NOT NULL,
                        CEP CHAR(8) NOT NULL,
                        CIDADE VARCHAR(20),
                        ESTADO CHAR(2),
                        BLOCO INTEGER,
                        ANDAR INTEGER,
                        NUMERO_SALA INTEGER,

                        CONSTRAINT PK_LOCAL
                            PRIMARY KEY (ID)
                    );

                    CREATE TABLE SALA_EDICAO (
                        BLOCO INTEGER,
                        ANDAR INTEGER,
                        NUMERO INTEGER,

                        CONSTRAINT PK_SALA_EDICAO
                            PRIMARY KEY (BLOCO, ANDAR, NUMERO)
                    );

                    CREATE TABLE EPISODIO (
                        DATA DATE,
                        PRODUTOR CHAR(11) DEFAULT 'INATIVO',

                        CONSTRAINT PK_EPISODIO
                            PRIMARY KEY(DATA),
                        CONSTRAINT FK_EPISODIO
                            FOREIGN KEY (PRODUTOR)
                            REFERENCES PRODUTOR (CPF)
                            ON DELETE SET DEFAULT
                    );

                    CREATE TABLE MATERIA_FINAL (
                        VIDEO_FINAL VARCHAR(50),
                        EDITOR CHAR(11) NOT NULL DEFAULT 'INATIVO',
                        BLOCO INTEGER NOT NULL DEFAULT -1, -- NOJENTO HEUHEU
                        ANDAR INTEGER NOT NULL DEFAULT -1,
                        NUMERO INTEGER NOT NULL DEFAULT -1,
                        DATA TIMESTAMP NOT NULL,
                        PERIODO INTERVAL NOT NULL,
                        EPISODIO DATE,

                        CONSTRAINT PK_MATERIA_FINAL
                            PRIMARY KEY (VIDEO_FINAL),
                        CONSTRAINT FK_MATERIA_FINAL_EDITOR
                            FOREIGN KEY (EDITOR)
                            REFERENCES EDITOR(CPF)
                            ON DELETE SET DEFAULT,
                        CONSTRAINT FK_MATERIA_FINAL_SALA_EDICAO
                            FOREIGN KEY (BLOCO, ANDAR, NUMERO)
                            REFERENCES SALA_EDICAO (BLOCO, ANDAR, NUMERO)
                            ON DELETE SET DEFAULT,
                        CONSTRAINT SK_MATERIA_FINAL
                            UNIQUE (EDITOR, BLOCO, ANDAR, NUMERO, DATA),
                        CONSTRAINT FK_MATERIA_FINAL_EPISODIO
                            FOREIGN KEY (EPISODIO)
                            REFERENCES EPISODIO (DATA)
                            ON DELETE SET NULL
                    );


                    CREATE TABLE SALA_EQUIPAMENTOS (
                        BLOCO INTEGER,
                        ANDAR INTEGER,
                        NUMERO INTEGER,

                        CONSTRAINT PK_SALA_EQUIPAMENTOS
                            PRIMARY KEY (BLOCO, ANDAR, NUMERO)
                    );

                    CREATE TABLE EQUIPAMENTO (
                        NPATRIMONIO SERIAL,
                        TIPO CHAR(10),
                        ANO INTEGER,
                        MARCA VARCHAR(20),
                        BLOCO INTEGER,
                        ANDAR INTEGER,
                        NUMERO INTEGER,

                        CONSTRAINT PK_EQUIPAMENTO
                            PRIMARY KEY (NPATRIMONIO),
                        CONSTRAINT FK_EQUIPAMENTO_SALA_EQUIPAMENTO
                            FOREIGN KEY (BLOCO, ANDAR, NUMERO)
                            REFERENCES SALA_EQUIPAMENTOS(BLOCO, ANDAR, NUMERO)
                            ON DELETE SET NULL
                    );


                    CREATE TABLE VIDEO (
                        MATERIA VARCHAR(100),
                        ARQUIVO VARCHAR(50), -- LINK DO VIDEO ARMAZENADO LOCALMENTE 
                        LOCAL INTEGER,
                        MATERIA_FINAL VARCHAR(50),
                        DURACAO INTERVAL,

                        CONSTRAINT PK_VIDEO
                            PRIMARY KEY(MATERIA, ARQUIVO),
                        CONSTRAINT FK_VIDEO_LOCAL
                            FOREIGN KEY (LOCAL)
                            REFERENCES LOCAL(ID)
                            ON DELETE SET NULL,
                        CONSTRAINT FK_VIDEO_MATERIA_FINAL
                            FOREIGN KEY (MATERIA_FINAL)
                            REFERENCES MATERIA_FINAL(VIDEO_FINAL)
                            ON DELETE SET NULL
                    );

                    CREATE TABLE PARTICIPA (
                        MATERIA VARCHAR(100),
                        ARQUIVO VARCHAR(50),
                        CARGO VARCHAR(20),
                        PESSOA CHAR(11),

                        CONSTRAINT PK_PARTICIPA
                            PRIMARY KEY (MATERIA, ARQUIVO, CARGO, PESSOA),
                        CONSTRAINT FK_PARTICIPA
                            FOREIGN KEY (MATERIA, ARQUIVO)
                            REFERENCES VIDEO (MATERIA, ARQUIVO)
                            ON DELETE CASCADE,
                        CONSTRAINT FK2_PARTICIPA
                            FOREIGN KEY (CARGO, PESSOA)
                            REFERENCES CARGO_PARTICIPANTE (CARGO, PESSOA)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE EQUIPAMENTO_UTILIZADO(
                        MATERIA VARCHAR(100),
                        ARQUIVO VARCHAR(50),
                        EQUIPAMENTO INTEGER,

                        CONSTRAINT PK_EQUIPAMENTO_UTILIZADO
                            PRIMARY KEY (MATERIA, ARQUIVO, EQUIPAMENTO),
                        CONSTRAINT FK_EQUIPAMENTO_UTILIZADO_VIDEO
                            FOREIGN KEY (MATERIA, ARQUIVO)
                            REFERENCES VIDEO(MATERIA, ARQUIVO)
                            ON DELETE CASCADE,
                        CONSTRAINT FK_EQUIPAMENTO_UTILIZADO_EQUIPAMENTO
                            FOREIGN KEY (EQUIPAMENTO)
                            REFERENCES EQUIPAMENTO(NPATRIMONIO)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE COMENTARIO(
                        MATERIA VARCHAR(100),
                        PRODUTOR CHAR(11),
                        DATA TIMESTAMP,
                        TEXTO TEXT,

                        CONSTRAINT PK_COMENTARIO
                            PRIMARY KEY (MATERIA, PRODUTOR, DATA),
                        CONSTRAINT FK_COMENTARIO_PRODUTOR
                            FOREIGN KEY (PRODUTOR)
                            REFERENCES PRODUTOR(CPF)
                            ON DELETE CASCADE
                    );
                    """
    cur.execute(sql_command)


if __name__ == "__main__":
    db = Database()
    cur = db.get_cursor()

    drop_table(cur)
    create_table(cur)