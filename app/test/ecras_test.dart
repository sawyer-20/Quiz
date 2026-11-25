import 'dart:convert';
import 'dart:io';

import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:quizlux/dados.dart';
import 'package:quizlux/main.dart';
import 'package:quizlux/tema.dart';

/// Lê o banco da app diretamente do disco (o rootBundle não é preciso neste teste).
Banco bancoDoDisco() {
  final l = jsonDecode(File('assets/perguntas.json').readAsStringSync()) as List;
  return Banco(l.map((e) {
    final m = e as Map<String, dynamic>;
    return Pergunta(m['id'] as String, m['topic'] as String, m['difficulty'] as int, m['correct'] as int,
        Map<String, dynamic>.from(m['text'] as Map), List<String>.from((m['sources'] ?? const []) as List));
  }).toList());
}

/// Carrega as letras verdadeiras: sem ela, o teste mede o texto com a letra de teste e os tamanhos não batem certo.
Future<void> carregarFontes() async {
  const fontes = {
    'Manrope': ['Manrope_400Regular', 'Manrope_500Medium', 'Manrope_600SemiBold', 'Manrope_700Bold', 'Manrope_800ExtraBold'],
    'CormorantGaramond': ['CormorantGaramond_500Medium', 'CormorantGaramond_600SemiBold', 'CormorantGaramond_700Bold'],
  };
  for (final e in fontes.entries) {
    final fl = FontLoader(e.key);
    for (final f in e.value) {
      fl.addFont(Future.value(ByteData.sublistView(File('assets/fonts/$f.ttf').readAsBytesSync())));
    }
    await fl.load();
  }
}

void main() {
  setUpAll(carregarFontes);
  testesEstados();

  testWidgets('o botão PT/EN muda o idioma do ecrã inicial', (t) async {
    await t.pumpWidget(const QuizluxApp());
    await t.pump(const Duration(milliseconds: 1500)); // fim do splash
    for (var i = 0; i < 50 && find.text('Escolhe um tópico').evaluate().isEmpty; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 100)));
      await t.pump(const Duration(milliseconds: 50));
    }
    await t.pumpAndSettle(); // fim da transição do splash para o início
    expect(find.text('Escolhe um tópico'), findsOneWidget);

    await t.tap(find.text('EN'));
    await t.pumpAndSettle();
    expect(find.text('Pick a topic'), findsOneWidget);
    expect(find.text('Escolhe um tópico'), findsNothing);

    await t.tap(find.text('PT'));
    await t.pumpAndSettle();
    expect(find.text('Escolhe um tópico'), findsOneWidget);
  });

  // Ecrãs pequenos e letra do sistema aumentada: nenhum texto pode ficar cortado.
  const casos = [
    (Size(320, 568), 1.0),
    (Size(360, 640), 1.0),
    (Size(360, 640), 1.3),
    (Size(360, 800), 1.3),
  ];
  for (final (tamanho, escala) in casos) {
    testWidgets('jogo sem texto cortado em ${tamanho.width.toInt()}x${tamanho.height.toInt()}, letra x$escala', (t) async {
      t.view.physicalSize = tamanho * 3;
      t.view.devicePixelRatio = 3;
      t.platformDispatcher.textScaleFactorTestValue = escala;
      addTearDown(t.view.reset);
      addTearDown(t.platformDispatcher.clearTextScaleFactorTestValue);
      final banco = bancoDoDisco();
      final falhas = <String>[];
      for (final lingua in ['pt-PT', 'en-US']) {
        for (final p in banco.perguntas) {
          // Árvore nova em cada pergunta: o Flutter só avisa uma vez por objeto cortado.
          await t.pumpWidget(const SizedBox());
          await t.pumpWidget(MaterialApp(theme: temaQuizlux(), home: EcraJogo(perguntas: [p], lingua: lingua, banco: banco, topico: null)));
          if (t.takeException() != null) falhas.add('${p.id} $lingua antes de responder');
          await t.tap(find.byKey(const Key('opcao_0')));
          await t.pumpAndSettle();
          if (t.takeException() != null) falhas.add('${p.id} $lingua depois de responder');
          expect(find.byType(FilledButton), findsOneWidget);
        }
      }
      await t.pumpWidget(const SizedBox());
      expect(falhas, isEmpty);
    });
  }
}

/// Cor de fundo e da borda do cartão da opção k.
(Color?, Color?) coresDaOpcao(WidgetTester t, int k) {
  final c = t.widget<AnimatedContainer>(find.byKey(Key('estado_$k')));
  final d = c.decoration! as BoxDecoration;
  return (d.color, (d.border! as Border).top.color);
}

/// Pergunta sintética: a certa é a C (índice 2).
Pergunta perguntaDeTeste() => Pergunta('Q-teste', 'Science', 1, 2, {
      'pt-PT': {'q': 'Pergunta?', 'o': ['Um', 'Dois', 'Três', 'Quatro'], 'e': 'Explicação.'},
      'en-US': {'q': 'Question?', 'o': ['One', 'Two', 'Three', 'Four'], 'e': 'Explanation.'},
    });

void testesEstados() {
  Future<void> abrir(WidgetTester t) async {
    final p = perguntaDeTeste();
    await t.pumpWidget(MaterialApp(theme: temaQuizlux(), home: EcraJogo(perguntas: [p], lingua: 'pt-PT', banco: Banco([p]), topico: null)));
  }

  testWidgets('resposta errada: a tua a vermelho, a certa a verde, as restantes a azul neutro', (t) async {
    await abrir(t);
    await t.tap(find.byKey(const Key('opcao_0')));
    await t.pumpAndSettle();
    expect(coresDaOpcao(t, 0).$2, Cores.errado);
    expect(coresDaOpcao(t, 2).$2, Cores.certo);
    for (final k in [1, 3]) {
      expect(coresDaOpcao(t, k).$1, Cores.azul.withValues(alpha: 0.08));
    }
    expect(find.text('A tua resposta'), findsOneWidget);
    expect(find.text('Certo'), findsOneWidget);
  });

  testWidgets('resposta certa: verde e as restantes a azul neutro', (t) async {
    await abrir(t);
    await t.tap(find.byKey(const Key('opcao_2')));
    await t.pumpAndSettle();
    expect(coresDaOpcao(t, 2).$2, Cores.certo);
    for (final k in [0, 1, 3]) {
      expect(coresDaOpcao(t, k).$1, Cores.azul.withValues(alpha: 0.08));
    }
    expect(find.text('A tua resposta'), findsNothing);
  });

  testWidgets('tempo esgotado: a certa a verde e as restantes a azul neutro', (t) async {
    await abrir(t);
    await t.pump(const Duration(seconds: 11));
    await t.pumpAndSettle();
    expect(find.text('Tempo esgotado'), findsOneWidget);
    expect(coresDaOpcao(t, 2).$2, Cores.certo);
    for (final k in [0, 1, 3]) {
      expect(coresDaOpcao(t, k).$1, Cores.azul.withValues(alpha: 0.08));
    }
  });

  testWidgets('a mudança de estado dura 200 ms', (t) async {
    await abrir(t);
    await t.tap(find.byKey(const Key('opcao_0')));
    await t.pump();
    expect(t.widget<AnimatedContainer>(find.byKey(const Key('estado_0'))).duration, const Duration(milliseconds: 200));
    // A meio da transição, a borda da tua resposta ainda não chegou ao vermelho.
    await t.pump(const Duration(milliseconds: 100));
    final meio = t.renderObject<RenderDecoratedBox>(
        find.descendant(of: find.byKey(const Key('estado_0')), matching: find.byType(DecoratedBox)).first);
    expect(((meio.decoration as BoxDecoration).border! as Border).top.color, isNot(Cores.errado));
    await t.pumpAndSettle();
    await t.pumpWidget(const SizedBox());
  });
}
