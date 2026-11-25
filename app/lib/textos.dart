/// Textos da interface nos dois idiomas. As perguntas vêm do banco, já nos dois idiomas.
class T {
  T(this.l);
  final String l; // 'pt-PT' ou 'en-US'
  bool get pt => l == 'pt-PT';

  String get titulo => 'QUIZLUX';
  String get escolhaTopico => pt ? 'Escolhe um tópico' : 'Pick a topic';
  String get misto => pt ? 'Misto (todos os tópicos)' : 'Mixed (all topics)';
  String perguntas(int n) => pt ? '$n perguntas' : '$n questions';
  String progresso(int i, int n) => pt ? 'Pergunta $i de $n' : 'Question $i of $n';
  String get pontos => pt ? 'pontos' : 'points';
  String get tempoEsgotado => pt ? 'Tempo esgotado' : "Time's up";
  String get certo => pt ? 'Certo!' : 'Correct!';
  String get errado => pt ? 'Errado' : 'Wrong';
  String get seguinte => pt ? 'Seguinte' : 'Next';
  String get verResultado => pt ? 'Ver resultado' : 'See result';
  String get resultado => pt ? 'Resultado' : 'Result';
  String acertos(int a, int n) => pt ? '$a de $n certas' : '$a of $n correct';
  String get jogarOutra => pt ? 'Jogar outra vez' : 'Play again';
  String get inicio => pt ? 'Início' : 'Home';
  String get revisao => pt ? 'Revisão' : 'Review';
  String get tuaResposta => pt ? 'A tua resposta' : 'Your answer';
  String get tempoMedio => pt ? 'Tempo médio' : 'Avg. time';
  String get melhorSerie => pt ? 'Melhor série' : 'Best streak';
  String get certasRotulo => pt ? 'Certas' : 'Correct';
  String get fontes => pt ? 'Fontes' : 'Sources';
  String get voltarInicio => pt ? 'Voltar ao início' : 'Back to home';
  String get proximaPergunta => pt ? 'Seguinte' : 'Next';
  String get tagline => 'THE GAME OF KNOWLEDGE';
  String perguntaDe(int i, int n) => pt ? 'PERGUNTA $i DE $n' : 'QUESTION $i OF $n';
  String get idioma => pt ? 'Idioma' : 'Language';
  String get avisoBanco => pt
      ? 'Versão de demonstração. Inclui perguntas do Open Trivia DB (opentdb.com, licença CC BY-SA 4.0), '
          'traduzidas automaticamente e auditadas por amostra, e perguntas geradas a partir do Wikidata (CC0).'
      : 'Demo version. Includes questions from Open Trivia DB (opentdb.com, CC BY-SA 4.0 licence), '
          'machine-translated and sample-audited, and questions generated from Wikidata (CC0).';

  String topico(String t) {
    const pt_ = {
      'General Knowledge': 'Cultura geral',
      'Geography': 'Geografia',
      'World History': 'História',
      'Science': 'Ciência',
      'Space': 'Espaço',
      'Movies': 'Cinema',
      'Music': 'Música',
      'Football': 'Futebol',
      'Video Games': 'Videojogos',
      'Nature & Animals': 'Natureza e animais',
    };
    return pt ? (pt_[t] ?? t) : t;
  }
}
