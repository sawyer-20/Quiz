import 'package:flutter_test/flutter_test.dart';
import 'package:quizlux/dados.dart';

void main() {
  test('sortear devolve no máximo 10 perguntas do tópico', () {
    final b = Banco([
      for (var i = 0; i < 12; i++) Pergunta('Q$i', 'Science', 1, 0, {'pt-PT': {'q': 'a', 'o': ['1', '2', '3', '4'], 'e': 'x'}}),
      Pergunta('Qm', 'Music', 1, 0, {'pt-PT': {'q': 'a', 'o': ['1', '2', '3', '4'], 'e': 'x'}}),
    ]);
    expect(b.sortear(topico: 'Science').length, 10);
    expect(b.sortear(topico: 'Music').length, 1);
    expect(b.sortear().length, 10);
  });
}
