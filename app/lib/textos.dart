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
  String get idioma => pt ? 'Idioma' : 'Language';
  String get avisoBanco => pt
      ? 'Perguntas verificadas pelo motor de factos QUIZLUX (versão de demonstração).'
      : 'Questions checked by the QUIZLUX fact engine (demo version).';

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
