"""
Gera eventos/relatoriojornadapg3/participantes.js a partir dos lotes de prints
transcritos.

Estrutura: cada entry e (name, email, nota, prompt_key, ts, text).
- prompt_key referencia o dicionario PROMPTS com a frase exibida na jornada.
- entries com mesmo email sao deduplicados em um participante com comments[].

Roda: python3 build-participantes.py
"""
import json
from collections import OrderedDict

PROMPTS = {
    'vamos': 'Vamos nessa?',
    'pressao': 'Você está entendendo por que pressão arterial não é só dado clínico — é responsabilidade do profissional que prescreve. Como você se sente para prescrever com segurança hoje?',
    'aplica': 'Você acabou de entender algo que a maioria dos profissionais ignora na prática. Quanto disso você já aplica com seus alunos hoje?',
    'glicemico': 'Você já entendeu mais sobre controle glicêmico do que muitos colegas de trabalho. Mas a pergunta real é: você se sente capaz de prescrever com autonomia para um aluno diabético amanhã?',
    'final': 'Chegando ao final dessa nossa primeira jornada.',
}

# Cada entry: (name, email, nota, prompt_key, ts, text)
ENTRIES = [
    # === LOTE 1 (22/05/2026) ===
    ('Luana Priscila da Silva Pereira', 'luhpsp190@gmail.com', 5, 'aplica', '22/05/2026 22:01', 'Sedentários'),
    ('Lais de Fátima da Silva', 'layisssliva52@gmail.com', 5, 'vamos', '22/05/2026 21:57', 'Ansiosa pelo curso, vai ser muito bom'),
    ('Alexandre de Oliveira Souza', 'aleolisouza@gmail.com', 5, 'vamos', '22/05/2026 21:54', 'Interessante essa forma de aprendizado...'),
    ('Rudy Zanella Jr', 'rudyzanellajr@gmail.com', 4, 'vamos', '22/05/2026 21:45', '.'),
    ('Pedro Paulo da Silva', 'pedropaulonovavida26@gmail.com', 5, 'vamos', '22/05/2026 21:45', 'Muito dinâmico e prazeroso'),
    ('Francisco Chagas Marques Martins', 'Prof.fran.personal@gmail.com', 5, 'glicemico', '22/05/2026 21:37', 'Reciclagem do conhecimento'),
    ('Cristina Paula Rodrigues', 'crispaularod88@gmail.com', 5, 'vamos', '22/05/2026 21:36', 'Estou cheia de curiosidades e querendo aprender mais.'),
    ('Jéssica Souza', 'jeeh_yasmin@hotmail.com', 5, 'vamos', '22/05/2026 21:35', 'Estou ansiosa e disposta a aprender'),
    ('ERINALDO BARROS DOS SANTOS', 'erinaldoeerika@gmail.com', 5, 'vamos', '22/05/2026 21:32', 'é de suma importância o conhecimento teorico e pratico para uma prescricao e aplicacao correta dos exercícios e atividades no atendimento aos grupos especiais'),
    ('Andressa de Lima Manzini', 'andressalimamanzini@gmail.com', 5, 'vamos', '22/05/2026 21:32', 'Estou muito ansiosa para aprender tudo o que preciso saber, para ser uma profissional de competência e com referência nessa área'),
    ('Átila Gomes da Costa', 'acadsansao@gmail.com', 5, 'pressao', '22/05/2026 21:31', 'Me sinto bem mais seguro com todo esse conteúdo'),
    ('Edvane de Sousa Lima', 'edsousalima@gmail.com', 5, 'vamos', '22/05/2026 21:31', 'Tenho certeza que será uma manhã de muito aprendizado e esclarecimentos, estou ansiosa para nosso workshop!!!'),
    ('Aline', 'Aline.al.alcantara@gmail.com', 5, 'vamos', '22/05/2026 21:27', 'Nao tinha pensado na importância de saber tambem Farmacologia basica, mas realmente é fundamental'),
    ('Mariano pires', 'pirmariano@gmail.com', 5, 'vamos', '22/05/2026 21:26', 'Esse primeiro passo ja foi de grande valia, pois ja mostrou po tos importantes que um profissional da area de ve seguir para ter sucesso.'),
    ('Rita', 'personal.kassia@gmail.com', 5, 'vamos', '22/05/2026 21:24', 'Muito importante o tema e a iniciativa da abordagem. Estou empolgada para o evento e para adquirir mais conhecimento.'),
    ('Pedro Antonio Viana da Luz Witte', 'pedroluzw@gmail.com', 5, 'pressao', '22/05/2026 21:20', 'Ótimo'),
    ('Sheila Aparecida da Silva', 'shesilva.ss86@gmail.com', 5, 'vamos', '22/05/2026 21:20', 'Atualização sempre é importante.'),
    ('Gisele Tizatto', 'giseletizzato@hotmail.com', 5, 'vamos', '22/05/2026 21:17', 'Os meus alunos que tem pressão alta, procuro trabalhar com exercicios de baixa intensidade controlando os batimentos cardíacos. Sempre oriento o usar os relógios que marca os batimentos. Controlo a respiração durante os exercicios, usar cargas mais leves e nos exercicios de solo levantar lentamente p não sentir tonturas. Mas com esse curso terei mais conhecimento para prescrever os exercicios com mais segurança.'),
    ('Pedro Antonio Viana da Luz Witte', 'pedroluzw@gmail.com', 5, 'aplica', '22/05/2026 21:13', 'Ótimo'),
    ('Marcelo Damasceno Reys', 'marceloreys@hotmail.com', 5, 'vamos', '22/05/2026 21:10', 'Muito positivo por enquanto.'),
    ('Pedro Antonio Viana da Luz Witte', 'pedroluzw@gmail.com', 5, 'vamos', '22/05/2026 21:05', 'Ótima organização de material'),
    ('Francisco Chagas Marques Martins', 'Prof.fran.personal@gmail.com', 5, 'pressao', '22/05/2026 20:55', 'Conhecimento'),
    ('Gisele Tizatto', 'giseletizzato@hotmail.com', 5, 'aplica', '22/05/2026 20:39', 'Eu tenho alguns alunos com algum tipo de comorbidade. Não tenho nenhum com problema cardíaco mas pressão alta sim. Procuro sempre explicar p meus alunos que o exercício físico vai além da estética e procuro adaptar os exercícios de acordo com a restrição que meu aluno tem. Procuro me atualizar mas sei que preciso aprender muito ainda.'),
    ('Francisco Chagas Marques Martins', 'Prof.fran.personal@gmail.com', 5, 'aplica', '22/05/2026 20:35', 'Retenção de conhecimento'),
    ('Rodrigo Francisco Mariano Lopes Dias', 'rodrigo.trainer@yahoo.com.br', 5, 'pressao', '22/05/2026 20:11', 'Conteúdo de relembrar. Muit importante.'),
    ('Fabrício Lazarini da Silva', 'fabriciolazarini@yahoo.com.br', 5, 'vamos', '22/05/2026 20:08', 'Rápido, direto e objetivo.'),
    ('ANTONIO CARLOS LUCIANO FILHO', 'acfilho39@gmail.com', 5, 'aplica', '22/05/2026 20:03', 'Tea'),
    ('Rodrigo Francisco Mariano Lopes Dias', 'rodrigo.trainer@yahoo.com.br', 5, 'aplica', '22/05/2026 19:52', 'Idosos'),
    ('Lucas Tiburtino de Lacerda', 'lucastiburtino01@gmail.com', 5, 'aplica', '22/05/2026 19:40', 'Com um pouco de todos os tipos, pois conhecimento só se aprende com todas as situações, sejas boas ou ruins!!'),
    ('Fernando Sampaio Barbosa', 'fernandobalasurf69@gmail.com', 5, 'final', '22/05/2026 19:26', 'Melhorar a vida ativa de cada pessoa, através da atividade física, como um profissional da área.'),
    ('Gilberto Martins dos Santos', 'Gilberto.ms1@hotmail.com', 3, 'pressao', '22/05/2026 19:24', 'Tomo alguns cuidados, como não prescrever atividade de alta intensidade'),
    ('Lucas Tiburtino de Lacerda', 'lucastiburtino01@gmail.com', 5, 'vamos', '22/05/2026 19:21', 'Muito bom esse workshop, tenho certeza que será de muito aprendizado!!'),
    ('Selma Previtalli', 'sprevitalli@sorocaba.sp.gov.br', 5, 'vamos', '22/05/2026 18:49', 'Este curso é muito importante, seja para atualizar ou para aprender. Ainda tenho dúvidas quando o assunto é "Grupos Especiais", pois é profundo, extenso e tenho consciência que não sei tudo. Por isso, estou aqui. Quero atualizar e aprender.'),
    ('Keila estefani cassimiro', 'cassimirosteffani@gmail.com', 5, 'vamos', '22/05/2026 18:04', 'Já estou adorando essa jornada'),
    ('Daniele Feriani', 'df.danifferiani@gmail.com', 5, 'vamos', '22/05/2026 17:59', 'Ótimo conteúdo.'),
    ('Fernando Sampaio Barbosa', 'fernandobalasurf69@gmail.com', 3, 'glicemico', '22/05/2026 17:54', 'Não vejo a hora de adquirir mais informações no workshop, até aqui, ja gostei muito.'),
    ('Igor Henrique Vale da Silva', 'igorhenriquevale@hotmail.com', 5, 'vamos', '22/05/2026 17:47', 'É muito importante se qualificar para melhor atender o público dos idosos levando em conta o bem-estar, comorbidades e limitações.'),
    ('Jonatan Shiniti Sooma', 'jonatansooma@gmail.com', 5, 'aplica', '22/05/2026 17:46', 'Boas explicações'),
    ('Valdineia de oliveira e silva', 'neia_oliveira@hotmail.com', 4, 'final', '22/05/2026 17:33', 'Eu gostaria de realizar a especialização em grupos especiais, pois esse é meu nicho, sempre gostei de trabalhar com pessoas mais velhas, pois elas procuram a atividade por entender a necessidade e os benefícios, mas morando no interior de São Paulo a logística acaba ficando difícil se a especialização for só na capital'),
    ('Valdineia de oliveira e silva', 'neia_oliveira@hotmail.com', 5, 'glicemico', '22/05/2026 17:25', 'Primeiro preciso saber do histórico glicemico desse aluno, se costuma alterar com frequência e em qualperíodo isso acontece'),
    ('Ricardo Filho', 'kakapersonal@hotmail.com', 5, 'aplica', '22/05/2026 17:23', 'Hipertensos e diabéticos.'),
    ('Marcelo', 'marcelodantaspbsb@gmail.com', 5, 'aplica', '22/05/2026 17:23', '✅✅✅'),
    ('Paula Rodrigues da Silva', 'paulinharsnat@gmail.com', 5, 'vamos', '22/05/2026 17:12', 'Conteúdo bem organizado.'),
    ('Alexandre Comar Bianco', 'acbianco@yahoo.com', 5, 'final', '22/05/2026 17:11', 'Atender de forma eficiente grupos especiais.'),
    ('Fernando Sampaio Barbosa', 'fernandobalasurf69@gmail.com', 4, 'pressao', '22/05/2026 17:10', 'Me sinto com um pouco mais de segurança e confiante, em saber desses conhecimentos .'),
    ('Alexandre Comar Bianco', 'acbianco@yahoo.com', 5, 'glicemico', '22/05/2026 17:01', 'Quase pronto.'),
    ('Isabela Camargo', 'bela.c.camargo@hotmail.com', 5, 'vamos', '22/05/2026 16:45', 'Gostaria de agradecer a oportunidade deste curso, que ira agregar mto no meu profissional'),
    ('Ricardo Filho', 'kakapersonal@hotmail.com', 5, 'vamos', '22/05/2026 16:42', 'vamos nessa!'),
    ('Daniel Ravazzani', 'redtigertkdhap@yahoo.com.br', 5, 'aplica', '22/05/2026 16:36', 'Pretendo trabalhar com idosos e na recuperação de saude'),
    ('Ricardo Alexandre', 'miranda-ricardo@bol.com.br', 5, 'vamos', '22/05/2026 16:31', 'Muito informativo , excelente didática de aprendizado, visual muito bom de informações.'),
    ('Pedro Santos da Silveira', 'pedrosantossilveira2948@gmail.com', 5, 'final', '22/05/2026 16:30', 'Curar aquilo que só o movimento consegue'),
    ('Alexandre Comar Bianco', 'acbianco@yahoo.com', 5, 'pressao', '22/05/2026 16:29', 'Com um pouco de dúvida na prática ainda.'),
    ('Pedro Santos da Silveira', 'pedrosantossilveira2948@gmail.com', 5, 'glicemico', '22/05/2026 16:18', 'Ja me sinto preparado'),
    ('Alexandre Comar Bianco', 'acbianco@yahoo.com', 5, 'aplica', '22/05/2026 16:12', 'Hipertensos'),
    ('Amarildo Arca', 'professorarca1@gmail.com', 5, 'aplica', '22/05/2026 16:02', 'Gosto de trabalhar com idosos, devida a ter maior controle da frequência cardiaca por recomendações médicas'),
    ('Jonatan Shiniti Sooma', 'jonatansooma@gmail.com', 4, 'vamos', '22/05/2026 15:57', 'Bacana o começo mas muito só introdutório então não tem muito o que falar nem elogiar kkkk'),
    ('Ari Rossett Junior', 'personal.ari@gmail.com', 5, 'vamos', '22/05/2026 15:50', 'O módulo apresentou conceitos importantíssimos para que possamos atuar com grupos especiais e o melhor, estes conhecimento é transmitido de uma maneira que facilita o aprendizado.'),
    ('Alan Olimpio', 'alanolimpio1995@gmail.com', 5, 'vamos', '22/05/2026 15:47', 'Vamos lá'),
    ('Gilberto Martins dos Santos', 'Gilberto.ms1@hotmail.com', 4, 'aplica', '22/05/2026 15:37', 'Preciso aprender a trabalhar com diabéticos'),
    ('Ana Claudia Arvani', 'ac-arvani@uol.com.br', 5, 'vamos', '22/05/2026 15:33', 'Gostei'),
    ('Idel Fuks', 'iwfuks@gmail.com', 5, 'pressao', '22/05/2026 14:45', 'Sempre procuro trabalhar em conjunto com os médicos que atendem os alunos independentemente de qualquer ação.'),
    ('Thomaz de Melo Alcântara', 'aicantaraldaz@gmail.com', 5, 'vamos', '22/05/2026 14:44', 'Muito bem desenvolvido.'),
    ('Isadora Maria Pereira Felix Rolim', 'misadora199@gmail.com', 5, 'vamos', '22/05/2026 14:07', 'Foi bem interessante'),
    ('Reginaldo Aparecido Rodrigues de Azevedo', 'Regis.az@hotmail.com', 5, 'vamos', '22/05/2026 13:34', 'Estou gostando muito do conteúdo'),
    ('Ivânio José Augusto de Sousa', 'ivaniotx@hotmail.com', 5, 'aplica', '22/05/2026 13:27', 'Excelente!'),
    ('Ivânio José Augusto de Sousa', 'ivaniotx@hotmail.com', 5, 'aplica', '22/05/2026 13:15', 'Excelente!'),
    ('Idel Fuks', 'iwfuks@gmail.com', 1, 'aplica', '22/05/2026 13:13', 'Estou tentando reingressar no mercado de trabalho, por isso atualmente não aplico os conceitos na prática. No entanto em tempos anteriores já aplicava a fisiologia do exercício para com os alunos.'),
    ('Claudemir Aparecido Rodrigues', 'claudemiraparecidorodrigues76@gmail.com', 5, 'pressao', '22/05/2026 13:12', 'Muito bom'),
    ('Marcelo', 'marcelodantaspbsb@gmail.com', 5, 'vamos', '22/05/2026 12:57', '✅✅✅'),
    ('Juliana Rozada Porto Campos', 'julianarozada@hotmail.com', 5, 'vamos', '22/05/2026 12:39', 'Ansiosa para o workshop...'),
    ('Waldir Aliot Jr', 'jraliot@hotmail.com', 5, 'aplica', '22/05/2026 12:34', 'Idosos, oncológicos, cardíacos'),
    ('Ana Beatriz Holanda Rodrigues', 'biaholanda03@gmail.com', 4, 'aplica', '22/05/2026 12:26', 'Atualmente, trabalho com alunos para reabilitação através do Pilates ou musculação. Porém, tenho interesse de aprender mais sobre o público do grupo especiais.'),
    ('Alexandre Francisco da Silva', 'Alex.f.silva75@gmail.com', 4, 'aplica', '22/05/2026 12:11', 'Bom'),
    ('Bruna Delella', 'bruna.delella@outlook.com', 4, 'aplica', '22/05/2026 12:04', 'Já tenho alunos idosos, tb com diabetes tipo 2, e hipertensão.'),
    ('Anderson Albuquerque', 'andalbuquerque@yahoo.com', 5, 'vamos', '22/05/2026 11:42', 'Conteúdo excelente'),
    ('Luis augusto fiori', 'gutofiori0002@hotmail.com', 5, 'vamos', '22/05/2026 11:31', 'Muito bom'),
    ('Debora Barbiero', 'debora.barbiero@sememail.com', 5, 'vamos', '22/05/2026 11:21', 'Vamos lá!'),
    ('Valdineia de oliveira e silva', 'neia_oliveira@hotmail.com', 4, 'pressao', '22/05/2026 10:49', 'Primeiramente eu estudo o caso do aluno, para sim montar seu treino respeitando sua individualidade e limitações'),
    ('Valdineia de oliveira e silva', 'neia_oliveira@hotmail.com', 5, 'aplica', '22/05/2026 10:32', 'Oncológicos em remissão, cardiacos, diabéticos, o meu público alvo é acima dos 60 anos e com comorbidades.'),
    ('Pedro Santos da Silveira', 'pedrosantossilveira2948@gmail.com', 3, 'pressao', '22/05/2026 10:12', 'Por enquanto só vi explicações fisiológicas e não como aplicar atividades a esse público'),
    ('Bruna Delella', 'bruna.delella@outlook.com', 5, 'vamos', '22/05/2026 09:50', 'Já sou aluna da pós, me inscrevi na black infinita em novembro do ano passado, foi a melhor decisão que tomei, estou gostando muito, já tenho alunos de grupos especiais e o conteúdo da pós está me deixando mais segura para trabalhar. Fiz a imersão em janeiro e vou fazer essa novamente, ainda estou insegura para realizar avaliações, e acredito que essa imersão irá me trazer mais segurança.'),
    ('Cassiano Leal', 'lealcassiano@gmail.com', 5, 'aplica', '22/05/2026 07:01', 'Diabético'),
    ('Cassiano Leal', 'lealcassiano@gmail.com', 5, 'vamos', '22/05/2026 06:40', 'Muito empolgado para aprender e poder atender os grupos especiais com segurança'),
    ('Edison Morgado', 'edisonmorgado@prof.educacao.sp.gov.br', 5, 'final', '22/05/2026 04:12', 'Ser útil, com os conhecimentos adquiridos, na orientação áquelas pessoas que decidiram incluir os exercícios físicos em seu modo de vida.'),
    ('Ana Beatriz Holanda Rodrigues', 'biaholanda03@gmail.com', 5, 'vamos', '22/05/2026 03:32', 'A reabilitação também é muito procurada no mercado.'),
    ('Andréia de Souza Carvalho', 'deia-carvalho91@hotmail.com', 5, 'pressao', '22/05/2026 03:19', 'Conteúdo rico!'),
    ('Rafael de Menezes', 'rfimenezes82@gmail.com', 5, 'vamos', '22/05/2026 03:03', 'Gostei bastante, foi bem específico e direto'),
    ('Ana Paula Delamo', 'ana-delamopersonal@hotmail.com', 5, 'vamos', '22/05/2026 02:57', 'Interessante'),
    ('Denis da Silva', 'denissilva261@gmail.com', 5, 'vamos', '22/05/2026 02:53', 'Muito bom'),
    ('Andréia de Souza Carvalho', 'deia-carvalho91@hotmail.com', 5, 'aplica', '22/05/2026 02:43', 'Reabilitação'),
    ('RODRIGO OTAVIO SOUZA MANARIN', 'rodrigoosm83@gmail.com', 5, 'final', '22/05/2026 02:22', 'Levar saúde a todos'),
    ('RODRIGO OTAVIO SOUZA MANARIN', 'rodrigoosm83@gmail.com', 5, 'glicemico', '22/05/2026 02:14', 'Em partes sim, pois depende do objetivo do aluno, do que terei de trabalhar com ele, do nível de diabetes, do paciente em si e como ele trata a doença... há diversos fatores influenciadores na minha prescrição'),
    ('Aldemar Moreira Pires', 'Dema_preto@hotmail.com', 5, 'vamos', '22/05/2026 01:51', 'Espero muito ansioso para estar aprendendo e poder ter mais conhecimento para poder ajudar pessoas não só de grupos especiais mas qualquer pessoas que eventualmente pode ser meu aluno'),
    ('Gustavo Canto', 'gustavo-canto@hotmail.com', 5, 'vamos', '22/05/2026 01:11', '-'),
    ('RODRIGO OTAVIO SOUZA MANARIN', 'rodrigoosm83@gmail.com', 5, 'pressao', '22/05/2026 01:08', 'Me sinto bem e confortável pois tive uma excelente formação'),
    ('RODRIGO OTAVIO SOUZA MANARIN', 'rodrigoosm83@gmail.com', 5, 'aplica', '22/05/2026 00:49', 'Aplico como forma de avaliação do meu trabalho com exercícios como a FC de repouso diminui, então avalio o pré e pós exercício e demonstro isso, indicando que um trabalho bem feito trás diversos beneficios visíveis e "invisíveis"'),
    ('Jeferson Vieira', 'jefsi.303@gmail.com', 5, 'glicemico', '22/05/2026 00:37', 'Quero aprender mais'),
    ('Leandro Azevedo dos Santos', 'Leandroasantos.tdb@gmail.com', 5, 'vamos', '22/05/2026 00:32', 'Bora pra cima'),
    ('ANTONIO CARLOS LUCIANO FILHO', 'acfilho39@gmail.com', 5, 'vamos', '22/05/2026 00:23', 'Bem dinâmico e de fácil absorção'),
    ('Jeferson Vieira', 'jefsi.303@gmail.com', 5, 'pressao', '22/05/2026 00:09', 'Tenho que me aprofundar mais em compreender os efeitos da PA'),
    ('RODRIGO OTAVIO SOUZA MANARIN', 'rodrigoosm83@gmail.com', 5, 'aplica', '22/05/2026 00:08', 'Só recebi orientações, achei que teria mini video aulas baseadas nos tópicos citados'),
    ('José Carlos De Oliveira', 'Jcbraganey@gmail.com', 5, 'vamos', '22/05/2026 00:04', 'Realizei todas as atividades propostas da primeira fase e pretendo dar continuidade, pois me capacitar profissionalmente'),
    ('Rafael dos Santos Olegário', 'ssuperafa@gmail.com', 5, 'vamos', '22/05/2026 00:03', 'Ótimo conteúdo'),

    # === LOTE 2 (21/05/2026 noite) ===
    ('Marcos Augusto de Carvalho Rossini', 'marcosrossini85@gmail.com', 5, 'aplica', '22/05/2026 00:00', 'Conteúdo bem prático.'),
    ('Jeferson Vieira', 'jefsi.303@gmail.com', 5, 'aplica', '21/05/2026 23:49', 'Alunos hipertensos porque há uma falta de profissionais para prescreverem exercicios para esse grupo deixando eles de lado.'),
    ('Fabiana Vieira de Sousa', 'fabyvielra@gmail.com', 5, 'pressao', '21/05/2026 23:33', 'Ainda estou aprendendo a lidar com este grupo.'),
    ('Fabiana Vieira de Sousa', 'fabyvielra@gmail.com', 5, 'aplica', '21/05/2026 23:29', 'Os alunos com obesidade.'),
    ('Fabiana Vieira de Sousa', 'fabyvielra@gmail.com', 5, 'vamos', '21/05/2026 23:23', 'Aprendizado nunca é demais!'),
    ('Jeferson Vieira', 'jefsi.303@gmail.com', 5, 'vamos', '21/05/2026 23:18', 'Estou empolgado para conhecer um pouco mais sobre grupos especiais'),
    ('Marcos Augusto de Carvalho Rossini', 'marcosrossini85@gmail.com', 5, 'vamos', '21/05/2026 23:12', 'Fácil entendimento e gostando.'),
    ('Amarildo Arca', 'professorarca1@gmail.com', 5, 'vamos', '21/05/2026 22:58', 'Foram questões bem elaboradas, totalmente com aspectos referentes ao curso, isso nos enriquece o conhecimento, e abre um leque importante para conquistas de novo plano de trabalho.'),
    ('William Sanchez Citriniti de Oliveira', 'william.citriniti@hotmail.com', 5, 'final', '21/05/2026 22:37', 'Conteúdo muito bom'),
    ('Edison Morgado', 'edisonmorgado@prof.educacao.sp.gov.br', 2, 'glicemico', '21/05/2026 22:33', 'Não me sentiria confiante.'),
    ('William Sanchez Citriniti de Oliveira', 'william.citriniti@hotmail.com', 5, 'glicemico', '21/05/2026 22:32', 'Bem explicado'),
    ('Mayara de Sousa Pereira', 'mayaradesousapereira@gmail.com', 5, 'vamos', '21/05/2026 22:28', 'ótimo!'),
    ('Alexandre Comar Bianco', 'acbianco@yahoo.com', 5, 'vamos', '21/05/2026 22:27', 'Conteúdo bastante interessante e curioso para o que está por vir!'),
    ('Pedro Santos da Silveira', 'pedrosantossilveira2948@gmail.com', 5, 'aplica', '21/05/2026 22:23', 'Com o pessoal de mais idade 40+'),
    ('Marcos Henrique Rosa Galindo', 'marcoshenrique.r.galindo@gmail.com', 5, 'vamos', '21/05/2026 22:22', 'Aquele que acha que sabe tudo é aquele que não sabe nada!'),
    ('Eliesiei Couto Barbosa', 'profile@gmail.com', 5, 'vamos', '21/05/2026 22:10', 'Sim, com certeza. Estamos já com esta situação na família. Infelizmente um deles não conseguiu melhoras na saúde para iniciar um programa de treino direcionado a paciente oncológico.'),
    ('Francisco Chagas Marques Martins', 'Prof.fran.personal@gmail.com', 5, 'vamos', '21/05/2026 22:09', 'Engajado'),
    ('Edison Morgado', 'edisonmorgado@prof.educacao.sp.gov.br', 3, 'pressao', '21/05/2026 21:23', 'Em uma prescrição de exercícios físicos para uma pessoa hipertensa eu daria preferência, por precaução, a exercícios aeróbicos com pouco volume de carga e intensidade.'),
    ('Ricardo Elias', 'Mtx.cross7@gmail.com', 3, 'pressao', '21/05/2026 21:08', 'A'),
    ('Ricardo Elias', 'Mtx.cross7@gmail.com', 3, 'aplica', '21/05/2026 21:05', 'Quero trabalhar com idosos.'),
    ('Ricardo Elias', 'Mtx.cross7@gmail.com', 5, 'vamos', '21/05/2026 21:02', 'Gostei muito e sei que posso evoluir ainda mais e com a ajuda do curso irei mim especializar ainda mais.'),
    ('Henrique Previato Pereira', 'hpreviato@yahoo.com.br', 5, 'vamos', '21/05/2026 20:59', 'Inicio de jornada top'),
    ('William Sanchez Citriniti de Oliveira', 'william.citriniti@hotmail.com', 5, 'pressao', '21/05/2026 20:52', 'Conteúdo excelente'),
    ('Daniel Ravazzani', 'redtigertkdhap@yahoo.com.br', 5, 'vamos', '21/05/2026 20:37', 'Bem interessante, acredito q este conhecimento é fundamental para os profissionais de Ed fisica!'),
    ('Edison Morgado', 'edisonmorgado@prof.educacao.sp.gov.br', 3, 'aplica', '21/05/2026 20:36', 'Gostaria de trabalhar com grupo de hipertenso.'),
    ('William Sanchez Citriniti de Oliveira', 'william.citriniti@hotmail.com', 5, 'aplica', '21/05/2026 20:34', 'Conteúdo simples mas que explica muito bem o que se deve fazer'),
    ('Thomaz Jefferson Pereira Ramos', 'thomazjeffersontom@gmail.com', 5, 'vamos', '21/05/2026 20:31', 'Excelente'),
    ('Fernando Sampaio Barbosa', 'fernandobalasurf69@gmail.com', 4, 'aplica', '21/05/2026 20:28', 'Eu trabalho com alunos de 50 a 93 anos, e cada um tem um comportamento, e preciso muita atenção.'),
    ('Hugo Rodrigo', 'prof.hugorodrigo@gmail.com', 5, 'vamos', '21/05/2026 20:27', 'Otima ideia de material didático , deixa o conteúdo leve e atraente da curiosidade de ler mais e saber mais sobre ! Parabéns'),
    ('Geviane', 'gevianekelly@hotmail.com', 5, 'final', '21/05/2026 20:19', 'Bem estar integral dos indivíduos por meio da prática orientada'),
    ('Geviane', 'gevianekelly@hotmail.com', 5, 'glicemico', '21/05/2026 20:14', 'isso mostra que uma boa avaliacao do aluno e execial na prescricao dos exercicios'),
    ('Rogério Soares Mendes', 'soaresmendes@hotmail.com', 5, 'vamos', '21/05/2026 20:08', 'Gostei muito desta degustação!!!'),
    ('Geviane', 'gevianekelly@hotmail.com', 5, 'pressao', '21/05/2026 20:07', 'mim sinto capaz da prescre'),
    ('Geviane', 'gevianekelly@hotmail.com', 5, 'aplica', '21/05/2026 19:49', 'idosos'),
    ('Fernando Sampaio Barbosa', 'fernandobalasurf69@gmail.com', 5, 'vamos', '21/05/2026 19:45', 'Movimento é vida, ja trabalho com o grupos específicos, e já percebi que quanto mais eles se mexem, mais tem vida.'),
    ('Ana Claudia Amorim da Paz', 'aninhaxuxapaz@hotmail.com', 4, 'pressao', '21/05/2026 19:44', 'Estou entrando melhor'),
    ('Viviane Ribeiro Lima', 'viviane.bianca.sp@gmail.com', 5, 'vamos', '21/05/2026 19:43', 'Conhecimento é importante.'),
    ('Edison Morgado', 'edisonmorgado@prof.educacao.sp.gov.br', 5, 'vamos', '21/05/2026 19:40', 'Gostei da objetividade das etapas apresentadas, com uma linguagem fácil e ideias claras.'),
    ('Jones Pires de Oliveira', 'jonespires@gmail.com', 5, 'aplica', '21/05/2026 19:39', 'Mto bom.'),
    ('Geviane', 'gevianekelly@hotmail.com', 5, 'vamos', '21/05/2026 19:37', 'o conhecimento e a base de tudo'),
    ('Gilberto Martins dos Santos', 'Gilberto.ms1@hotmail.com', 5, 'vamos', '21/05/2026 19:31', 'Se este estufo for realmente estes temas é bem abordados, esteral no fim deste com uma bagagem imensa para ser um profissional melhor'),
    ('Ana Claudia Amorim da Paz', 'aninhaxuxapaz@hotmail.com', 3, 'aplica', '21/05/2026 19:28', 'Diabetes'),
    ('Alex Santana', 'alex@escolaadapta.com', 5, 'aplica', '21/05/2026 19:17', 'Essa aqui é na fase 1'),
    ('Alex Santana', 'alex@escolaadapta.com', 5, 'vamos', '21/05/2026 19:15', 'Corrige essa pergunta jovem'),
    ('Luiz Carlos da Silva Junior', 'luizcjunior.personal@icloud.com', 5, 'vamos', '21/05/2026 19:04', 'Conteúdo muito importante'),
    ('William Sanchez Citriniti de Oliveira', 'william.citriniti@hotmail.com', 5, 'vamos', '21/05/2026 18:59', 'Conteúdo simples porém informativo'),
    ('Juliana Silva Justino', 'juliana_justino@yahoo.com.br', 5, 'aplica', '21/05/2026 18:49', 'Trabalho com musculação. Várias patologias. Inclusive hipertensos.'),
    ('Andréia de Souza Carvalho', 'deia-carvalho91@hotmail.com', 5, 'vamos', '21/05/2026 18:44', 'Estou amando as informações até agora abordada!'),
    ('Allex Bruno', 'allex.bruno600@gmail.com', 5, 'vamos', '21/05/2026 18:40', 'A primeira fase está sendo excelente!'),
    ('Átila Gomes da Costa', 'acadsansao@gmail.com', 5, 'aplica', '21/05/2026 18:36', 'Estou querendo começar a trabalhar com grupos especiais'),
    ('Valdineia de oliveira e silva', 'neia_oliveira@hotmail.com', 3, 'vamos', '21/05/2026 18:36', 'Aguardando a jornada , acho que a nota agora é muito cedo'),
    ('Natalia D S Bueno', 'naahdass.nd@gmail.com', 5, 'vamos', '21/05/2026 18:36', '★★★★★'),
    ('Marcos Henrique do Nascimento Chagas', 'marcos.unioeste@gmail.com', 5, 'vamos', '21/05/2026 18:31', 'Tudo muito interessante'),
    ('Ricardo', 'Ricardopersonal12@gmail.com', 5, 'vamos', '21/05/2026 18:31', 'Até aqui achei bem fácil de entender .'),
    ('Alexandro Francisco da Silva', 'Alex.f.silva75@gmail.com', 4, 'vamos', '21/05/2026 18:31', 'Muito bom aprendi'),
    ('Claudemir Aparecido Rodrigues', 'claudemiraparecidorodrigues76@gmail.com', 5, 'aplica', '21/05/2026 18:21', 'Bom demais'),
    ('Antônio Airton Sedrez Junior', 'sedrez@hotmail.com', 5, 'final', '21/05/2026 18:12', 'Me tornar uma referência como profissional de EF.'),
    ('Jones Pires de Oliveira', 'jonespires@gmail.com', 5, 'vamos', '21/05/2026 18:07', 'Até agora estou gostando.'),
    ('Antônio Airton Sedrez Junior', 'sedrez@hotmail.com', 5, 'glicemico', '21/05/2026 18:06', 'Desejo entender mais e melhor como o controle glicêmico pode me ajudar a prescrever treinos.'),
    ('Juliana Silva Justino', 'juliana_justino@yahoo.com.br', 5, 'vamos', '21/05/2026 17:54', 'Conteúdo bem direcionado.'),
    ('Antônio Airton Sedrez Junior', 'sedrez@hotmail.com', 4, 'pressao', '21/05/2026 17:50', 'Com mais conhecimento sobre o sistema vascular, a prescrição de exercícios se torna mais assertiva.'),
    ('Antônio Airton Sedrez Junior', 'sedrez@hotmail.com', 4, 'aplica', '21/05/2026 17:32', 'Alunos diabéticos'),
    ('Claudemir Aparecido Rodrigues', 'claudemiraparecidorodrigues76@gmail.com', 5, 'vamos', '21/05/2026 17:25', 'Conteúdo muito bom, fácil leitura'),
    ('Karine Vieira de Freitas', 'karine_freitas25@outlook.com', 5, 'vamos', '21/05/2026 17:25', 'ótimo!!!'),
    ('Rogério Mota Barboza', 'rmotaborza@gmail.com', 5, 'vamos', '21/05/2026 17:23', 'Nota dez!'),
    ('Jacqueline Oliveira', 'Jkoliveira200@gmail.com', 5, 'glicemico', '21/05/2026 17:13', 'Espero aprender bastante com o passar do estudo'),
    ('Luciene Cristina Bartolo', 'lucienecb1975@gmail.com', 5, 'vamos', '21/05/2026 17:12', 'Percebi que tem muitos pontos que realmente eu preciso me aprofundar. Conteúdo gerou ainda mais curiosidade e anseio para o treinamento. Muito bom mesmo'),
    ('Raquel Fernanda de Almeida Silva', 'quel_edf@yahoo.com.br', 5, 'vamos', '21/05/2026 17:10', 'Estou lisonjeada com a oportunidade oferecida para me aprofundar num tema tão importante. Desde a minha formação, trabalho com crianças, mas quero e sei que posso contribuir de forma favorável nessa área.'),
    ('Danilo de Medeiros Toniolo', 'danilotoniolo.personal@gmail.com', 5, 'vamos', '21/05/2026 17:08', 'Conhecimento é sempre bom, para trabalharmos com segurança.'),
    ('Marcio Henrique de sousa', 'mhsdam11@gmail.com', 5, 'vamos', '21/05/2026 17:07', 'estou adorando...'),

    # === LOTE 3 (21/05/2026 tarde -> 20/05/2026) ===
    ('David', 'David_bossanova@yahoo.com.br', 5, 'vamos', '21/05/2026 17:06', 'interessante pra maior busca do conhecimento'),
    ('Antônio Airton Sedrez Junior', 'sedrez@hotmail.com', 5, 'vamos', '21/05/2026 17:00', 'Todos os tópicos são de extrema importância a realidade do profissional de educação física. Gostei muito dessa jornada. Obrigado.'),
    ('Lauro dos Santos Filho', 'biglauro2602@gmail.com', 5, 'vamos', '21/05/2026 17:00', 'Muito bom entender a dimensão da prescrição de exercícios físicos'),
    ('Daniela Bruniera Arruda', 'danifazenda16@gmail.com', 5, 'vamos', '21/05/2026 16:59', 'Um ótimo início para ter motivação para o workshop.'),
    ('Agnes Penha Negrao', 'gui_negrao@yahoo.com.br', 5, 'vamos', '21/05/2026 16:57', 'Conteúdo Interessante.'),
    ('Jacqueline Oliveira', 'Jkoliveira200@gmail.com', 5, 'pressao', '21/05/2026 16:54', 'Preciso ter experiência'),
    ('Maria Cristina Santos', 'smorenacris@gmail.com', 5, 'vamos', '21/05/2026 16:52', 'Ola td bem todo conteúdo perfeito'),
    ('Rodrigo Francisco Mariano Lopes Dias', 'rodrigo.trainer@yahoo.com.br', 5, 'vamos', '21/05/2026 16:51', 'interessante e impoetante ter sempre o conhecimento aliado.'),
    ('Ana Guiomar dos Santos', 'anaguiomar01@gmail.com', 5, 'vamos', '21/05/2026 16:50', 'Animada para novos conhecimentos'),
    ('Lucas Guimarães Braga', 'lucasbraga92@live.com', 5, 'vamos', '21/05/2026 16:50', 'Vamos!'),
    ('Gisele Tizatto', 'giseletizzato@hotmail.com', 5, 'vamos', '21/05/2026 16:49', 'Com certeza precisamos ter muito conhecimento para trabalhar com grupos especiais que é cada vez maior nas academias. Eu me sinto bastante insegura para realizar o atendimento e esse curso com certeza fará muita diferença nos meus atendimentos.'),
    ('Juciel Lima dos Santos', 'Juciel.20014@gmail.com', 5, 'vamos', '21/05/2026 16:46', 'Estou gostando, as vezes agente se forma e não busca outros conhecimentos.'),
    ('Gabriel Fernando Barbosa', 'gabrielfb1994@gmail.com', 5, 'vamos', '21/05/2026 16:46', 'Ansioso para a aula no fim de semana!'),
    ('Caroline Iatauro', 'Caiatauro@bol.com.br', 5, 'vamos', '21/05/2026 16:35', 'O 👍'),
    ('Idel Fuks', 'iwfuks@gmail.com', 5, 'vamos', '21/05/2026 16:34', 'vosso profissionalismo é de grandr importância'),
    ('Ana Claudia Amorim da Paz', 'aninhaxuxapaz@hotmail.com', 5, 'vamos', '21/05/2026 16:34', 'Tenho muito a aprender'),
    ('Átila Gomes da Costa', 'acadsansao@gmail.com', 5, 'vamos', '21/05/2026 16:33', 'Ótimo conteúdo esta sendo Ótimo esse preparatório'),
    ('Jacqueline Oliveira', 'Jkoliveira200@gmail.com', 5, 'aplica', '21/05/2026 16:33', 'Idosos'),
    ('Pedro Santos da Silveira', 'pedrosantossilveira2948@gmail.com', 5, 'vamos', '21/05/2026 16:32', 'Achando muito interessante a montagem do curso'),
    ('Luana Priscila da Silva Pereira', 'luhpsp190@gmail.com', 5, 'vamos', '21/05/2026 16:31', 'Top'),
    ('Jason Paulina dos Santos', 'chefe.jason@gmail.com', 5, 'vamos', '21/05/2026 16:27', 'Realmente foi maravilhoso parabéns!!!'),
    ('Fernando bernardo de pontes junior', 'juninhopontes.tj@gmail.com', 5, 'final', '21/05/2026 16:25', '10'),
    ('Fernando bernardo de pontes junior', 'juninhopontes.tj@gmail.com', 5, 'glicemico', '21/05/2026 16:23', '10'),
    ('Fernando bernardo de pontes junior', 'juninhopontes.tj@gmail.com', 1, 'pressao', '21/05/2026 16:21', '10'),
    ('Maristela Borba Terra', 'maristelabterra@yahoo.com.br', 5, 'vamos', '21/05/2026 16:20', 'Ja estou ansiosa para aprender e aumentar meu conhecimento'),
    ('Wellington Berbel', 'wellingtonberbel@hotmail.com', 5, 'vamos', '21/05/2026 16:18', '10 Muito legal a jornada'),
    ('Fernando bernardo de pontes junior', 'juninhopontes.tj@gmail.com', 5, 'aplica', '21/05/2026 16:16', '10'),
    ('Jacqueline Oliveira', 'Jkoliveira200@gmail.com', 5, 'vamos', '21/05/2026 16:16', 'Ansiosa pra dia 24'),
    ('Fernando bernardo de pontes junior', 'juninhopontes.tj@gmail.com', 5, 'vamos', '21/05/2026 16:14', 'ptima'),
    ('Maximiliano Quevedo de Oliveira Rocha', 'mestremaxquevedo@gmail.com', 5, 'vamos', '21/05/2026 16:11', 'Excelente, sempre buscando qualificação profissional'),
    ('Hellen Sena', 'hellensenayou60@gmail.com', 5, 'vamos', '21/05/2026 16:07', 'Adorei a retenção'),
    ('Waldir Aliot Jr', 'jraliot@hotmail.com', 5, 'vamos', '21/05/2026 16:06', 'Excelente curso'),
    ('Matheus Alves', 'w3malves@gmail.com', 5, 'final', '21/05/2026 01:46', 'Ganhar dinheiro'),
    ('Matheus Alves', 'w3malves@gmail.com', 5, 'glicemico', '21/05/2026 01:24', 'Vamo que vamo'),
    ('Matheus Alves', 'w3malves@gmail.com', 5, 'pressao', '20/05/2026 21:04', 'Tenho medo de prescrever errado'),

    # === LOTE 4 (23/05/2026 dia inteiro + complementos de 22/05) ===
    # Screenshot 1 - 23/05 13:47 -> 11:59
    ('WILIAM JUNIOR BUENO', 'wiliamjuniorbueno@gmail.com', 5, 'vamos', '23/05/2026 13:47', 'Personal Trainer: WILIAM JUNIOR BUENO CREF9/PR: 044934-G/PR'),
    ('Andreza Cristina Rodrigues Oliveira', 'tsigaga@gmail.com', 5, 'vamos', '23/05/2026 13:47', 'Bom'),
    ('Rafael Santiago Geremias', 'rafaelsgeremias@gmail.com', 5, 'vamos', '23/05/2026 13:37', 'Excelente'),
    ('João Paulo Ferraz de Castro Teixeira', 'jpmusculacao@gmail.com', 5, 'vamos', '23/05/2026 13:36', 'Obrigado! Preciso mesmo aprender o máximo que eu puder para prescrever treinos adequados para este público, e com segurança de que estou fazendo a coisa certa. Acredito também que trabalhar neste nixo trará à mim uma satisfação pessoal e profissional sem paralelos. Obrigado'),
    ('Letícia', 'leticialau7@gmail.com', 5, 'vamos', '23/05/2026 13:34', 'entendo a importancia e me intersso pelo assunto por isso quero me especializar'),
    ('Fabio Moledo', 'fabiomoledo@hotmail.com', 5, 'vamos', '23/05/2026 13:31', 'O único caminho é o estudo'),
    ('Stephanie Aline de Oliveira', 'teezinha.oliveira02@gmail.com', 5, 'vamos', '23/05/2026 13:29', 'Muito bom'),
    ('Henrique Previato Pereira', 'hpreviato@yahoo.com.br', 5, 'glicemico', '23/05/2026 13:28', 'Ok'),
    ('Lucas Tiburtino de Lacerda', 'lucastiburtino01@gmail.com', 5, 'pressao', '23/05/2026 13:28', 'É uma responsabilidade muito grande, caso seja feita errada, custará a vida do paciente em exercício, muito importante esse aprendizado!'),
    ('Jeilso Feitosa da Silva', 'jasonkan25@gmail.com', 5, 'vamos', '23/05/2026 13:25', 'Estou achando interessante.'),
    ('Cassiano Leal', 'lealcassiano@gmail.com', 5, 'pressao', '23/05/2026 13:20', 'Muito bem organizado e didático'),
    ('Kawan Almeida dos Santos', 'kawanguga200@gmail.com', 4, 'vamos', '23/05/2026 13:14', 'Excelente assunto abortado, precisamos de mais profissionais capacitados e vamos em busca de aumentar o nosso conhecimento.'),
    ('Vicente Nascimento', 'nascivi@yahoo.com.br', 5, 'final', '23/05/2026 13:13', 'Ser humano e eficiente em proporcionar segurança e uma vida saudável aos clientes.'),
    ('Jason Paulina dos Santos', 'chefe.jason@gmail.com', 5, 'final', '23/05/2026 13:12', 'Muito bom'),
    ('Josafa', 'jo.cris.sarah@gmail.com', 5, 'vamos', '23/05/2026 13:11', 'Estou ansioso para participar do workshop.'),
    ('Augusto Cid Perez Verndi', 'augustocpv@gmail.com', 5, 'vamos', '23/05/2026 13:10', 'Excelente'),
    ('Ana Julia Oliveira Alves', 'ana-juliaa_2009@outlook.com', 5, 'vamos', '23/05/2026 13:10', 'Adorei como fazem a preparação para o evento'),
    ('Liliane Codogno Lima', 'liliane_codogno@yahoo.com.br', 5, 'vamos', '23/05/2026 13:09', 'Muito bom'),
    ('Gabriel Fernando Barbosa', 'gabrielfb1994@gmail.com', 5, 'final', '23/05/2026 13:08', 'Muito bom!'),
    ('Rodrigo Frigério', 'rodrigofrigerio.professor@gmail.com', 5, 'vamos', '23/05/2026 13:08', 'Top, aguardando ansiosamente o workshop!!!'),
    ('Jason Paulina dos Santos', 'chefe.jason@gmail.com', 5, 'glicemico', '23/05/2026 13:07', 'Muito bom'),
    ('Gabriel Fernando Barbosa', 'gabrielfb1994@gmail.com', 5, 'glicemico', '23/05/2026 13:07', 'Muito bomNmN'),
    ('Vicente Nascimento', 'nascivi@yahoo.com.br', 5, 'glicemico', '23/05/2026 13:04', 'Ficou mais claro o entendimento deste equilíbrio.'),
    ('Gabriel Fernando Barbosa', 'gabrielfb1994@gmail.com', 5, 'pressao', '23/05/2026 13:04', 'Muito bom'),
    ('Jeferson Vieira', 'jefsi.303@gmail.com', 5, 'final', '23/05/2026 12:46', 'Muitos informação relevante para o aperfeiçoamento'),
    ('Ivânio José Augusto de Sousa', 'ivaniotx@hotmail.com', 5, 'final', '23/05/2026 12:38', 'Prestar o melhor serviço possível aos meus alunos.'),
    ('Rafaela Silva do Nascimento', 'rafaelarsn76@gmail.com', 5, 'vamos', '23/05/2026 12:36', 'Fase bem compreensiva, fácil de entender!!!! Agora, é só estudar e se dedicar ao aprendizado, transformando teoria em prática.'),
    ('Victor dos Santos Garcia', 'v91garcia@gmail.com', 5, 'final', '23/05/2026 12:29', 'Crescimento profissional'),
    ('Ivânio José Augusto de Sousa', 'ivaniotx@hotmail.com', 5, 'glicemico', '23/05/2026 12:28', 'Excelente!'),
    ('Fernando Luís da Silva', 'personalfernandoluis@gmail.com', 5, 'vamos', '23/05/2026 12:22', 'São novos desafios e precisamos sempre estar atualizados.'),
    ('Idel Fuks', 'iwfuks@gmail.com', 5, 'final', '23/05/2026 12:17', 'Proporcionar qualidade de vida à população.'),
    ('Vicente Nascimento', 'nascivi@yahoo.com.br', 5, 'pressao', '23/05/2026 12:15', 'Prescrever a atividade adequada, não oferecendo riscos'),
    ('Jaqueline Leandro Pimenta', 'Jaque.l.pimenta@gmail.com', 5, 'vamos', '23/05/2026 12:15', 'Ansiosa'),
    ('Victor dos Santos Garcia', 'v91garcia@gmail.com', 5, 'glicemico', '23/05/2026 12:12', 'Vou sempre procurar um começo mais tranquilo até ter total controle do aluno.'),
    ('Idel Fuks', 'iwfuks@gmail.com', 5, 'glicemico', '23/05/2026 11:59', 'Com certeza uma avaliação criteriosa e estrutura em ciências, experimentos e constatações de pesquisas iram proporcionar segurança e principalmente HUMANIDADE!'),

    # Screenshot 4 - 23/05 11:52 -> 01:20
    ('Victor dos Santos Garcia', 'v91garcia@gmail.com', 5, 'pressao', '23/05/2026 11:52', 'Procuro estudar o aluno antes para prescrever um treino a ele.'),
    ('Victor dos Santos Garcia', 'v91garcia@gmail.com', 5, 'aplica', '23/05/2026 11:42', 'Idoso'),
    ('Victor dos Santos Garcia', 'v91garcia@gmail.com', 5, 'vamos', '23/05/2026 11:32', 'Excelente'),
    ('Ivânio José Augusto de Sousa', 'ivaniotx@hotmail.com', 5, 'pressao', '23/05/2026 11:31', 'Excelente!'),
    ('Vicente Nascimento', 'nascivi@yahoo.com.br', 4, 'aplica', '23/05/2026 11:23', 'Hipertenso e diabético'),
    ('Jéssica Souza', 'jeeh_yasmin@hotmail.com', 2, 'aplica', '23/05/2026 11:23', 'Atualmente não atuo na área, mas pretendo atuar com mulheres 30+ e grupos para a terceira idade.'),
    ('ANDRÉA LOPES DE SOUSA BARRETO', 'andreabarretopb@gmail.com', 5, 'vamos', '23/05/2026 11:20', 'Estudar é o melhor caminho a seguir.'),
    ('Henrique Previato Pereira', 'hpreviato@yahoo.com.br', 5, 'pressao', '23/05/2026 11:18', 'Muito bom'),
    ('Gabriel Fernando Barbosa', 'gabrielfb1994@gmail.com', 5, 'aplica', '23/05/2026 11:13', 'Muito bom!'),
    ('Adriana Deroldo', 'deroldoadriana@gmail.com', 5, 'pressao', '23/05/2026 11:12', 'Que o profissional de EF, deva atuar com atenção e responsabilidade as condições fisiológicas do aluno, para alcançar os objetivos durante o tratamento.'),
    ('Laís de Fátima da Silva', 'layisssilva52@gmail.com', 5, 'final', '23/05/2026 11:03', 'Fazer a diferença'),
    ('Henrique Previato Pereira', 'hpreviato@yahoo.com.br', 5, 'aplica', '23/05/2026 10:59', 'Ok'),
    ('Josias Vieira Camargo', 'josias.camargo@hotmail.com', 5, 'vamos', '23/05/2026 10:55', 'Muito bom, obrigado.'),
    ('Adriana Deroldo', 'deroldoadriana@gmail.com', 5, 'aplica', '23/05/2026 10:46', 'Trabalho com pessoas idosas'),
    ('Ari Rossett Junior', 'personal.ari@gmail.com', 5, 'aplica', '23/05/2026 10:46', 'O grupo com o qual eu mais trabalho são os idosos, no entanto também quero iniciar os trabalhos com portadores de cardiopatia e este conteúdo me ajudará muito.'),
    ('Wellington Clayton de Oliveira', 'amaral.personaltrainer@gmail.com', 5, 'vamos', '23/05/2026 10:38', '👍'),
    ('Vicente Nascimento', 'nascivi@yahoo.com.br', 5, 'vamos', '23/05/2026 10:35', 'Módulo objetivo'),
    ('Larissa Albino', 'albino.bella@gmail.com', 4, 'vamos', '23/05/2026 10:32', 'Ansiosa para começar'),
    ('Adriana Deroldo', 'deroldoadriana@gmail.com', 5, 'vamos', '23/05/2026 10:10', 'De fato, o profissional de Educação Física, hoje precisa, estar sempre atualizando para atender as demandas e os diversos públicos.'),
    ('Ricardo Filho', 'kakapersonal@hotmail.com', 5, 'pressao', '23/05/2026 09:50', 'Me sinto preparado!'),
    ('David', 'David_bossanova@yahoo.com.br', 5, 'final', '23/05/2026 07:46', 'Ajudar na evolução do ser humano como pessoa'),
    ('David', 'David_bossanova@yahoo.com.br', 5, 'glicemico', '23/05/2026 07:43', 'Após uma boa anamnese da sim pra prescrever com segurança pro aluno'),
    ('David', 'David_bossanova@yahoo.com.br', 5, 'pressao', '23/05/2026 07:36', 'Muito bem'),
    ('David', 'David_bossanova@yahoo.com.br', 5, 'aplica', '23/05/2026 07:32', 'Tea'),
    ('Jason Paulina dos Santos', 'chefe.jason@gmail.com', 5, 'pressao', '23/05/2026 07:24', 'Bom de mais'),
    ('Jason Paulina dos Santos', 'chefe.jason@gmail.com', 5, 'aplica', '23/05/2026 07:18', 'Muito legal'),
    ('Lucas Guimarães Braga', 'lucasbraga92@live.com', 5, 'aplica', '23/05/2026 07:16', 'Idoso, neurodivergente, diabeticos'),
    ('Maycon acunha', 'Mayconacunha@gmail.com', 5, 'vamos', '23/05/2026 06:35', 'Muito bom estou animado para expandir ainda mais meus conhecimentos'),
    ('Rogério Soares Mendes', 'soaresmendes@hotmail.com', 4, 'pressao', '23/05/2026 03:31', 'Pelo conhecido que tenho, fico confortável em preservar os exercícios.'),
    ('Rogério Soares Mendes', 'soaresmendes@hotmail.com', 5, 'aplica', '23/05/2026 02:06', 'Muito bom.'),
    ('Emerson', 'emerson.redf@yahoo.com.br', 5, 'vamos', '23/05/2026 01:57', 'Acredito que o curso será importante para minha função de educador físico.'),
    ('Luana Grave Delavia', 'luanarihanna750@gmail.com', 5, 'final', '23/05/2026 01:28', 'Ótimo'),
    ('Alexandre de Oliveira Souza', 'aleolisouza@gmail.com', 5, 'final', '23/05/2026 01:25', 'Dar melhores condições física as pessoas que praticam esporte, desde crianças ate os idosos'),
    ('Luana Grave Delavia', 'luanarihanna750@gmail.com', 5, 'glicemico', '23/05/2026 01:20', 'Ótimo'),

    # Screenshot 3 - 23/05 01:19 -> 22/05 23:34
    ('Alexandre de Oliveira Souza', 'aleolisouza@gmail.com', 5, 'glicemico', '23/05/2026 01:19', 'Sim, sinto que sou capaz sim... mas creio que preciso me aprofundar mais...'),
    ('Daniele Feriani', 'df.danifferiani@gmail.com', 5, 'aplica', '23/05/2026 01:18', 'Cardiopatas.'),
    ('Luana Grave Delavia', 'luanarihanna750@gmail.com', 5, 'pressao', '23/05/2026 01:15', 'Ótimo'),
    ('Aldemar Moreira Pires', 'Dema_preto@hotmail.com', 5, 'aplica', '23/05/2026 01:11', 'Quero trabalhar com idoso tentar dar uma vida mais saudável a eles'),
    ('Bruna Delella', 'bruna.delella@outlook.com', 5, 'pressao', '23/05/2026 01:06', 'Hoje me sinto muito mais segura para prescrever exercicio para um hipertenso'),
    ('Andressa de Lima Manzini', 'andressalimamanzini@gmail.com', 5, 'final', '23/05/2026 01:02', 'Ser um profissional capacitado e de referência, com conhecimentos necessários e com segurança para atuar com grupos especiais'),
    ('Luana Grave Delavia', 'luanarihanna750@gmail.com', 5, 'aplica', '23/05/2026 01:00', 'Ótimo'),
    ('Alexandre de Oliveira Souza', 'aleolisouza@gmail.com', 5, 'pressao', '23/05/2026 00:59', 'Um pouco mais preparado pra nao passar do limite.'),
    ('Luana Grave Delavia', 'luanarihanna750@gmail.com', 5, 'vamos', '23/05/2026 00:58', 'Ótimo'),
    ('Daniela Bruniera Arruda', 'danifazenda16@gmail.com', 5, 'aplica', '23/05/2026 00:58', 'Conhecimento pré aula 👏🏼👏🏼👏🏼'),
    ('Rafael de Menezes', 'rfimenezes82@gmail.com', 5, 'final', '23/05/2026 00:55', 'Formação continuada, com aproveitamento do que o mercado atual pode oferecer'),
    ('Anderson Carvalho', 'andersoncpersonal@gmail.com', 5, 'vamos', '23/05/2026 00:55', 'Já atuo nessa área a alguns anos. Acredito ter um bom conhecimento teórico e experiência prática, mas estou com bastante expectativa de ter novos aprendizados e atualizar o pouco do que sei! Oportunidade de ouro!'),
    ('Rafael de Menezes', 'rfimenezes82@gmail.com', 4, 'glicemico', '23/05/2026 00:48', 'Ainda não me sinto capaz, preciso de mais conhecimentos'),
    ('Juscelino Rodrigues Lima', 'jorgejuscelino40@gmail.com', 5, 'vamos', '23/05/2026 00:44', 'Está sendo muito a troca de conhecimentos estou gostando muito das perguntas que estão sendo feitas'),
    ('Andressa de Lima Manzini', 'andressalimamanzini@gmail.com', 5, 'glicemico', '23/05/2026 00:43', 'Ainda não me sinto preparada'),
    ('Laís de Fátima da Silva', 'layisssilva52@gmail.com', 2, 'glicemico', '23/05/2026 00:27', 'Estou ansiosa'),
    ('Douglas Jefferson Gonçalves', 'douglasjefferson1980@gmail.com', 5, 'final', '23/05/2026 00:21', 'Eu como professor de educação física, procuro ser o melhor e mais eficiente aos meus alunos, procurar prescrever o melhor exercício para podermos chegar com segurança aos objetivos traçados.'),
    ('Mauricio Laham', 'mauriciolaham@gmail.com', 5, 'pressao', '23/05/2026 00:19', 'Muito importante mesmo.'),
    ('Rafael de Menezes', 'rfimenezes82@gmail.com', 4, 'pressao', '23/05/2026 00:18', 'Com as aulas desta trilha, consigo entender um pouco mais sobre este processo, mas ainda sinto que preciso de mais conhecimento para trazer mais segurança'),
    ('Andréia de Souza Carvalho', 'deia-carvalho91@hotmail.com', 5, 'final', '23/05/2026 00:13', 'Amei o conteúdo, muito produtivo!'),
    ('Douglas Jefferson Gonçalves', 'douglasjefferson1980@gmail.com', 5, 'glicemico', '23/05/2026 00:12', 'Importantes informações para gente que trabalha com alunos atletas amadores e alto rendimento, ficar atento aos sinais e reações dos atletas, assim podendo oferecer o melhor treino com maior segurança'),
    ('Mauricio Laham', 'mauriciolaham@gmail.com', 5, 'aplica', '23/05/2026 00:06', 'Insuficiência cardíaca e hipertensos.'),
    ('Laís de Fátima da Silva', 'layisssilva52@gmail.com', 5, 'pressao', '23/05/2026 00:05', 'Ainda tenho insegurança'),
    ('Douglas Jefferson Gonçalves', 'douglasjefferson1980@gmail.com', 4, 'pressao', '23/05/2026 00:00', 'Temos que ficar atentos aos sinais de resposta dos alunos, para saber se ele está fazendo os exercícios de forma correta e sua pressão adequada ao movimento'),
    ('Alexandre de Oliveira Souza', 'aleolisouza@gmail.com', 5, 'aplica', '22/05/2026 23:57', 'Não aplico ainda pois estou na faculdade ainda... ainda nao tenho definido qual area atuar, mas obter conhecimento e estudos nunca é de mais... tenho tendencia a trabalhar com a terceira idade pois trabalho na secretaria de esportes da cidade, aonde atendemos hipertensos, diabeticos entre outros.'),
    ('Rogeria Maria da Silva', 'rmsilva26@gmail.com', 5, 'vamos', '22/05/2026 23:56', 'A jornada está bem esclarecedora. 👏🏼👏🏼👏🏼'),
    ('Rafael de Menezes', 'rfimenezes82@gmail.com', 3, 'aplica', '22/05/2026 23:54', 'Eu trabalho com grupos da 3ª idade.'),
    ('Andréia de Souza Carvalho', 'deia-carvalho91@hotmail.com', 5, 'glicemico', '22/05/2026 23:51', 'Conteúdo rico'),
    ('Douglas Jefferson Gonçalves', 'douglasjefferson1980@gmail.com', 5, 'aplica', '22/05/2026 23:49', 'Eu trabalho com alunos atletas amadores que trabalha com a frequência cardíaca mais rapida e volta a calma'),
    ('Laís de Fátima da Silva', 'layisssilva52@gmail.com', 5, 'aplica', '22/05/2026 23:48', 'Todos os tipos, idoso, todos os tipos de problemas ortopédicos, diabético, hipertensos, obesos e bariátricos'),
    ('Gisele Soares de Jesus', 'giselestudio20@hotmail.com', 5, 'vamos', '22/05/2026 23:46', 'Muito necessário esse curso'),
    ('Douglas Jefferson Gonçalves', 'douglasjefferson1980@gmail.com', 5, 'vamos', '22/05/2026 23:41', 'Gostei muito das informações, da forma de explicação recomendo parabéns e obrigado pela oportunidade de receber mais informações'),
    ('Daniel Almeida Ribeiro', 'drdanielribeiro23@gmail.com', 5, 'vamos', '22/05/2026 23:37', 'É muito legal a iniciativa de ministrar cursos de capacitação para os profissionais, com certeza isso impactará à nossa classe.'),

    # Screenshot 2 - 22/05 23:34 -> 22:04
    ('Andressa de Lima Manzini', 'andressalimamanzini@gmail.com', 5, 'pressao', '22/05/2026 23:34', 'Estou um pouco mais confiante'),
    ('Thomaz Jefferson Pereira Ramos', 'thomazjeffersontom@gmail.com', 5, 'final', '22/05/2026 23:32', 'Ótimo'),
    ('Renan da Silva Ramos', 'reenan.ramos18@gmail.com', 2, 'aplica', '22/05/2026 23:30', 'Idosos'),
    ('Josiane Peixoto dos Santos Simões', 'jo.peixoto.js@gmail.com', 5, 'vamos', '22/05/2026 23:27', 'Mto feliz em ter essa oportunidade de ampliar meus conhecimentos'),
    ('Thomaz Jefferson Pereira Ramos', 'thomazjeffersontom@gmail.com', 5, 'glicemico', '22/05/2026 23:25', 'Excelente 🌟😊'),
    ('Mauricio Laham', 'mauriciolaham@gmail.com', 5, 'vamos', '22/05/2026 23:19', 'Fundamental esse entendimento. Muitos personals não sabem o que estão fazendo.'),
    ('Átila Gomes da Costa', 'acadsansao@gmail.com', 5, 'final', '22/05/2026 23:15', 'Ter capacidade de oferecer o melhor para todos os tipos e idades de pessoas'),
    ('Suely Tambalo', 'Sutambalo@yahoo.com.br', 4, 'pressao', '22/05/2026 23:13', 'Ainda preciso aprender mais sobre isdo'),
    ('Renan da Silva Ramos', 'reenan.ramos18@gmail.com', 5, 'vamos', '22/05/2026 23:05', 'Conteudo bom e proveitoso 👍'),
    ('Jones Pires de Oliveira', 'jonespires@gmail.com', 5, 'final', '22/05/2026 22:56', 'Bom'),
    ('Suely Tambalo', 'Sutambalo@yahoo.com.br', 5, 'aplica', '22/05/2026 22:54', 'Idosos com comirbidades variadas'),
    ('Ana Margarida Fernandes Pinto Anastácio', 'anafpanastacio@gmail.com', 3, 'pressao', '22/05/2026 22:53', 'Preciso ficar mais segura.'),
    ('Jones Pires de Oliveira', 'jonespires@gmail.com', 5, 'glicemico', '22/05/2026 22:50', 'Mto bom'),
    ('Eda Maria Wiggert Ferreira Zaniolo', 'emwzaniolo@gmail.com', 5, 'vamos', '22/05/2026 22:48', 'Muito interessante o formato dos ensinamentos'),
    ('Edvane de Sousa Lima', 'edsousalima@gmail.com', 5, 'aplica', '22/05/2026 22:44', 'Tenho aplicação na prática, porém sei que preciso melhorar bastante; e meu público, são os idosos!'),
    ('Rita', 'personal.kassia@gmail.com', 5, 'final', '22/05/2026 22:42', 'Ajudar, cuidar, transformar vidas, através da minha profissão dar uma vida mais ativa e com mais qualidade às pessoas.'),
    ('Monica Maria da Silva Barbosa', 'monica_kinhabarbosa@hotmail.com', 5, 'vamos', '22/05/2026 22:40', 'Eu estou muito feliz em poder continuar estudando e aprendendo com profissionais tão capacitados espero a cada dia melhorar meus atendimentos e meu financeiro.'),
    ('Jones Pires de Oliveira', 'jonespires@gmail.com', 5, 'pressao', '22/05/2026 22:37', 'Nota 10'),
    ('Ana Margarida Fernandes Pinto Anastácio', 'anafpanastacio@gmail.com', 3, 'aplica', '22/05/2026 22:37', 'Diabéticos'),
    ('Andressa de Lima Manzini', 'andressalimamanzini@gmail.com', 1, 'aplica', '22/05/2026 22:36', 'Pretendo trabalhar com idosos'),
    ('Thomaz Jefferson Pereira Ramos', 'thomazjeffersontom@gmail.com', 5, 'pressao', '22/05/2026 22:36', 'Realmente a pressão arterial é um "divisor de aguas" no que compete uma prescrição de exercício e acompanhamento do aluno.'),
    ('Alex Douglas Oliveira Pinto', 'alexdop2018@gmail.com', 5, 'vamos', '22/05/2026 22:35', 'Expectativa de colher algumas informações específicas já neste workshop.'),
    ('Rita', 'personal.kassia@gmail.com', 5, 'glicemico', '22/05/2026 22:35', 'Quero ter mais conhecimento sobre esse grupo.'),
    ('Marcelo Dantas Ribeiro', 'secagordura24@gmail.com', 5, 'vamos', '22/05/2026 22:33', 'Foi uma jornada muito proveitosa e objetiva. O conteúdo reforçou de avaliar cada aluno de forma individualizada, principalmente quando falamos de grupos especiais, respeitando limitações, condições de saúde e segurança na prescrição do treinamento. Foi um aprendizado muito importante para minha atuação profissional. Não vejo a hora de iniciar o workshop.'),
    ('Rita', 'personal.kassia@gmail.com', 5, 'pressao', '22/05/2026 22:28', 'Adquirir mais conhecimento.'),
    ('Gisele Tizatto', 'giseletizzato@hotmail.com', 5, 'glicemico', '22/05/2026 22:27', 'Não me sinto ainda preparada para prescrever exercícios p diabéticos com segurança. Preciso me aprofundar mais no conteúdo. Para prescrever exercícios com segurança p meus alunos.'),
    ('Suely Tambalo', 'Sutambalo@yahoo.com.br', 5, 'vamos', '22/05/2026 22:23', 'Monitorar sinais e riscos durante os exercicios'),
    ('IRAN OLIVEIRA', 'iradoju@gmail.com', 5, 'vamos', '22/05/2026 22:21', 'Obrigado!'),
    ('Rita', 'personal.kassia@gmail.com', 5, 'aplica', '22/05/2026 22:21', 'Alguns dos pontos.'),
    ('Thomaz Jefferson Pereira Ramos', 'thomazjeffersontom@gmail.com', 5, 'aplica', '22/05/2026 22:14', 'Excelente explicação sobre sistema cardiovascular e seus receptores'),
    ('Francisco Chagas Marques Martins', 'Prof.fran.personal@gmail.com', 5, 'final', '22/05/2026 22:09', 'Surpreendente'),
    ('Átila Gomes da Costa', 'acadsansao@gmail.com', 5, 'glicemico', '22/05/2026 22:07', 'Me sinto mais seguro com todas informações e também com seus sintomas'),
    ('Ana Margarida Fernandes Pinto Anastácio', 'anafpanastacio@gmail.com', 5, 'vamos', '22/05/2026 22:04', 'Muito importante essa preocupação com o público especial. Precisamos ter mais segurança em atender. Estou animada'),
    ('Wesley Alex', 'wesleyalex79@gmail.com', 5, 'vamos', '22/05/2026 22:04', 'Show'),

    # === LOTE 5 (24/05/2026 — 13:38 -> 11:43) ===
    ('Paula de Freitas Brandão', 'nutripaulabrandao@gmail.com', 5, 'glicemico', '24/05/2026 13:38', 'Um pouco mais segura.'),
    ('Francisco Pereira da Silva Filho', 'parajp_pb@hotmail.com', 5, 'glicemico', '24/05/2026 13:36', 'Tendo como base cientifica os conhecimentos vivenciados, sim'),
    ('Talita de Lucas Morales', 'tatadelucass@hotmail.com', 5, 'aplica', '24/05/2026 13:36', 'Muito bom para minha evolução'),
    ('Ivanice Fernandes de Oliveira', 'prof_ivanice@outlook.com', 5, 'final', '24/05/2026 13:36', 'Ok'),
    ('Whisner Cesar da Silva', 'estudiowpersonal@gmail.com', 5, 'pressao', '24/05/2026 13:36', 'Muito bom'),
    ('Ivanice Fernandes de Oliveira', 'prof_ivanice@outlook.com', 5, 'glicemico', '24/05/2026 13:32', 'Ok'),
    ('Talita de Lucas Morales', 'tatadelucass@hotmail.com', 4, 'vamos', '24/05/2026 13:32', 'Achei muito importante para meu futuro profissional'),
    ('Ivanice Fernandes de Oliveira', 'prof_ivanice@outlook.com', 5, 'pressao', '24/05/2026 13:29', 'Bom.'),
    ('Francisco Pereira da Silva Filho', 'parajp_pb@hotmail.com', 5, 'pressao', '24/05/2026 13:28', 'Mais seguro do que antes de iniciar essa jornada de conhecimento'),
    ('eng.benoni@gmail.com', 'Eng.benoni@gmail.com', 4, 'final', '24/05/2026 13:28', 'Mais conhecimento para melhor atender'),
    ('Ivanice Fernandes de Oliveira', 'prof_ivanice@outlook.com', 5, 'aplica', '24/05/2026 13:25', 'Bom tema.'),
    ('gabrielafermoraes@icloud.com', 'gabrielafermoraes@icloud.com', 5, 'vamos', '24/05/2026 13:24', 'show'),
    ('Ivanice Fernandes de Oliveira', 'prof_ivanice@outlook.com', 5, 'vamos', '24/05/2026 13:20', 'Bom conteúdo, mas poderiam deixar opção de download.'),
    ('Whisner Cesar da Silva', 'estudiowpersonal@gmail.com', 5, 'aplica', '24/05/2026 13:20', 'Esclarecedor'),
    ('Luana da Silva Machado', '19luanamachado@gmail.com', 5, 'aplica', '24/05/2026 13:16', 'Ótimo questionário'),
    ('Francisco Pereira da Silva Filho', 'parajp_pb@hotmail.com', 5, 'aplica', '24/05/2026 13:16', '55+'),
    ('ws8s44vryj@privaterelay.appleid.com', 'ws8s44vryj@privaterelay.appleid.com', 5, 'final', '24/05/2026 13:11', 'Muito bom'),
    ('ANDRÉA LOPES DE SOUSA BARRETO', 'andreabarretopb@gmail.com', 5, 'final', '24/05/2026 13:10', 'Prescrever treinos para os meus alunos com eficiência e responsabilidade.'),
    ('ws8s44vryj@privaterelay.appleid.com', 'ws8s44vryj@privaterelay.appleid.com', 5, 'glicemico', '24/05/2026 13:09', 'Show'),
    ('Whisner Cesar da Silva', 'estudiowpersonal@gmail.com', 5, 'vamos', '24/05/2026 13:08', 'Muito bom e produtivo.'),
    ('Bruna Palotino', 'brunapalotino12@gmail.com', 5, 'final', '24/05/2026 13:08', 'Ser referência e ganhar mais financeiramente'),
    ('ws8s44vryj@privaterelay.appleid.com', 'ws8s44vryj@privaterelay.appleid.com', 5, 'pressao', '24/05/2026 13:06', 'Muito bom'),
    ('Rayanny Tavares Fernandes', 'tavaresrayanny1@gmail.com', 5, 'vamos', '24/05/2026 13:05', 'Aula com bastante informações úteis'),
    ('ws8s44vryj@privaterelay.appleid.com', 'ws8s44vryj@privaterelay.appleid.com', 5, 'aplica', '24/05/2026 13:05', 'Top'),
    ('Bruna Palotino', 'brunapalotino12@gmail.com', 5, 'glicemico', '24/05/2026 13:04', 'Sim'),
    ('Rodolfo Campos Cardoso', 'rodolfocardoso_155@hotmail.com', 5, 'final', '24/05/2026 13:04', 'Cuidar, acompanhar e transformar a vida de nossos alunos é nossa missão enquanto profissionais!!!'),
    ('eng.benoni@gmail.com', 'Eng.benoni@gmail.com', 4, 'glicemico', '24/05/2026 13:04', 'Com certeza melhor que antes. Mais ainda inseguro.'),
    ('ws8s44vryj@privaterelay.appleid.com', 'ws8s44vryj@privaterelay.appleid.com', 5, 'vamos', '24/05/2026 13:03', 'Muito bom'),
    ('Luana da Silva Machado', '19luanamachado@gmail.com', 5, 'vamos', '24/05/2026 13:03', 'O app é muito útil e a forma como o tema é trabalhado é muito bom'),
    ('Lauro dos Santos Filho', 'biglauro2602@gmail.com', 5, 'aplica', '24/05/2026 13:02', 'Todos do grupo especial'),
    ('Elisangela Patricia da Silva Santos', 'elispatricia777@gmail.com', 5, 'final', '24/05/2026 13:02', 'Ser referência em cuidado individualizado e humanizado.'),
    ('ANDRÉA LOPES DE SOUSA BARRETO', 'andreabarretopb@gmail.com', 5, 'glicemico', '24/05/2026 13:02', 'Realmente, uma avaliação bem estruturada é primordial para uma boa prescrição do treino.'),
    ('Elisangela Patricia da Silva Santos', 'elispatricia777@gmail.com', 5, 'glicemico', '24/05/2026 12:59', 'Ok'),
    ('Francisco Pereira da Silva Filho', 'parajp_pb@hotmail.com', 5, 'vamos', '24/05/2026 12:58', 'Excelente metodologia de avaliação.'),
    ('Elisangela Patricia da Silva Santos', 'elispatricia777@gmail.com', 5, 'pressao', '24/05/2026 12:53', 'Mais preparada'),
    ('Gabriela Ayumi Yano', 'gabriela.yano21@gmail.com', 1, 'pressao', '24/05/2026 12:53', 'Ainda não faço prescrição de treinos, estou cursando a faculdade'),
    ('Daniel Henrique', 'Dhansantos0729@gmail.com', 5, 'vamos', '24/05/2026 12:51', 'Conteúdo top'),
    ('Camila santos', 'Kmyllasantos18@yahoo.com.br', 5, 'vamos', '24/05/2026 12:50', 'Estou amando essa jornada, me deixa mais inspirada e segura em atuar com os grupos especiais'),
    ('Rodolfo Campos Cardoso', 'rodolfocardoso_155@hotmail.com', 5, 'glicemico', '24/05/2026 12:50', 'Com certeza a visão já mudou bastante e o conhecimento específico é fundamental para que eu possa atender e bem este tipo de aluno, por exemplo!!'),
    ('Denise Akemi Simões de Oliveira', 'de.sid@hotmail.com', 2, 'aplica', '24/05/2026 12:49', 'Diabéticos e hipertensos'),
    ('Adriana Deroldo', 'deroldoadriana@gmail.com', 5, 'glicemico', '24/05/2026 12:48', 'Com informações apresentadas no workshop e na prática, acredito ser possível.'),
    ('Bruna Palotino', 'brunapalotino12@gmail.com', 4, 'pressao', '24/05/2026 12:47', 'Ótima'),
    ('Vanessa de Paiva', 'vanessababuzinha@yahoo.com.br', 5, 'vamos', '24/05/2026 12:45', 'muito bom'),
    ('Emerson Corona', 'ecorona8576@gmail.com', 5, 'vamos', '24/05/2026 12:45', 'Muito bom'),
    ('ANDRÉA LOPES DE SOUSA BARRETO', 'andreabarretopb@gmail.com', 5, 'pressao', '24/05/2026 12:43', 'É muito importante entender o funcionamento do organismo do seu aluno para ler essa segurança na prescrição do exercício.'),
    ('Hugo Rodrigo', 'prof.hugorodrigo@gmail.com', 5, 'pressao', '24/05/2026 12:43', 'Muito mais seguro e embasado!'),
    ('José Carlos De Oliveira', 'Jcbraganey@gmail.com', 5, 'final', '24/05/2026 12:38', 'Fazer um trabalho de qualidade, com cunho científico'),
    ('Bruna Palotino', 'brunapalotino12@gmail.com', 5, 'aplica', '24/05/2026 12:37', 'Este módulo foi muito útil'),
    ('Paula de Freitas Brandão', 'nutripaulabrandao@gmail.com', 5, 'pressao', '24/05/2026 12:36', 'Um pouco mais segura, mas ainda preciso de mais conhecimento.'),
    ('André Gonçalves', 'agyann@gmail.com', 4, 'final', '24/05/2026 12:34', 'Me capacitar cada vez mais, pra melhor atender meus clientes.'),
    ('William Olielo Pereira', 'williams.olielo@gmail.com', 5, 'final', '24/05/2026 12:32', 'Transformar positivamente vidas'),
    ('Monica Mendes', 'mepthey@yahoo.com.br', 5, 'final', '24/05/2026 12:32', 'Evoluir como profissional e dar atendimento de qualidade ao meu paciente'),
    ('Cláudio', 'claudiojrferreirapereira56@gmail.com', 5, 'final', '24/05/2026 12:32', 'Busca por conhecimento'),
    ('Fabiano Mendes de Oliveira', 'Profabiano.edu@gmail.com', 5, 'final', '24/05/2026 12:30', 'Qualificar-me para atender pessoas idosas.'),
    ('Amanda Moreira Trevizan', 'amandamtrevizan@hotmail.com', 5, 'vamos', '24/05/2026 12:29', '👍'),
    ('Monica Mendes', 'mepthey@yahoo.com.br', 5, 'glicemico', '24/05/2026 12:29', 'Sim, me sinto confiante e empolgada para o curso'),
    ('William Olielo Pereira', 'williams.olielo@gmail.com', 5, 'glicemico', '24/05/2026 12:28', 'Recursos essenciais para uma prática profissional segura e responsável'),
    ('André Gonçalves', 'agyann@gmail.com', 4, 'glicemico', '24/05/2026 12:28', 'Agora consigo'),
    ('João Lucas Valdomiro Vieira', 'joaolucas190302@gmail.com', 5, 'final', '24/05/2026 12:27', 'Muito bom'),
    ('Fabiano Mendes de Oliveira', 'Profabiano.edu@gmail.com', 5, 'glicemico', '24/05/2026 12:27', 'Sim.'),
    ('Cláudio', 'claudiojrferreirapereira56@gmail.com', 5, 'glicemico', '24/05/2026 12:26', 'Sim'),
    ('João Lucas Valdomiro Vieira', 'joaolucas190302@gmail.com', 5, 'glicemico', '24/05/2026 12:26', 'Legal'),
    ('eng.benoni@gmail.com', 'Eng.benoni@gmail.com', 5, 'pressao', '24/05/2026 12:25', 'Todo cuidado é pouco. Exercícios certos.'),
    ('Bruna Palotino', 'brunapalotino12@gmail.com', 4, 'vamos', '24/05/2026 12:25', 'Gostei'),
    ('Rodolfo Campos Cardoso', 'rodolfocardoso_155@hotmail.com', 5, 'pressao', '24/05/2026 12:23', 'Com o workshop com certeza me sentirei mais seguro para a prescrição e acompanhamento de treinos e exercícios para Grupos Especiais. As informações até aqui, tem ajudado bastante já 🙏🏼👍'),
    ('João Lucas Valdomiro Vieira', 'joaolucas190302@gmail.com', 5, 'pressao', '24/05/2026 12:23', 'Muito bom'),
    ('André Gonçalves', 'agyann@gmail.com', 4, 'pressao', '24/05/2026 12:23', 'Não me sinto confiante, agora com esse curso estou capacitado.'),
    ('Monica Mendes', 'mepthey@yahoo.com.br', 5, 'pressao', '24/05/2026 12:22', 'Aprendendo muito'),
    ('Sabrina Oliveira', 'sabrinajustinodeoliveira@yahoo.com.br', 5, 'vamos', '24/05/2026 12:22', 'conteudo muito bom'),
    ('Fabiano Mendes de Oliveira', 'Profabiano.edu@gmail.com', 5, 'pressao', '24/05/2026 12:22', 'Sim. Estou sempre estudando para estar qualificado para cada caso clínico.'),
    ('Giulia Gomes Nappo', 'nappolitano15@gmail.com', 5, 'glicemico', '24/05/2026 12:22', 'Ótimo conteúdo'),
    ('William Olielo Pereira', 'williams.olielo@gmail.com', 5, 'pressao', '24/05/2026 12:20', 'Informações importantes para uma prática profissional segura e responsável'),
    ('João Lucas Valdomiro Vieira', 'joaolucas190302@gmail.com', 5, 'aplica', '24/05/2026 12:20', 'Muito legal'),
    ('Vanessa Neglisoli', 'vanessaneglisoli@gmail.com', 5, 'pressao', '24/05/2026 12:19', 'Obrigada'),
    ('Cláudio', 'claudiojrferreirapereira56@gmail.com', 5, 'pressao', '24/05/2026 12:18', 'Maior segurança para fazer acompanhamento e prescrição de exercícios para grupos de risco'),
    ('Keli Cristina Toledo Souza', 'kikacristinaT@gmail.com', 5, 'vamos', '24/05/2026 12:18', 'Está sendo muito curioso o conteúdo'),
    ('André Gonçalves', 'agyann@gmail.com', 4, 'aplica', '24/05/2026 12:17', 'Grupo idoso'),
    ('Carlos Júnior de Abreu Braga', 'Carlosjuniorabreu43@gmail.com', 5, 'final', '24/05/2026 12:17', 'Contribuir para a qualidade de vida da população.'),
    ('Monica Mendes', 'mepthey@yahoo.com.br', 5, 'aplica', '24/05/2026 12:17', 'População idosa'),
    ('João Lucas Valdomiro Vieira', 'joaolucas190302@gmail.com', 5, 'vamos', '24/05/2026 12:17', 'Muito bacana'),
    ('Fabiano Mendes de Oliveira', 'Profabiano.edu@gmail.com', 5, 'aplica', '24/05/2026 12:16', 'Como sou aluno do doutorado em Promoção da Saúde, acabo trabalhando com diversos grupos: Idosos. Crianças e adolescentes com doenças crônicas não transmissíveis. Pacientes com sintomas de COVID longa.'),
    ('Giulia Gomes Nappo', 'nappolitano15@gmail.com', 5, 'pressao', '24/05/2026 12:14', 'Ótimo conteúdo'),
    ('André Gonçalves', 'agyann@gmail.com', 4, 'vamos', '24/05/2026 12:14', 'Muito bom o curso'),
    ('Charles Alessandro Neves', 'charles_exalta@hotmail.com', 5, 'final', '24/05/2026 12:14', '🙏'),
    ('Josadak Vasconcelos Neto', 'josadak1402@gmail.com', 5, 'vamos', '24/05/2026 12:13', 'Muito bom'),
    ('Jaqueline Leandro Pimenta', 'Jaque.l.pimenta@gmail.com', 5, 'pressao', '24/05/2026 12:11', 'A importância de conhecer cada indivíduo de forma individual é de extrema importância para prescrever exercícios'),
    ('Stephanie Aline de Oliveira', 'teezinha.oliveira02@gmail.com', 4, 'final', '24/05/2026 12:11', 'Fazer meu trabalho com excelência'),
    ('Carlos Júnior de Abreu Braga', 'Carlosjuniorabreu43@gmail.com', 4, 'glicemico', '24/05/2026 12:11', 'Certo'),
    ('Charles Alessandro Neves', 'charles_exalta@hotmail.com', 5, 'glicemico', '24/05/2026 12:10', '👍'),
    ('William Olielo Pereira', 'williams.olielo@gmail.com', 5, 'aplica', '24/05/2026 12:09', 'Idosos e DCNT'),
    ('Celio de Oliveira Sebastião', 'celioo@prof.educacao.sp.gov.br', 5, 'final', '24/05/2026 12:09', 'Muito bom'),
    ('Monica Mendes', 'mepthey@yahoo.com.br', 5, 'vamos', '24/05/2026 12:08', 'Adorei o conteúdo, estão de parabéns!!!'),
    ('Giulia Gomes Nappo', 'nappolitano15@gmail.com', 5, 'aplica', '24/05/2026 12:07', 'Ótimo conteúdo'),
    ('Fabiano Mendes de Oliveira', 'Profabiano.edu@gmail.com', 5, 'vamos', '24/05/2026 12:07', 'O material didático proporcionou uma base sólida para aprofundar o conhecimento.'),
    ('Charles Alessandro Neves', 'charles_exalta@hotmail.com', 5, 'pressao', '24/05/2026 12:05', '👍'),
    ('Giulia Gomes Nappo', 'nappolitano15@gmail.com', 5, 'vamos', '24/05/2026 12:05', 'Ótimo conteúdo'),
    ('Stephanie Aline de Oliveira', 'teezinha.oliveira02@gmail.com', 3, 'glicemico', '24/05/2026 12:04', 'Ainda não'),
    ('Gilvanildo Pereira de Oliveira', 'gilvanildo.rcc@gmail.com', 5, 'final', '24/05/2026 12:04', 'Ajudar as pessoas, a ter melhora na auto estima e sua qualidade de vida...'),
    ('Vanessa Neglisoli', 'vanessaneglisoli@gmail.com', 5, 'aplica', '24/05/2026 12:03', 'Obrigada'),
    ('Jaqueline Leandro Pimenta', 'Jaque.l.pimenta@gmail.com', 5, 'aplica', '24/05/2026 12:02', 'Atualmente está misto'),
    ('Rodolfo Campos Cardoso', 'rodolfocardoso_155@hotmail.com', 5, 'aplica', '24/05/2026 12:02', 'Trabalho com alunos de idade média, até 60 anos, mas na academia atendemos muitas pessoas de grupos especiais. Que direta ou indiretamente irão nos fazer diretamente com este público.'),
    ('Cláudio', 'claudiojrferreirapereira56@gmail.com', 5, 'aplica', '24/05/2026 12:01', 'Grupo de idosos e estudantes do ensino médio'),
    ('Charles Alessandro Neves', 'charles_exalta@hotmail.com', 5, 'aplica', '24/05/2026 12:01', 'Já trabalhei com alguns tipos diferentes tanto diabética, idosos hipertensão, e com síndromes'),
    ('Vanessa Neglisoli', 'vanessaneglisoli@gmail.com', 5, 'vamos', '24/05/2026 12:00', 'Obrigada'),
    ('José Carlos De Oliveira', 'Jcbraganey@gmail.com', 5, 'vamos', '24/05/2026 12:00', 'Estou ansioso para o workshop'),
    ('Emilly de Lima Cordeiro', 'emillyc125@gmail.com', 5, 'final', '24/05/2026 12:00', 'Levar saúde e qualidade de vida através do movimento.'),
    ('Gilvanildo Pereira de Oliveira', 'gilvanildo.rcc@gmail.com', 5, 'glicemico', '24/05/2026 11:59', 'Ansioso 👍'),
    ('Jalisson', 'jalissonsantos26@gmail.com', 5, 'final', '24/05/2026 11:58', 'Promover a saúde, a autonomia e a qualidade de vida das pessoas por meio do movimento. Isso transforma a atividade física em uma ferramenta essencial de bem-estar.'),
    ('Stephanie Aline de Oliveira', 'teezinha.oliveira02@gmail.com', 1, 'pressao', '24/05/2026 11:57', 'Não me sinto confortável'),
    ('Celio de Oliveira Sebastião', 'celioo@prof.educacao.sp.gov.br', 5, 'glicemico', '24/05/2026 11:57', 'Ótimo'),
    ('Emilly de Lima Cordeiro', 'emillyc125@gmail.com', 4, 'glicemico', '24/05/2026 11:56', 'Ansiosa para o conteúdo do workshop!'),
    ('Carlos Júnior de Abreu Braga', 'Carlosjuniorabreu43@gmail.com', 5, 'pressao', '24/05/2026 11:56', 'Ainda com algumas dúvidas'),
    ('Haruo', 'haruo.m.b@gmail.com', 4, 'final', '24/05/2026 11:56', 'Molhorar a qualidade de vida das pessoas.'),
    ('Meiry Ellen Estevão dos Santos', 'ellen.meiry@gmail.com', 5, 'final', '24/05/2026 11:55', 'Muito bom'),
    ('Charles Alessandro Neves', 'charles_exalta@hotmail.com', 5, 'vamos', '24/05/2026 11:54', 'Muito bom ter esse feedback antes da aula'),
    ('Paula de Freitas Brandão', 'nutripaulabrandao@gmail.com', 5, 'aplica', '24/05/2026 11:52', 'Ainda não sei o tipo de aluno, mas acho a área fascinante.'),
    ('Emilly de Lima Cordeiro', 'emillyc125@gmail.com', 4, 'pressao', '24/05/2026 11:52', 'Apesar de termos bastante estudos que falam sobre, lidar com alunos que possuem condições ligadas à pressão arterial é extremamente delicado, então ainda é necessário mais conhecimento para prescrever com mais segurança.'),
    ('Cláudio', 'claudiojrferreirapereira56@gmail.com', 5, 'vamos', '24/05/2026 11:52', 'Extremamente proveitoso'),
    ('Otávio Pereira Ferreira Sampaio', 'osampaio502@gmail.com', 5, 'aplica', '24/05/2026 11:52', 'Ótimo'),
    ('Meiry Ellen Estevão dos Santos', 'ellen.meiry@gmail.com', 5, 'glicemico', '24/05/2026 11:52', 'Muito obrigada, tudo maravilhoso'),
    ('Wellington Berbel', 'wellingtonberbel@hotmail.com', 5, 'final', '24/05/2026 11:51', 'Aprender e evoluir sempre'),
    ('Haruo', 'haruo.m.b@gmail.com', 5, 'glicemico', '24/05/2026 11:50', 'Ainda não'),
    ('Jalisson', 'jalissonsantos26@gmail.com', 5, 'glicemico', '24/05/2026 11:49', 'Não, eu não sou capaz e não posso prescrever nenhuma rotina, treino ou plano alimentar de forma autônoma para um aluno diabético. Como profissional de Educação Física, sua autonomia técnica é legal é fundamental para guiar o aluno diabético com segurança'),
    ('Silvia Regina Tonetto', 'silproff@yahoo.com.br', 5, 'aplica', '24/05/2026 11:47', 'Cardiopatas, Diabeticos e doentes neurologicos'),
    ('Meiry Ellen Estevão dos Santos', 'ellen.meiry@gmail.com', 5, 'pressao', '24/05/2026 11:46', 'Muito bom'),
    ('Isaias robert', 'losacatrapo200@gmail.com', 5, 'final', '24/05/2026 11:46', 'Muito conhecimento'),
    ('Celio de Oliveira Sebastião', 'celioo@prof.educacao.sp.gov.br', 5, 'pressao', '24/05/2026 11:46', 'Estou gostando muito.'),
    ('Wellington Berbel', 'wellingtonberbel@hotmail.com', 5, 'glicemico', '24/05/2026 11:45', 'Muito obrigado'),
    ('Luana Priscila da Silva Pereira', 'luhpsp190@gmail.com', 5, 'final', '24/05/2026 11:45', 'Ser Diferenciada.'),
    ('Emilly de Lima Cordeiro', 'emillyc125@gmail.com', 4, 'aplica', '24/05/2026 11:45', 'Trabalho com a terceira idade, que em sua grande maioria possui hipertensão.'),
    ('Otávio Pereira Ferreira Sampaio', 'osampaio502@gmail.com', 5, 'vamos', '24/05/2026 11:45', 'Ótimo'),
    ('Rodolfo Campos Cardoso', 'rodolfocardoso_155@hotmail.com', 5, 'vamos', '24/05/2026 11:45', 'Muito didático e prático. Com certeza o conteúdo será muito bem explicado e orientado de maneira prática e eficaz!!!'),
    ('Isaias robert', 'losacatrapo200@gmail.com', 5, 'glicemico', '24/05/2026 11:44', 'workshop muito bom'),
    ('Carlos Júnior de Abreu Braga', 'Carlosjuniorabreu43@gmail.com', 5, 'aplica', '24/05/2026 11:44', 'Hipertensos'),
    ('Meiry Ellen Estevão dos Santos', 'ellen.meiry@gmail.com', 5, 'aplica', '24/05/2026 11:44', 'Maravilhoso'),
    ('Carla Naiara voltolini sales', 'ro89ca95@gmail.com', 5, 'final', '24/05/2026 11:44', 'Meu maior objetivo é ver a melhor constante em meus alunos, ver eles conseguindo ou voltando a fazer coisas simples na vida como poder caminhar, sentar ou levantar sem sentir dor poder voltar a fazer coisas simples que não era mais possíveis'),
    ('Haruo', 'haruo.m.b@gmail.com', 5, 'pressao', '24/05/2026 11:44', 'Ainda com algumas dúvidas'),
    ('Eduardo Natividade Luiz', 'natividadeestudio@gmail.com', 5, 'final', '24/05/2026 11:43', 'Fazer a diferença na vida das pessoas'),
    ('Luana Priscila da Silva Pereira', 'luhpsp190@gmail.com', 5, 'glicemico', '24/05/2026 11:43', 'Ótimo'),

    # === LOTE 6 (24/05/2026 — 11:42 madrugada -> 02:55) ===
    ('Juna Yuri Oshikawa Zacarin', 'junayuri@gmail.com', 5, 'vamos', '24/05/2026 11:42', 'Muito bom!'),
    ('Isaias robert', 'losacatrapo200@gmail.com', 5, 'pressao', '24/05/2026 11:42', 'show'),
    ('Wellington Berbel', 'wellingtonberbel@hotmail.com', 4, 'pressao', '24/05/2026 11:40', 'Forte'),
    ('Haruo', 'haruo.m.b@gmail.com', 4, 'aplica', '24/05/2026 11:40', 'Ainda com nenhum'),
    ('Jonathan Cristorf Camargo', 'jcristorf@gmail.com', 5, 'final', '24/05/2026 11:39', 'Ajudar as pessoas'),
    ('Emilly de Lima Cordeiro', 'emillyc125@gmail.com', 5, 'vamos', '24/05/2026 11:39', 'Super didático e explicativo!'),
    ('Celio de Oliveira Sebastião', 'celioo@prof.educacao.sp.gov.br', 5, 'aplica', '24/05/2026 11:39', 'Ótimo.'),
    ('Meiry Ellen Estevão dos Santos', 'ellen.meiry@gmail.com', 5, 'vamos', '24/05/2026 11:39', 'Muito bem explicado'),
    ('Gilvanildo Pereira de Oliveira', 'gilvanildo.rcc@gmail.com', 5, 'pressao', '24/05/2026 11:39', 'Boa'),
    ('Isaias robert', 'losacatrapo200@gmail.com', 5, 'aplica', '24/05/2026 11:38', 'muito top'),
    ('Stephanie Aline de Oliveira', 'teezinha.oliveira02@gmail.com', 5, 'aplica', '24/05/2026 11:38', 'Hipertensos e diabéticos'),
    ('Isadora Maria Pereira Felix Rolim', 'misadora199@gmail.com', 5, 'final', '24/05/2026 11:38', 'Ser um profissional diferenciado'),
    ('Eduardo Natividade Luiz', 'natividadeestudio@gmail.com', 5, 'glicemico', '24/05/2026 11:38', 'Durante minha graduação eu me aprofundei em diabetes, realizei estagio e trabalhos na associação dos diabéticos da minha cidade'),
    ('José Carlos De Oliveira', 'Jcbraganey@gmail.com', 5, 'pressao', '24/05/2026 11:38', 'Muito aprendizado.'),
    ('Jonathan Cristorf Camargo', 'jcristorf@gmail.com', 5, 'glicemico', '24/05/2026 11:37', 'Sim'),
    ('Carlos Júnior de Abreu Braga', 'Carlosjuniorabreu43@gmail.com', 5, 'vamos', '24/05/2026 11:37', 'Muito bom'),
    ('Iasmin Rios Piterskih', 'iasminrios48@gmail.com', 5, 'final', '24/05/2026 11:37', 'Levar saúde e alegria aos meus alunos'),
    ('Alfredo Tadeu Salvo', 'atsalvo@gmail.com', 5, 'aplica', '24/05/2026 11:37', 'Todos'),
    ('Jalisson', 'jalissonsantos26@gmail.com', 5, 'pressao', '24/05/2026 11:37', 'Primeiramente fazer uma boa avaliação anamnese, O processo de anamnese costuma responder por cerca de 80 a 90% da formulação de hipóteses diagnósticas.'),
    ('Josimone Maciel', 'personaltrainer_josi@yahoo.com.br', 4, 'final', '24/05/2026 11:35', 'Bom'),
    ('Isadora Maria Pereira Felix Rolim', 'misadora199@gmail.com', 5, 'glicemico', '24/05/2026 11:35', 'Não'),
    ('Jonathan Cristorf Camargo', 'jcristorf@gmail.com', 5, 'pressao', '24/05/2026 11:35', 'Capacitado'),
    ('Isaias robert', 'losacatrapo200@gmail.com', 5, 'vamos', '24/05/2026 11:35', 'muito boom'),
    ('Paula de Freitas Brandão', 'nutripaulabrandao@gmail.com', 5, 'vamos', '24/05/2026 11:34', 'Estou achando incrível!!'),
    ('Luana Priscila da Silva Pereira', 'luhpsp190@gmail.com', 5, 'pressao', '24/05/2026 11:34', 'Hoje tenho mais segurança.'),
    ('Iasmin Rios Piterskih', 'iasminrios48@gmail.com', 5, 'glicemico', '24/05/2026 11:34', 'Sim'),
    ('Jonathan Cristorf Camargo', 'jcristorf@gmail.com', 5, 'aplica', '24/05/2026 11:34', 'idosos'),
    ('Carla Naiara voltolini sales', 'ro89ca95@gmail.com', 5, 'glicemico', '24/05/2026 11:33', 'Ainda não me sinto capaz de prescrever o treino pela manhã para um diabético por vários fatores .'),
    ('Eduardo Natividade Luiz', 'natividadeestudio@gmail.com', 5, 'pressao', '24/05/2026 11:33', 'É muito importante controlar a pressão arterial'),
    ('ANDRÉA LOPES DE SOUSA BARRETO', 'andreabarretopb@gmail.com', 5, 'aplica', '24/05/2026 11:32', 'Idosos, doenças crônicas, doenças músculos-esqueléticas, Alzheimer e outras patologias.'),
    ('Celio de Oliveira Sebastião', 'celioo@prof.educacao.sp.gov.br', 5, 'vamos', '24/05/2026 11:32', 'Muito bom .'),
    ('Wellington Berbel', 'wellingtonberbel@hotmail.com', 1, 'aplica', '24/05/2026 11:31', 'Atuo com grupo grande, difícil fazer avaliação!'),
    ('Isadora Maria Pereira Felix Rolim', 'misadora199@gmail.com', 5, 'pressao', '24/05/2026 11:31', 'Ainda não me sinto bem preparada'),
    ('Jonathan Cristorf Camargo', 'jcristorf@gmail.com', 5, 'vamos', '24/05/2026 11:31', 'otimo'),
    ('Iasmin Rios Piterskih', 'iasminrios48@gmail.com', 5, 'pressao', '24/05/2026 11:30', 'Me sinto insegura'),
    ('Josimone Maciel', 'personaltrainer_josi@yahoo.com.br', 5, 'glicemico', '24/05/2026 11:30', 'boa'),
    ('Thiago Martinho Pereira', 'Thiaguinho.martinho@gmail.com', 5, 'final', '24/05/2026 11:30', 'Bom'),
    ('Larissa Franciele Roque', 'larif.roque@gmail.com', 5, 'vamos', '24/05/2026 11:30', 'Muito didático.'),
    ('Beatriz Postal Costa', 'Beatriz.postal88@gmail.com', 5, 'vamos', '24/05/2026 11:29', 'Conhecimento nunca é demais!!!'),
    ('Gilvanildo Pereira de Oliveira', 'gilvanildo.rcc@gmail.com', 4, 'aplica', '24/05/2026 11:29', 'Pretendo ter um leque de opções de aluno'),
    ('Armando Lima e Silva Corujeira Junior', 'corujeira@gmail.com', 5, 'vamos', '24/05/2026 11:29', 'Excelente.'),
    ('Silvia Regina Tonetto', 'silproff1@yahoo.com.br', 5, 'vamos', '24/05/2026 11:29', 'ansiosa por começar a me aprofundar em conhecimentos e atender cada vez melhor meu grupo especial❤️'),
    ('Mauro', 'maurolaurindo@professor.educacao.sp.gov.br', 5, 'vamos', '24/05/2026 11:28', 'Top'),
    ('Iasmin Rios Piterskih', 'iasminrios48@gmail.com', 5, 'aplica', '24/05/2026 11:27', 'Idosos'),
    ('Jalisson', 'jalissonsantos26@gmail.com', 5, 'aplica', '24/05/2026 11:27', 'Pessoas idosos'),
    ('Thiago Martinho Pereira', 'Thiaguinho.martinho@gmail.com', 5, 'glicemico', '24/05/2026 11:27', 'Bom'),
    ('Isadora Maria Pereira Felix Rolim', 'misadora199@gmail.com', 5, 'aplica', '24/05/2026 11:27', 'Idosos'),
    ('Haruo', 'haruo.m.b@gmail.com', 5, 'vamos', '24/05/2026 11:26', 'Muito bom, informações claras e fáceis de compreender.'),
    ('Eduardo Natividade Luiz', 'natividadeestudio@gmail.com', 5, 'aplica', '24/05/2026 11:26', 'Eu atendo idosos, e atualmente uma gestante'),
    ('Iasmin Rios Piterskih', 'iasminrios48@gmail.com', 5, 'vamos', '24/05/2026 11:26', 'Amei'),
    ('Thiago Martinho Pereira', 'Thiaguinho.martinho@gmail.com', 5, 'pressao', '24/05/2026 11:24', 'Bom'),
    ('Monique Nicole Alves da Silva', 'alvesmoniquenicole@gmail.com', 5, 'vamos', '24/05/2026 11:23', '-'),
    ('Carla Naiara voltolini sales', 'ro89ca95@gmail.com', 5, 'pressao', '24/05/2026 11:21', 'Após entender melhor o assunto me sinto capacitada pois somos responsáveis direitos na melhora do aluno.'),
    ('Thiago Martinho Pereira', 'Thiaguinho.martinho@gmail.com', 5, 'aplica', '24/05/2026 11:20', 'Bom'),
    ('Josimone Maciel', 'personaltrainer_josi@yahoo.com.br', 4, 'pressao', '24/05/2026 11:18', 'Me sinto qualificado, mas nao 100% confiante ainda.'),
    ('Luiz Carlos Fernandes', 'cinemaluprofluiz@gmail.com', 5, 'final', '24/05/2026 11:18', 'Segurança e competência'),
    ('Thiago Martinho Pereira', 'Thiaguinho.martinho@gmail.com', 5, 'vamos', '24/05/2026 11:17', 'Bos'),
    ('Eduardo Natividade Luiz', 'natividadeestudio@gmail.com', 5, 'vamos', '24/05/2026 11:17', 'Muito obrigado, e ótimo conteúdo'),
    ('William Olielo Pereira', 'williams.olielo@gmail.com', 5, 'vamos', '24/05/2026 11:15', 'Muito interessante como o conhecimento do curso está sendo conduzido!'),
    ('Ana Karolina de Almeida', 'anakarolinaapg18@gmail.com', 5, 'vamos', '24/05/2026 11:15', 'Adorei! Muito bem explicativo e educativo.'),
    ('Alfredo Tadeu Salvo', 'atsalvo@gmail.com', 5, 'vamos', '24/05/2026 11:15', 'É um ensino maravilhoso, gratidão'),
    ('Carla Naiara voltolini sales', 'ro89ca95@gmail.com', 5, 'aplica', '24/05/2026 11:13', 'Com os dois tipos de grupos especiais'),
    ('Carla Mabila de Oliveira', 'mabilaolveira12@gmail.com', 3, 'vamos', '24/05/2026 11:10', 'Vamos lá! Conhecimento é sempre bem vindo!'),
    ('Daniel', 'thedanis013@gmail.com', 5, 'vamos', '24/05/2026 11:08', 'Todo conhecimento é válido, para compreender melhor sobre a amplitude da área da saúde e educação física.'),
    ('Jorge Katsuo Nishimura de Andrade', 'jorgekatsuofdc@gmail.com', 5, 'final', '24/05/2026 11:07', '-'),
    ('Josimone Maciel', 'personaltrainer_josi@yahoo.com.br', 4, 'aplica', '24/05/2026 11:05', 'Estou gostando'),
    ('Jorge Katsuo Nishimura de Andrade', 'jorgekatsuofdc@gmail.com', 5, 'glicemico', '24/05/2026 11:04', '-'),
    ('Carla Naiara voltolini sales', 'ro89ca95@gmail.com', 5, 'vamos', '24/05/2026 11:03', 'Ótima explicação'),
    ('Rafaela Castellanos', 'rafapilatespersonal@gmail.com', 5, 'pressao', '24/05/2026 11:02', 'Sinto parcialmente segura. Gostaria de algumas orientações como protocolos e equipamentos adequados para acompanhar atendimento do idoso em casa'),
    ('Juscelino Rodrigues Lima', 'jorgejuscelino40@gmail.com', 5, 'final', '24/05/2026 11:02', 'Meu objetivo é me tornar referência em prescrição de treino para grupos especiais, oferecendo resultados com segurança e excelência.'),
    ('Emilio', 'ignatievo@yahoo.com.br', 4, 'glicemico', '24/05/2026 11:02', 'Sinto-me mais seguro.'),
    ('Cicero Galdino Nascimento da Silva', 'cicerogaldino09@gmail.com', 5, 'vamos', '24/05/2026 11:01', 'muito boom o conteudo'),
    ('Jenmey Yen', 'j3nm3y.y3n@gmail.com', 5, 'aplica', '24/05/2026 11:01', 'Desejo trabalhar com grupos especiais da melhor idade, grupos dos 50+'),
    ('Hugo Rodrigo', 'prof.hugorodrigo@gmail.com', 4, 'aplica', '24/05/2026 10:59', 'Idosos geralmente com ponte de safena e marcapasso'),
    ('Jorge Katsuo Nishimura de Andrade', 'jorgekatsuofdc@gmail.com', 5, 'pressao', '24/05/2026 10:59', '-'),
    ('Carlos Matsuo', 'fisiologista.carlosjr@gmail.com', 5, 'final', '24/05/2026 10:58', 'Servir as pessoas.'),
    ('Naiala Ferreira de Oliveira', 'nanaixavier@gmail.com', 4, 'final', '24/05/2026 10:58', 'Sentir segurança em minha atuação profissional.'),
    ('João Paulo Ribeiro Ferreira', 'Jhoni1034@yahoo.com', 4, 'pressao', '24/05/2026 10:58', 'Bom'),
    ('Fabio Tanabe', 'fabio.kazu@yahoo.com.br', 5, 'vamos', '24/05/2026 10:58', 'Precisamos muito conhecimento e segurança para trabalhar com este grupo de pessoas.'),
    ('Luiz Carlos Fernandes', 'cinemaluprofluiz@gmail.com', 5, 'glicemico', '24/05/2026 10:57', 'Ok'),
    ('Juscelino Rodrigues Lima', 'jorgejuscelino40@gmail.com', 5, 'glicemico', '24/05/2026 10:56', 'Eu já estou trabalhando com pessoas assim aais de 25 anos só que é sempre bom ter reflexões sobre os assuntos. O conteúdo abriu minha visão sobre o controle glicêmico e a importância da prescrição correta para alunos diabéticos. Me sinto muito mais preparado para aplicar isso na prática.'),
    ('Ricardo Filho', 'kakapersonal@hotmail.com', 5, 'final', '24/05/2026 10:56', 'Meu propósito é ajudar as pessoas a transformarem a vida com exercício físico!'),
    ('Lucia Helena Rodrigues Couto', 'efucinha@gmail.com', 4, 'final', '24/05/2026 10:55', 'Proporcionar qualidade de vida aos meus alunos, com segurança e conhecimento!!!'),
    ('Emilio', 'ignatievo@yahoo.com.br', 4, 'pressao', '24/05/2026 10:55', 'Mais confiante.'),
    ('Daniela Bruniera Arruda', 'danifazenda16@gmail.com', 5, 'final', '24/05/2026 10:54', 'Conhecimento é tudo'),
    ('Sidney Amancio da Silva', 'sidney0511daniela@gmail.com', 4, 'glicemico', '24/05/2026 10:54', 'Isso que eu espero'),
    ('Stephani Souza de Oliveira', 'phanyoliveira29@gmail.com', 5, 'vamos', '24/05/2026 10:53', 'Gostei'),
    ('Marco Jim Gui Vallin', 'marcojm.treinador@gmail.com', 5, 'vamos', '24/05/2026 10:52', 'Conhecimento de introdução, curto, mas abre a curiosidade para iniciar curso.'),
    ('Jenmey Yen', 'j3nm3y.y3n@gmail.com', 5, 'vamos', '24/05/2026 10:52', 'Parabéns a toda equipe por disponibilizar eventos como este e materiais de qualidade que possam agregar conhecimento e nos tornar profissionais qualificados e capacitados'),
    ('Tatiane Hernandes', 'tati_hernandes@hotmail.com', 3, 'aplica', '24/05/2026 10:50', 'trabalho com idosos com patologias como diabetes e hipertensao.'),
    ('Juliana balabenute faci', 'Jubafefa@yahoo.com.br', 5, 'final', '24/05/2026 10:49', 'Prescrever exercícios físicos com embasamento científico, para gerar efetividade'),
    ('F', 'fatimacestari2017@gmail.com', 5, 'vamos', '24/05/2026 10:49', 'Atualizar- se frequentemente.'),
    ('Emilio', 'ignatievo@yahoo.com.br', 5, 'aplica', '24/05/2026 10:49', 'cardiopatas e pessoas com doenças crônicas'),
    ('Lucia Helena Rodrigues Couto', 'efucinha@gmail.com', 3, 'glicemico', '24/05/2026 10:49', 'Sinto ainda que preciso de mais ferramentas para me sentir segura na prescrição de exercícios...'),
    ('Ana Claudia Arvani', 'ac-arvani@uol.com.br', 3, 'aplica', '24/05/2026 10:48', 'Cardiopata'),
    ('Naiala Ferreira de Oliveira', 'nanaixavier@gmail.com', 1, 'glicemico', '24/05/2026 10:48', 'Ainda não me sinto pronta.'),
    ('Carlos Matsuo', 'fisiologista.carlosjr@gmail.com', 5, 'glicemico', '24/05/2026 10:47', 'Sim, pois claramente foi explicado o processo. Se seguir essa sequência de informações não há problemas sérios com o aluno. Cabe ao profissional desenvolver o processo do seu protocolo de atendimento e fazer as observações e perguntas corretas ao aluno antes do treino.'),
    ('João Paulo Ribeiro Ferreira', 'Jhoni1034@yahoo.com', 4, 'aplica', '24/05/2026 10:47', 'Muito bom.'),
    ('Daniela Bruniera Arruda', 'danifazenda16@gmail.com', 5, 'aplica', '24/05/2026 10:45', 'Essencial os aprendizados de hoje, pode salvar vidas.'),
    ('Rafaela Castellanos', 'rafapilatespersonal@gmail.com', 5, 'aplica', '24/05/2026 10:44', 'Eu trabalho com alunos 60+ muitos tem diversas patologias. Diabete pressão alta artrose. Minha duvida é fazer aula para um aluno que sofre principalmente DOR crônica pela artrose'),
    ('Juliana balabenute faci', 'Jubafefa@yahoo.com.br', 5, 'glicemico', '24/05/2026 10:42', 'Não'),
    ('Emilio', 'ignatievo@yahoo.com.br', 3, 'vamos', '24/05/2026 10:41', 'Interessado em seguir aprendendo.'),
    ('Josimone Maciel', 'personaltrainer_josi@yahoo.com.br', 4, 'vamos', '24/05/2026 10:40', 'curioso pelo aprendizado do workshop'),
    ('Jorge Katsuo Nishimura de Andrade', 'jorgekatsuofdc@gmail.com', 5, 'aplica', '24/05/2026 10:40', 'Excelente conteúdo'),
    ('Luiz Carlos Fernandes', 'cinemaluprofluiz@gmail.com', 5, 'pressao', '24/05/2026 10:39', 'Seguro'),
    ('Josias Vieira Camargo', 'josias.camargo@hotmail.com', 5, 'final', '24/05/2026 10:37', 'Ser útil ao próximo.'),
    ('João Paulo Ribeiro Ferreira', 'Jhoni1034@yahoo.com', 4, 'vamos', '24/05/2026 10:33', 'Muito bom os conteúdos aqui aplicados'),
    ('Juliana balabenute faci', 'Jubafefa@yahoo.com.br', 5, 'pressao', '24/05/2026 10:33', 'Tenho um conhecimento de base da faculdade, porém os estudo hoje esta me embasando melhor o que seguir'),
    ('Josias Vieira Camargo', 'josias.camargo@hotmail.com', 5, 'glicemico', '24/05/2026 10:32', 'Sim.'),
    ('Cassiano Leal', 'lealcassiano@gmail.com', 5, 'final', '24/05/2026 10:30', 'Pronto para evoluir no meu conhecimento sobre esse público que só vai crescer e crescer.'),
    ('Jorge Silveira', 'jwps1989@gmail.com', 4, 'aplica', '24/05/2026 10:30', 'Hipertensos e diabéticos.'),
    ('Pedro Paulo da Silva', 'pedropaulonovavida26@gmail.com', 5, 'final', '24/05/2026 10:30', 'Salvar vidas'),
    ('Richard Cristiano Mendes', 'richard.mendes148@gmail.com', 5, 'vamos', '24/05/2026 10:29', 'Muito bom, são questões que sempre foram importantes para área'),
    ('Jorge Silveira', 'jwps1989@gmail.com', 5, 'vamos', '24/05/2026 10:27', 'Conteúdo atual e, muito importante.'),
    ('Cassiano Leal', 'lealcassiano@gmail.com', 5, 'glicemico', '24/05/2026 10:24', 'Muito interessante conhecer profundamente minha doença, diabetes tipo 1'),
    ('Tatiane Hernandes', 'tati_hernandes@hotmail.com', 5, 'vamos', '24/05/2026 10:24', 'conteudo simplificado e com muita clareza.'),
    ('Pedro Paulo da Silva', 'pedropaulonovavida26@gmail.com', 5, 'glicemico', '24/05/2026 10:21', 'Ainda não'),
    ('Thabata Lang', 'thabata.lang@gmail.com', 3, 'pressao', '24/05/2026 10:20', 'Não muito'),
    ('Martinho dos Santos Araújo Junior', 'martinhoaraujo75@gmail.com', 5, 'final', '24/05/2026 10:20', 'Obrigado'),
    ('Luiz Carlos Fernandes', 'cinemaluprofluiz@gmail.com', 5, 'aplica', '24/05/2026 10:19', 'Idosos'),
    ('Nilson Bastos Hendel', 'hendelnbh_@hotmail.com', 5, 'aplica', '24/05/2026 10:19', 'Estou iniciando. Ainda não trabalho com grupos de alunos específicos.'),
    ('Rafaela Castellanos', 'rafapilatespersonal@gmail.com', 5, 'vamos', '24/05/2026 10:18', 'Muito legal a gameficacao'),
    ('Martinho dos Santos Araújo Junior', 'martinhoaraujo75@gmail.com', 5, 'glicemico', '24/05/2026 10:17', 'Obrigado'),
    ('Jorge Katsuo Nishimura de Andrade', 'jorgekatsuofdc@gmail.com', 5, 'vamos', '24/05/2026 10:16', 'Mto interessante o conteudo'),
    ('Gilvanildo Pereira de Oliveira', 'gilvanildo.rcc@gmail.com', 5, 'vamos', '24/05/2026 10:16', 'Vejo muito em outros personais atendendo aquele público de sempre, difícil ver alguém de fato com comorbidades'),
    ('Pedro Paulo da Silva', 'pedropaulonovavida26@gmail.com', 5, 'pressao', '24/05/2026 10:15', 'Pré preparado'),
    ('Martinho dos Santos Araújo Junior', 'martinhoaraujo75@gmail.com', 5, 'pressao', '24/05/2026 10:14', 'O'),
    ('Nelson Marques da Silva', 'profnelsonsilva@gmail.com', 5, 'vamos', '24/05/2026 10:14', 'Vamos se capacitar ainda mais'),
    ('Martinho dos Santos Araújo Junior', 'martinhoaraujo75@gmail.com', 5, 'aplica', '24/05/2026 10:12', 'Obrigado'),
    ('Juliana balabenute faci', 'Jubafefa@yahoo.com.br', 5, 'aplica', '24/05/2026 10:10', 'Cardíacos'),
    ('Naiala Ferreira de Oliveira', 'nanaixavier@gmail.com', 1, 'pressao', '24/05/2026 10:10', 'Não me sinto apta no momento.'),
    ('Lucia Helena Rodrigues Couto', 'efucinha@gmail.com', 3, 'pressao', '24/05/2026 10:10', 'Prescrevo com um pouco mais de conhecimento, mas ainda preciso de tempo de estudo para prescrever c segurança e confiança....'),
    ('Martinho dos Santos Araújo Junior', 'martinhoaraujo75@gmail.com', 5, 'vamos', '24/05/2026 10:07', 'Obrigado'),
    ('Pedro Paulo da Silva', 'pedropaulonovavida26@gmail.com', 5, 'aplica', '24/05/2026 10:06', 'Idosos'),
    ('Renan da Silva Ramos', 'reenan.ramos18@gmail.com', 5, 'pressao', '24/05/2026 10:03', 'Com muito mais conhecimento'),
    ('Sidney Amancio da Silva', 'sidney0511daniela@gmail.com', 4, 'pressao', '24/05/2026 09:55', 'Percebi que tenho que focar e buscar compreender realmente o público especial'),
    ('Lucas Guimarães Braga', 'lucasbraga92@live.com', 5, 'final', '24/05/2026 09:46', 'Cuidar da saúde'),
    ('Nilson Bastos Hendel', 'hendelnbh_@hotmail.com', 5, 'vamos', '24/05/2026 09:44', 'Até aqui comecei a compreender como aplicar conhecimento durante as práticas de exercício para grupos especiais. Comecei a ter as primeiras noções e quero aprender muito mais.'),
    ('Lucas Guimarães Braga', 'lucasbraga92@live.com', 5, 'glicemico', '24/05/2026 09:43', 'Para diabéticos acho que não'),
    ('Lucas Guimarães Braga', 'lucasbraga92@live.com', 5, 'pressao', '24/05/2026 09:38', 'Muito bem'),
    ('luzieti', 'luzieti44@gmail.com', 5, 'vamos', '24/05/2026 09:35', 'Estou gostando muito'),
    ('Lucia Helena Rodrigues Couto', 'efucinha@gmail.com', 4, 'aplica', '24/05/2026 09:11', 'Quero trabalhar c diabéticos, para ajudá-los, através do exercício físico, ganharem qualidade de vida e menos medicação ... Hipertensos, qdo me sentir mais capacitada e segura, através de aprendizado como esse workshop e especializações...'),
    ('Aline', 'Aline.al.alcantara@gmail.com', 5, 'final', '24/05/2026 09:07', 'Melhorar a vida das pessoas'),
    ('Fabricio Lazarini da Silva', 'fabriciolazarini@yahoo.com.br', 1, 'aplica', '24/05/2026 09:06', 'Gostaria de atuar com hipertensão'),
    ('Thabata Lang', 'thabata.lang@gmail.com', 4, 'aplica', '24/05/2026 09:01', 'Idosos'),
    ('Anderson Angelo Gomes Da Silva', 'andersonangelo24361@gmail.com', 5, 'vamos', '24/05/2026 08:56', 'Ótimo conteúdo'),
    ('Lucia Helena Rodrigues Couto', 'efucinha@gmail.com', 4, 'vamos', '24/05/2026 07:56', 'A jornada de aprendizado me pareceu até aqui, pautada em conteúdo planejado e estruturado em diretrizes clínicas de segurança'),
    ('Thabata Lang', 'thabata.lang@gmail.com', 4, 'vamos', '24/05/2026 07:21', 'Vamos6'),
    ('Aline', 'Aline.al.alcantara@gmail.com', 5, 'glicemico', '24/05/2026 07:07', 'Excelente'),
    ('Maycon acunha', 'Mayconacunha@gmail.com', 5, 'final', '24/05/2026 06:58', 'Impactar e mudar vidas'),
    ('Aline', 'Aline.al.alcantara@gmail.com', 5, 'pressao', '24/05/2026 06:50', 'Ainda insegura'),
    ('Maycon acunha', 'Mayconacunha@gmail.com', 5, 'glicemico', '24/05/2026 06:49', 'Mais ou menos'),
    ('Vanessa de Lima Marins', 'vanessa_delima_marins@hotmail.com', 5, 'final', '24/05/2026 06:27', 'Aprender e evoluir'),
    ('Vanessa de Lima Marins', 'vanessa_delima_marins@hotmail.com', 5, 'glicemico', '24/05/2026 06:23', 'Amando'),
    ('Maycon acunha', 'Mayconacunha@gmail.com', 5, 'pressao', '24/05/2026 06:13', 'Mais confiante'),
    ('Vanessa de Lima Marins', 'vanessa_delima_marins@hotmail.com', 5, 'pressao', '24/05/2026 05:58', 'Ainda não apta'),
    ('Vanessa de Lima Marins', 'vanessa_delima_marins@hotmail.com', 5, 'aplica', '24/05/2026 05:42', 'Hipertenso e diabéticos'),
    ('Vanessa de Lima Marins', 'vanessa_delima_marins@hotmail.com', 5, 'vamos', '24/05/2026 05:33', 'Estou amando o app'),
    ('José Carlos De Oliveira', 'Jcbraganey@gmail.com', 5, 'aplica', '24/05/2026 04:27', '3ª idade'),
    ('Gabriela Ayumi Yano', 'gabriela.yano21@gmail.com', 1, 'aplica', '24/05/2026 04:13', 'Ainda não decidi específicamente com qual tipo de aluno pretendo trabalhar, mas gosto da ideia de que poderei ajudar qualquer um deles.'),
    ('Gabriela Ayumi Yano', 'gabriela.yano21@gmail.com', 5, 'vamos', '24/05/2026 03:43', 'Esse módulo introduz os assuntos a serem estudados posteriormente, dando uma ideia geral da importância de entender a fisiologia de pessoas com doenças crônicas, que necessitam de uma atenção diferenciada.'),
    ('Marliza Canal Peres', 'canalmarliza@gmail.com', 5, 'final', '24/05/2026 03:32', 'Contribuir para o bem estar fisico e mental daqueles que me procuram em busca de saúde e uma melhor qualidade de vida.'),
    ('Everton Capitanio', 'evertoncapitanio@yahoo.com.br', 5, 'final', '24/05/2026 03:23', 'Manter-me sempre atualizado!'),
    ('Henrique Xavier Ferreira de Lima', 'hxfl21@yahoo.com.br', 5, 'vamos', '24/05/2026 03:20', 'Didático.'),
    ('Everton Capitanio', 'evertoncapitanio@yahoo.com.br', 4, 'glicemico', '24/05/2026 03:15', 'Aguardando o conteúdo do workshop para deixar mais claro as situações do dia a dia dos treinos.'),
    ('Marliza Canal Peres', 'canalmarliza@gmail.com', 3, 'glicemico', '24/05/2026 03:14', 'Me sinto com pouca autonomia.'),
    ('Arivane Batista do Nascimento', 'Arivanebatista@gmail.com', 5, 'final', '24/05/2026 03:06', 'Ajudar e mudar vidas'),
    ('Everton Capitanio', 'evertoncapitanio@yahoo.com.br', 4, 'pressao', '24/05/2026 03:05', 'Por se tratar de uma situação individual, diversos cenários são possíveis e algumas dúvidas surgem na tomada de decisão.'),
    ('Aline', 'Aline.al.alcantara@gmail.com', 5, 'aplica', '24/05/2026 03:04', 'Idosos'),
    ('Marcio Claudio Gaefke', 'marciovidaativa@gmail.com', 5, 'final', '24/05/2026 03:03', 'Salvar vidas e promover saúde e bem estar, combatendo, prevenindo e tratando as doenças crônicas, ser um autêntico promotor de saúde!'),
    ('Marcio Claudio Gaefke', 'marciovidaativa@gmail.com', 5, 'glicemico', '24/05/2026 02:56', 'Sim me sinto apto, trabalho com alunos com diabetes tipo 2, estou querendo sempre me aperfeiçoar!'),
    ('Arivane Batista do Nascimento', 'Arivanebatista@gmail.com', 5, 'glicemico', '24/05/2026 02:56', 'Sim, uma prescrição bem estruturada e eficaz, prezando e valorizando sempre a qualidade de vida.'),
    ('Everton Capitanio', 'evertoncapitanio@yahoo.com.br', 4, 'aplica', '24/05/2026 02:55', 'Trabalho, especificamente, com o público acima de 60 anos que, geralmente, apresentam alteração cardiacas.'),
]


# ===================== TAGS =====================
# Cada tag aponta para uma categoria + label visivel.
# A deteccao usa keywords (case + accent insensitive) presentes no texto do comment.
TAG_CATALOG = OrderedDict([
    # PAIN: dores e friccoes do lead
    ('medo',            {'label': 'Medo de prescrever',  'category': 'pain'}),
    ('inseguro',        {'label': 'Insegurança',         'category': 'pain'}),
    ('duvida',          {'label': 'Tem dúvida',          'category': 'pain'}),
    ('critica-formato', {'label': 'Crítica ao formato',  'category': 'pain'}),
    ('logistica',       {'label': 'Logística difícil',   'category': 'pain'}),

    # GOAL: aspiracoes e objetivos
    ('ganhar-dinheiro', {'label': 'Quer ganhar dinheiro','category': 'goal'}),
    ('ser-referencia',  {'label': 'Quer ser referência', 'category': 'goal'}),
    ('mercado',         {'label': 'Vê oportunidade no mercado', 'category': 'goal'}),
    ('pediu-mais',      {'label': 'Quer mais conteúdo',  'category': 'goal'}),
    ('atualizacao',     {'label': 'Busca atualização',   'category': 'goal'}),

    # CLINICAL: publico que atende ou quer atender
    ('atende-idosos',       {'label': 'Atende idosos',       'category': 'clinical'}),
    ('atende-hipertensos',  {'label': 'Hipertensos',         'category': 'clinical'}),
    ('atende-diabeticos',   {'label': 'Diabéticos',          'category': 'clinical'}),
    ('atende-cardiacos',    {'label': 'Cardíacos',           'category': 'clinical'}),
    ('atende-oncologicos',  {'label': 'Oncológicos',         'category': 'clinical'}),
    ('comorbidades',        {'label': 'Comorbidades múltiplas', 'category': 'clinical'}),
    ('reabilitacao',        {'label': 'Reabilitação',        'category': 'clinical'}),
    ('obesidade',           {'label': 'Obesidade',           'category': 'clinical'}),

    # HOT: lead quente (alta probabilidade de fechar)
    ('cliente-atual',   {'label': 'Já é aluno Adapta',  'category': 'hot'}),
    ('preparado',       {'label': 'Já se sente preparado','category': 'hot'}),

    # NEUTRAL: contexto util mas neutro
    ('iniciante',       {'label': 'Quer começar no nicho','category': 'neutral'}),
    ('ansiedade',       {'label': 'Ansioso pelo curso', 'category': 'neutral'}),
])

# Keywords sem acento, lower-case. Match substring tolerante a acentos.
TAG_KEYWORDS = {
    'medo':            ['medo de prescrever', 'medo', 'tenho medo'],
    'inseguro':        ['insegura', 'inseguro', 'nao me sent', 'nao me sinto', 'pouco de duvida na pratica', 'nao tenho confianca', 'nao sentiria confiante', 'nao me sentia confiante'],
    'duvida':          ['duvida', 'preciso aprender', 'me aprofundar', 'tenho que aprofundar', 'preciso saber', 'preciso me aprofundar'],
    'critica-formato': ['so vi explicacoes', 'esperava', 'introdutorio', 'so recebi orientacoes', 'achei que teria', 'nota agora e muito cedo', 'nao tem muito o que falar'],
    'logistica':       ['interior', 'logistica', 'distancia', 'so na capital', 'morando no interior'],

    'ganhar-dinheiro': ['ganhar dinheiro', 'faturar', 'rentab'],
    'ser-referencia':  ['me tornar referencia', 'tornar referencia', 'ser referencia', 'me destacar'],
    'mercado':         ['falta de profissionais', 'muito procurada', 'mercado', 'demanda', 'oferta no mercado'],
    'pediu-mais':      ['gostaria de mais', 'mais conteudo', 'quero saber mais', 'mais informacoes', 'aprender mais', 'querendo aprender mais', 'mais aprofund', 'desejo entender mais', 'quero aprender'],
    'atualizacao':     ['atualizar', 'atualizacao', 'reciclagem', 'me atualizar'],

    'atende-idosos':       ['idosos', 'pessoas mais velhas', '60 anos', '93 anos', 'pessoal de mais idade', 'idade 40+'],
    'atende-hipertensos':  ['hipertenso', 'pressao alta', 'hipertensao', 'pressao arterial'],
    'atende-diabeticos':   ['diabetic', 'diabetes', 'glicemico', 'glicemic', 'diabete'],
    'atende-cardiacos':    ['cardiaco', 'cardiopata', 'problema cardiaco', 'frequencia cardiaca'],
    'atende-oncologicos':  ['oncologic', 'cancer'],
    'comorbidades':        ['comorbidade', 'multipatologia', 'varias patologias'],
    'reabilitacao':        ['reabilitacao', 'pos cirurgia', 'pilates ou musculacao'],
    'obesidade':           ['obesidade', 'obeso', 'sobrepeso'],

    'cliente-atual':   ['sou aluna da pos', 'sou aluno da pos', 'ja sou aluna', 'ja sou aluno', 'fiz a imersao', 'me inscrevi na black', 'aluna da pos'],
    'preparado':       ['me sinto preparado', 'me sinto bem mais seguro', 'me sinto bem e confortavel', 'me sinto capaz', 'sinto capaz da prescre', 'mim sinto capaz', 'sinto bem e confortavel'],

    'iniciante':       ['querendo comecar', 'comecar a trabalhar', 'ainda estou aprendendo', 'primeira fase', 'reingressar', 'estou aprendendo a lidar', 'iniciar um programa'],
    'ansiedade':       ['ansiosa', 'ansioso', 'empolgado', 'empolgada', 'ansiosa pelo', 'ansiosa para', 'ansioso para'],
}


def _strip_accents(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def detect_tags(text):
    """Retorna lista de tag keys que casam com o texto do comment."""
    normalized = _strip_accents((text or '').lower())
    matched = []
    for tag_key, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw in normalized:
                matched.append(tag_key)
                break
    return matched


def first_name(name):
    parts = name.strip().split()
    if not parts:
        return name
    n = parts[0]
    # Capitalize properly even if input is all caps
    return n[0].upper() + n[1:].lower() if len(n) > 1 else n.upper()


def detect_archetype(comments):
    """Detecta o arquetipo do lead pelos comentarios."""
    text = ' '.join(c['text'] for c in comments).lower()

    if any(w in text for w in ['medo', 'insegura', 'inseguro', 'não me sent', 'nao me sent', 'não sei', 'não me sinto', 'dificuldade', 'tenho dúvida', 'preciso aprender']):
        return 'medo'
    if any(w in text for w in ['referência', 'referencia', 'me tornar', 'ganhar dinheiro', 'destaque', 'reabilitação também é muito procurada', 'mercado']) and 'me sinto' not in text.split('mercado')[0] if 'mercado' in text else False:
        return 'referencia'
    # Reabilitar testes
    if any(w in text for w in ['me tornar', 'ganhar dinheiro', 'referência como profissional', 'falta de profissionais', 'muito procurada no mercado']):
        return 'referencia'
    if any(w in text for w in ['querendo começar', 'querendo comecar', 'começar a trabalhar', 'ainda estou aprendendo', 'primeira fase', 'iniciar', 'reingressar', 'estou aprendendo']):
        return 'iniciante'
    if any(w in text for w in ['só vi', 'so vi', 'esperava', 'introdutório', 'introdutorio', 'só recebi', 'so recebi', 'nota agora é muito cedo', 'não tem muito o que falar', 'achei que teria']):
        return 'cetico'
    if any(w in text for w in ['trabalho com', 'tenho alunos', 'meus alunos', 'atendo', 'já trabalho', 'ja trabalho']):
        return 'experiente'
    if len(text.strip()) < 25 or text.strip() in {'-', '.', 'tea', 'a', 'idosos', 'diabéticos', 'diabético', 'hipertensos', 'sedentários', 'reabilitação', 'bom', 'top', 'vamos lá', 'engajado', 'ótimo', 'excelente!', 'mto bom.', 'conhecimento', 'nota dez!', 'ótimo!', 'ótimo!!!', '✅✅✅', '★★★★★'}:
        return 'basico'
    return 'engajado'


def best_quote(comments):
    """Pega a frase mais 'citavel' do participante."""
    valid = [c['text'] for c in comments if 25 < len(c['text']) < 220 and c['text'] not in ['-', '.', '✅✅✅']]
    if not valid:
        # fallback: any comment >= 10 chars
        valid = [c['text'] for c in comments if len(c['text']) >= 10]
    if not valid:
        return None
    # Prefer comments with emotional words
    emotional = [t for t in valid if any(w in t.lower() for w in ['medo', 'insegura', 'inseguro', 'me sinto', 'quero', 'preciso', 'gostei', 'ansiosa', 'ansioso', 'referência', 'segurança', 'aprender'])]
    if emotional:
        return max(emotional, key=len)
    return max(valid, key=len)


OPENERS_WITH_QUOTE = [
    '{fn}, achei muito legal você ter comentado na jornada preparatória "{quote}", então:',
    '{fn}, parei pra reler o que você escreveu lá no preparatório — "{quote}" — e fui te chamar na hora. Então:',
    '{fn}, fiquei pensando no seu comentário "{quote}" da jornada. Então:',
    '{fn}, quando você escreveu "{quote}" no preparatório, vi um ponto que vale a pena conversar. Então:',
    '{fn}, ler o teu "{quote}" lá no preparatório me fez parar tudo pra te procurar. Então:',
    '{fn}, teu comentário "{quote}" na jornada diz muito sobre teu momento. Então:',
    '{fn}, olha esse trecho do que você comentou na jornada: "{quote}". Isso me leva direto a isso aqui:',
]

OPENERS_NO_QUOTE = [
    '{fn}, vi suas interações na jornada preparatória — dá pra ver que esse tema importa de verdade pra você. Então:',
    '{fn}, suas respostas no preparatório me chamaram atenção. Então:',
    '{fn}, andei olhando teu envolvimento na jornada e quis te chamar. Então:',
    '{fn}, pelo seu engajamento no preparatório, tem algo específico que faz sentido te falar. Então:',
]


def make_suggestions(p, participant_idx=0):
    """Gera lista de sugestoes de abordagem para o comercial usar com este participante."""
    archetype = detect_archetype(p['comments'])
    fn = first_name(p['name'])
    quote = best_quote(p['comments']) or ''

    # quote_short pode quebrar se o comentario for ".", "-", emoji. Usa fallback.
    quote_clean = quote.strip()
    use_quote = bool(quote_clean) and len(quote_clean) > 6 and quote_clean not in {'-', '.', '✅✅✅', '★★★★★'}

    # Trunca em fronteira natural (ponto final, virgula, ' — ') se for muito longo
    LIMIT = 130
    if len(quote_clean) > LIMIT:
        candidate = quote_clean[:LIMIT]
        # Procura um break point natural rolando pra tras
        for sep in ['. ', '! ', '? ', ', ', ' — ', '; ']:
            pos = candidate.rfind(sep)
            if pos > 40:
                candidate = candidate[:pos] + (sep.rstrip() if sep[0] in '.!?' else '')
                break
        else:
            # nenhum separador bom — quebra em espaco
            sp = candidate.rfind(' ')
            if sp > 40:
                candidate = candidate[:sp].rstrip(' ,;') + '...'
        quote_short = candidate
    else:
        quote_short = quote_clean
    # remover pontuacao terminal redundante quando vier seguido de aspas
    quote_short = quote_short.rstrip('.,;: ').strip()

    # Body templates por arquetipo (sem o nome — o opener ja saúda)
    if archetype == 'medo':
        bodies = [
            ('Identidade', 'identidade',
             'quem se preocupa em prescrever com segurança JÁ é o tipo de profissional que esse curso forma. Só falta a gente te entregar a ferramenta pra você não ter que adivinhar caso a caso. Posso te mostrar como?'),
            ('Progresso visível', 'progresso',
             'te dou um diagnóstico rápido — você já tem boa parte do conhecimento técnico. O que trava é o protocolo de avaliação inicial e a comunicação com o aluno especial na primeira sessão. O curso fecha exatamente esse gap em 3 semanas. Quer ver o passo a passo?'),
            ('Curiosidade', 'curiosidade',
             'uma pergunta antes de te oferecer qualquer coisa: você sabe o que faz a maioria dos colegas evitarem o aluno hipertenso ou diabético? Tem uma resposta específica que muda completamente como você prescreve — vale o curso inteiro. Posso te mandar?'),
            ('Status social', 'status',
             'tem muito profissional na jornada com a MESMA insegurança que a sua — só que os que entraram no curso saem prescrevendo com confiança em 6 semanas. Você quer estar nesse grupo ou continuar evitando o aluno especial?'),
            ('Perda iminente', 'perda',
             'vou ser direto — a turma com mentoria ao vivo fecha em breve. Quem entra fora pega só material gravado e perde justamente o ajuste fino de caso real, que é o que tira a insegurança. Posso garantir tua vaga?'),
        ]
    elif archetype == 'referencia':
        bodies = [
            ('Identidade', 'identidade',
             'isso não é discurso de quem só quer aprender — é de quem decidiu se posicionar. Esse curso é a ferramenta de quem ocupa o espaço de referência em grupos especiais. Posso te chamar pra detalhar?'),
            ('Status social', 'status',
             'a turma desse curso é exatamente esse perfil: profissional que vê grupos especiais como nicho de diferenciação. Tem gente do interior, da capital, e gente que já bombava em geral migrou pra cá. Quer ver quem tá na turma?'),
            ('Perda iminente', 'perda',
             'o nicho de grupos especiais tem mais demanda do que oferta qualificada — você já viu isso. A janela pra ocupar esse espaço com autoridade é AGORA, antes do mercado se inundar com gente despreparada. Posso te garantir a vaga?'),
            ('Progresso visível', 'progresso',
             'posicionamento de referência é resultado de método, não de vontade. O curso te dá os 4 pilares: avaliação clínica, prescrição segura, comunicação com médico e comunicação com aluno. Em 8 semanas você tem o pacote completo. Quer ver o roteiro?'),
            ('Curiosidade', 'curiosidade',
             'uma observação rápida — boa parte dos personals que faturam acima da média no Brasil atendem grupos especiais como nicho principal. Quer ver o dado e o porquê?'),
        ]
    elif archetype == 'iniciante':
        bodies = [
            ('Identidade', 'identidade',
             'quem decide começar pelo nicho de grupos especiais não é amador — é estratégico. Você acertou no segmento que mais ensina rápido e que tem mais demanda real. Posso te mostrar como entrar com pé direito?'),
            ('Progresso visível', 'progresso',
             'o curso é desenhado em fases — do zero (fisiologia aplicada, sem teoria desnecessária) até protocolo prático com casos reais. Você termina em 8 semanas mesmo começando agora. Quer ver a estrutura módulo por módulo?'),
            ('Pertencimento', 'pertencimento',
             'todo profissional que hoje é referência em grupos especiais começou exatamente onde você tá agora. A diferença é que eles tiveram um guia certo nos primeiros meses. Quer que esse seja o teu ponto de partida?'),
            ('Curiosidade', 'curiosidade',
             'antes de te falar do curso, te dou um spoiler: a primeira sessão com aluno especial NUNCA é avaliação física. Tem um protocolo específico de entrevista que decide 80% do resultado. Quer que eu te mande um resumo?'),
            ('Perda iminente', 'perda',
             'quem começa errado no nicho perde o primeiro aluno e desiste do segmento. Quem começa com protocolo testado tem indicação já no primeiro mês. Posso te garantir a vaga na turma com mentoria?'),
        ]
    elif archetype == 'cetico':
        bodies = [
            ('Curiosidade', 'curiosidade',
             'tua observação é válida — e é exatamente porque a maioria espera "aula gravada e pronto" que o método aqui é diferente. Tem um diferencial específico do curso que NÃO tá na jornada preparatória e muda o jogo. Quer ver qual?'),
            ('Ganho racional', 'ganho',
             'entendo o ponto. A jornada preparatória é só o gancho — o curso de fato tem 8 módulos com aulas estruturadas, mentoria semanal e estudo de caso. Posso te mandar a grade completa pra você comparar com o que esperava?'),
            ('Identidade', 'identidade',
             'profissional crítico é o tipo que mais ganha com esse curso. Você não vai engolir conteúdo solto — vai cobrar profundidade. Bom pra você, bom pra gente. Posso te chamar pra detalhar?'),
            ('Progresso visível', 'progresso',
             'te dou um plano direto — assiste a aula 1 completa (45min, protocolo de avaliação inicial). Se não justificar o investimento, a gente devolve. Quer que eu te libere o acesso?'),
            ('Perda iminente', 'perda',
             'a turma com mentoria ao vivo fecha em breve. É o componente que faz diferença pra perfil exigente como o seu — sem ela é só conteúdo gravado. Posso garantir tua vaga?'),
        ]
    elif archetype == 'experiente':
        bodies = [
            ('Identidade', 'identidade',
             'dá pra ver que você já é quem pega caso complexo na academia. Esse curso é pra você não ficar mais dependente de pesquisar a cada caso na internet ou esperar resposta de médico. Posso te mostrar como?'),
            ('Progresso (Maestria)', 'progresso',
             'você já cobre a operação básica. O que esse curso faz é refinar — prescrição com bioestatística do aluno (FC, PA, glicemia em tempo real), comunicação com equipe médica e protocolo pra casos limítrofes. É upgrade técnico. Quer ver?'),
            ('Curiosidade', 'curiosidade',
             'pergunta direta — quanto tempo você gasta hoje pra preparar a aula de um aluno especial novo? Quem usa nosso protocolo tá fazendo isso em 20 minutos. Quer ver o passo a passo?'),
            ('Status social', 'status',
             'o curso tem rede ativa de professores que trocam casos reais entre si. Você passa a discutir aluno com gente do teu nível — não com aluno de graduação. Quer ver o grupo?'),
            ('Perda iminente', 'perda',
             'a turma com mentoria fecha em breve. É a única chance de pegar discussão de caso em tempo real com a equipe técnica. Posso garantir tua vaga?'),
        ]
    elif archetype == 'engajado':
        bodies = [
            ('Identidade', 'identidade',
             'esse tipo de comentário não é de quem só veio fazer a tarefa — é de quem pensa o aluno, não só o exercício. É exatamente esse perfil que mais aproveita o curso completo. Posso te chamar?'),
            ('Progresso (Maestria)', 'progresso',
             'você claramente já estudou bastante. O passo que falta é SISTEMATIZAR — transformar o que você sabe em protocolo replicável e que dê pra ensinar a outros. É isso que o curso entrega. Quer ver?'),
            ('Status social', 'status',
             'gente que se engaja no preparatório do jeito que você se engajou é minoria — e é justamente quem vira referência no nicho em 12 meses. Quer entrar na turma com esse perfil?'),
            ('Curiosidade', 'curiosidade',
             'pelo que você escreveu, tenho 2-3 módulos específicos do curso que vão direto ao teu interesse — não é o pacote inteiro genérico. Posso te mandar quais são?'),
            ('Perda iminente', 'perda',
             'a turma com mentoria ao vivo fecha em breve. Pra teu nível de engajamento, esse é o componente mais valioso do curso — sem ele é só material gravado. Posso garantir tua vaga?'),
        ]
    else:  # basico
        bodies = [
            ('Curiosidade', 'curiosidade',
             'te incomoda se eu te fizer 2 perguntas? Tua resposta determina se o curso faz sentido pra você AGORA ou só daqui a um ano. Tá ok?'),
            ('Identidade', 'identidade',
             'quem termina a jornada inteira e dá 5 estrelas não faz por preencher — faz porque achou que valia. Bora conversar sobre o próximo passo?'),
            ('Progresso visível', 'progresso',
             'te explico em 3 frases o que o curso entrega. Se fizer sentido, a gente continua. Pode ser?'),
            ('Ganho racional', 'ganho',
             '8 módulos · 8 semanas · mentoria semanal ao vivo · acesso vitalício ao material · investimento parcelado em até 12x. Faz sentido pra você ouvir mais?'),
            ('Perda iminente', 'perda',
             'a turma com mentoria fecha em breve. Quer que eu segure tua vaga enquanto a gente conversa?'),
        ]

    # Compoe opener + body
    suggestions = []
    for i, (label, key, body) in enumerate(bodies):
        if use_quote:
            opener_tpl = OPENERS_WITH_QUOTE[(participant_idx + i) % len(OPENERS_WITH_QUOTE)]
            opener = opener_tpl.format(fn=fn, quote=quote_short)
        else:
            opener_tpl = OPENERS_NO_QUOTE[(participant_idx + i) % len(OPENERS_NO_QUOTE)]
            opener = opener_tpl.format(fn=fn)
        text = opener + ' ' + body
        suggestions.append({'trigger': label, 'icon_key': key, 'text': text})

    return suggestions


def main():
    # Dedupe por email: agrupa comments. Pula entries duplicadas (mesmo email + ts + text).
    by_email = OrderedDict()
    seen_comments = set()
    dup_count = 0
    for name, email, nota, prompt_key, ts, text in ENTRIES:
        key = email.strip().lower()
        comment_key = (key, ts.strip(), text.strip())
        if comment_key in seen_comments:
            dup_count += 1
            continue
        seen_comments.add(comment_key)
        if key not in by_email:
            by_email[key] = {
                'name': name,
                'email': email,
                'comments': [],
            }
        else:
            if len(name) > len(by_email[key]['name']):
                by_email[key]['name'] = name
        tags = detect_tags(text)
        by_email[key]['comments'].append({
            'nota': nota,
            'prompt': PROMPTS[prompt_key],
            'ts': ts,
            'text': text,
            'tags': tags,
        })
    if dup_count:
        print(f'(dedup: {dup_count} entries duplicadas ignoradas)')

    # Gera sugestoes para cada participante (com indice para variar opener)
    for idx, p in enumerate(by_email.values()):
        p['suggestions'] = make_suggestions(p, participant_idx=idx)
        p['archetype'] = detect_archetype(p['comments'])

    # Ordena participantes por nome
    parts = list(by_email.values())
    parts.sort(key=lambda p: p['name'].lower())

    # Estatistica de tags
    tag_counts = {k: 0 for k in TAG_CATALOG}
    for p in parts:
        for c in p['comments']:
            for t in c.get('tags', []):
                tag_counts[t] = tag_counts.get(t, 0) + 1

    # Gera JS
    lines = [
        '/*',
        ' * Base de participantes da jornada preparatoria PG3.',
        ' *',
        ' * Estrutura:',
        ' *   { name, email, archetype, comments: [ { nota, prompt, ts, text, tags } ], suggestions: [...] }',
        ' *',
        ' * Gerado por build-participantes.py a partir dos lotes de prints.',
        f' * Total: {sum(len(p["comments"]) for p in parts)} comentarios de {len(parts)} participantes unicos.',
        ' */',
        'window.ADAPTA_TAGS = ' + json.dumps(dict(TAG_CATALOG), ensure_ascii=False, indent=2) + ';',
        '',
        'window.ADAPTA_TAG_COUNTS = ' + json.dumps(tag_counts, ensure_ascii=False) + ';',
        '',
        'window.ADAPTA_PARTICIPANTS = ' + json.dumps(parts, ensure_ascii=False, indent=2) + ';',
    ]
    out = '\n'.join(lines) + '\n'
    with open('participantes.js', 'w', encoding='utf-8') as f:
        f.write(out)

    total_tagged = sum(1 for p in parts for c in p['comments'] if c.get('tags'))
    used_tags = sum(1 for v in tag_counts.values() if v > 0)
    print(f'OK · {len(parts)} participantes · {sum(len(p["comments"]) for p in parts)} comentarios')
    print(f'Tags · {used_tags}/{len(TAG_CATALOG)} tags em uso · {total_tagged} comentarios com pelo menos 1 tag')
    print('Top tags:')
    for k, v in sorted(tag_counts.items(), key=lambda x: -x[1])[:10]:
        if v > 0:
            print(f'  {v:>3}  {TAG_CATALOG[k]["label"]}')


if __name__ == '__main__':
    main()
