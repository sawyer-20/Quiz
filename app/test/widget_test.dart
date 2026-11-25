import 'package:flutter_test/flutter_test.dart';
import 'package:quizlux/dados.dart';
import 'package:quizlux/textos.dart';

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

  test('o subtítulo do tópico mostra o total e o tamanho da ronda', () {
    expect(T('pt-PT').disponiveis(308, 10), '308 perguntas · rondas de 10');
    expect(T('pt-PT').disponiveis(2056, 10), '2.056 perguntas · rondas de 10');
    expect(T('en-US').disponiveis(2056, 10), '2,056 questions · rounds of 10');
    expect(T('pt-PT').disponiveis(3, 3), '3 perguntas · rondas de 3');
  });

  testWidgets('o banco carrega as verificadas e o pacote importado', (t) async {
    final b = (await t.runAsync(Banco.carregar))!;
    final topicos = b.topicos();
    expect(b.perguntas.length, greaterThan(2000));
    expect(topicos['General Knowledge'], greaterThan(300));
    expect(topicos['Space'], greaterThan(80));
  });
}
