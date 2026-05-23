/*
 * Base de participantes da jornada preparatoria PG3.
 *
 * Estrutura:
 *   { name, email, comments: [ { nota, prompt, ts, text } ] }
 *
 * - "name" e "email" sao a chave de busca (case + accent insensitive)
 * - "comments" e a lista de todas as interacoes do participante na jornada
 * - "prompt" e o topico/pergunta que o sistema apresentou (ex: "Vamos nessa?",
 *   "Voce esta entendendo por que pressao arterial nao e so dado clinico..."),
 *   pode ser null quando nao houver
 * - "ts" e o timestamp em formato "DD/MM/AAAA HH:MM"
 * - "nota" e a avaliacao 1 a 5
 *
 * Atualizacoes futuras: append novos participantes ou comments aqui.
 * Se o participante ja existir (mesmo email), apenas adicione comments ao array.
 */
window.ADAPTA_PARTICIPANTS = [
  // dataset sera populado a medida que os lotes de prints chegarem
];
