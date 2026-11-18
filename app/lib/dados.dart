import 'dart:convert';
import 'dart:math';
import 'package:flutter/services.dart' show rootBundle;

class Pergunta {
  Pergunta(this.id, this.topico, this.dificuldade, this.certa, this._texto);
  final String id;
  final String topico;
  final int dificuldade;
  final int certa;
  final Map<String, dynamic> _texto;

  String enunciado(String l) => _texto[l]['q'] as String;
  List<String> opcoes(String l) => List<String>.from(_texto[l]['o'] as List);
  String explicacao(String l) => _texto[l]['e'] as String;
}

class Banco {
  Banco(this.perguntas);
  final List<Pergunta> perguntas;

  static Future<Banco> carregar() async {
    final bruto = await rootBundle.loadString('assets/perguntas.json');
    final lista = (jsonDecode(bruto) as List).map((e) {
      final m = e as Map<String, dynamic>;
      return Pergunta(m['id'] as String, m['topic'] as String, m['difficulty'] as int, m['correct'] as int,
          Map<String, dynamic>.from(m['text'] as Map));
    }).toList();
    return Banco(lista);
  }

  /// Tópicos presentes no banco e quantas perguntas tem cada um.
  Map<String, int> topicos() {
    final r = <String, int>{};
    for (final p in perguntas) {
      r[p.topico] = (r[p.topico] ?? 0) + 1;
    }
    return r;
  }

  /// Até 10 perguntas, por ordem aleatória, só do tópico pedido (ou de todos se for null).
  List<Pergunta> sortear({String? topico, int n = 10, Random? rng}) {
    final r = rng ?? Random();
    final base = perguntas.where((p) => topico == null || p.topico == topico).toList()..shuffle(r);
    return base.take(n).toList();
  }
}
