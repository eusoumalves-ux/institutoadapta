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
]


def main():
    # Dedupe por email: agrupa comments
    by_email = OrderedDict()
    for name, email, nota, prompt_key, ts, text in ENTRIES:
        key = email.strip().lower()
        if key not in by_email:
            by_email[key] = {
                'name': name,
                'email': email,
                'comments': [],
            }
        else:
            # Mantém o nome com mais caracteres (provável ortografia mais completa)
            if len(name) > len(by_email[key]['name']):
                by_email[key]['name'] = name
        by_email[key]['comments'].append({
            'nota': nota,
            'prompt': PROMPTS[prompt_key],
            'ts': ts,
            'text': text,
        })

    # Ordena participantes por nome
    parts = list(by_email.values())
    parts.sort(key=lambda p: p['name'].lower())

    # Gera JS
    lines = [
        '/*',
        ' * Base de participantes da jornada preparatoria PG3.',
        ' *',
        ' * Estrutura:',
        ' *   { name, email, comments: [ { nota, prompt, ts, text } ] }',
        ' *',
        ' * Gerado por build-participantes.py a partir dos lotes de prints.',
        f' * Total: {sum(len(p["comments"]) for p in parts)} comentarios de {len(parts)} participantes unicos.',
        ' */',
        'window.ADAPTA_PARTICIPANTS = ' + json.dumps(parts, ensure_ascii=False, indent=2) + ';',
    ]
    out = '\n'.join(lines) + '\n'
    with open('participantes.js', 'w', encoding='utf-8') as f:
        f.write(out)

    print(f'OK · {len(parts)} participantes · {sum(len(p["comments"]) for p in parts)} comentarios')


if __name__ == '__main__':
    main()
