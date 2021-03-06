const express = require('express');
const router = express.Router();
const conexao = require('../conexao');

router.use(express.json()); // for parsing application/json
router.use(
  express.urlencoded({
    extended: true,
  })
);

router.delete('/', async (request, response) => {
  console.log(request.body.titulo);
  try {
    //delete from LINK where pauta = '${request.body.titulo}';
    const sql = `
            delete from PAUTA where titulo = '${request.body.titulo}';
        `;
    console.log(sql);
    await conexao.query(sql); //insere pauta
    response.status(200).send('Pauta deletada com sucesso');
  } catch (err) {
    response.status(400).send('Falha ao inserir dados!\n' + err.message);
    console.log('Database ' + err);
    // console.log(Object.getOwnPropertyNames(err));
  }
});

router.post('/', async (request, response) => {
  console.log(request.body.titulo, request.body.pesquisador, request.body.resumo);
  try {
    const sql = {
      text: 'INSERT INTO PAUTA ("titulo", "pesquisador", "resumo") VALUES ($1, $2, $3)',
      values: [
        request.body.titulo.trim(),
        request.body.pesquisador.trim(),
        request.body.resumo.trim(),
      ],
    };

    console.log(sql);

    const ans = await conexao.query(sql); // insere pauta
    console.log(ans);

    response.status(200).send('Dados inseridos com sucesso');
  } catch (err) {
    response.status(400).send('Falha ao inserir dados!\n' + err.message);
    console.log('Database ' + err);
    // console.log(Object.getOwnPropertyNames(err));
  }
});

router.post('/link', async (request, response) => {
  console.log(request.body.pauta, request.body.link);
  try {
    const sql = {
      text: 'INSERT INTO LINK ("pauta", "link") VALUES ($1, $2)',
      values: [request.body.pauta.trim(), request.body.link.trim()],
    };

    console.log(sql);

    await conexao.query(sql); // insere pauta

    response.status(200).send('Dados inseridos com sucesso');
  } catch (err) {
    response.status(400).send('Falha ao inserir dados!\n' + err.message);
    console.log('Database ' + err);
    // console.log(Object.getOwnPropertyNames(err));
  }
});

router.get('/porcentagemPautasGravadas', async (request, response) => {
  // usando await async
  try {
    let sql = `
        SELECT COUNT(distinct p.titulo) FROM VIDEO V
            JOIN PAUTA P
                ON V.MATERIA = P.TITULO;
        `;

    console.log(sql);

    let results = await conexao.query(sql);
    let qtd_video = results.rows[0].count;
    console.log(qtd_video);

    sql = `
        SELECT COUNT(*) FROM PAUTA;
        `;

    results = await conexao.query(sql);
    let qtd_pautas = results.rows[0].count;
    console.log(qtd_pautas);

    response.status(200).json(((qtd_video / qtd_pautas) * 100).toFixed(2));
  } catch (err) {
    response.status(404).send('Not found');
    console.log('Database ' + err);
  }
});

router.get('/semMateria', async (request, response) => {
  // usando await async
  try {
    const sql = `
        SELECT P.titulo, P.pesquisador, PESSOA.nome, to_char(P.DATA_INCLUSAO, 'DD/MM/YYYY') AS DATA_INCLUSAO, P.resumo from PAUTA P
            left join MATERIA M
                ON P.titulo = M.titulo
            join pessoa
                ON PESSOA.cpf = P.pesquisador
            where M.jornalista is null;
        `;

    console.log(sql);

    const results = await conexao.query(sql);
    response.status(200).json(results.rows);
  } catch (err) {
    response.status(404).send('Not found');
    console.log('Database ' + err);
  }
});

router.get('/semMateria/:cpf', async (request, response) => {
  // usando await async
  try {
    const sql = `
        SELECT P.titulo, P.pesquisador, PESSOA.nome, to_char(P.DATA_INCLUSAO, 'DD/MM/YYYY') AS DATA_INCLUSAO, P.resumo from PAUTA P
            left join MATERIA M
                ON P.titulo = M.titulo
            join pessoa
                ON PESSOA.cpf = P.pesquisador
            where M.jornalista is null and P.pesquisador = '${request.params.cpf}';
        `;

    console.log(sql);

    const results = await conexao.query(sql);
    response.status(200).json(results.rows);
  } catch (err) {
    response.status(404).send('Not found');
    console.log('Database ' + err);
  }
});

router.get('/link/:titulo', async (request, response) => {
  // usando await async
  try {
    const sql = `
        select link from  LINK
            where pauta = '${request.params.titulo}';
        `;

    console.log(sql);

    const results = await conexao.query(sql);
    response.status(200).json(results.rows);
  } catch (err) {
    response.status(404).send('Not found');
    console.log('Database ' + err);
  }
});

router.get('/', async (request, response) => {
  // usando await async
  try {
    const sql = `
        select P.TITULO, PESSOA.NOME, P.PESQUISADOR, to_char(P.DATA_INCLUSAO, 'DD/MM/YYYY') AS DATA_INCLUSAO, P.RESUMO from  PAUTA P
            join PESSOA
                ON PESSOA.CPF = P.pesquisador
        order by P.DATA_INCLUSAO desc;
        `;

    console.log(sql);

    const results = await conexao.query(sql);
    response.status(200).json(results.rows);
  } catch (err) {
    response.status(404).send('Not found');
    console.log('Database ' + err);
  }
});

router.get('/pesquisador/:cpf', async (request, response) => {
  // usando await async
  try {
    const sql = `
        select P.TITULO, PESSOA.NOME, P.PESQUISADOR, to_char(P.DATA_INCLUSAO, 'DD/MM/YYYY') AS DATA_INCLUSAO, P.RESUMO  from  PAUTA P
            join PESSOA
                ON PESSOA.CPF = P.pesquisador
            where P.pesquisador = '${request.params.cpf}';
        `;

    console.log(sql);

    const results = await conexao.query(sql);
    response.status(200).json(results.rows);
  } catch (err) {
    response.status(404).send('Not found');
    console.log('Database ' + err);
  }
});

module.exports = router;
