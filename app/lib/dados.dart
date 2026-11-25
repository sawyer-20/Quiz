import 'dart:convert';
import 'dart:math';
import 'package:flutter/services.dart' show rootBundle;

class Pergunta {
  Pergunta(this.id, this.topico, this.dificuldade, this.certa, this._texto, [this.fontes = const []]);
  final List<String> fontes;
  final String id;
  final String topico;
  final int dificuldade;
  final int certa;
  final Map<String, dynamic> _texto;

  String enunciado(String l) => _texto[l]['q'] as String;
  List<String> opcoes(String l) => List<String>.from(_texto[l]['o'] as List);
  String explicacao(String l) => _texto[l]['e'] as String;

  /// Nomes curtos das fontes (domínio sem «www.»), para mostrar como na board «Sources: NASA · ESO».
  List<String> nomesFontes() {
    final r = <String>[];
    for (final u in fontes) {
      final h = Uri.tryParse(u)?.host ?? '';
      final d = h.startsWith('www.') ? h.substring(4) : h;
      if (d.isNotEmpty && !r.contains(d)) r.add(d);
    }
    return r;
  }
}

class Banco {
  Banco(this.perguntas);
  final List<Pergunta> perguntas;

  static Future<Banco> carregar() async {
    // perguntas.json: as 57 verificadas pelo motor; importadas.json: pacote separado
    // (Open Trivia DB, CC BY-SA 4.0, tradução automática; Wikidata, CC0), auditado por amostra.
    final lista = <Pergunta>[];
    for (final ficheiro in ['assets/perguntas.json', 'assets/importadas.json']) {
      String bruto;
      try {
        bruto = await rootBundle.loadString(ficheiro);
      } catch (_) {
        continue;
      }
      lista.addAll((jsonDecode(bruto) as List).map((e) {
        final m = e as Map<String, dynamic>;
        return Pergunta(m['id'] as String, m['topic'] as String, m['difficulty'] as int, m['correct'] as int,
            Map<String, dynamic>.from(m['text'] as Map), List<String>.from((m['sources'] ?? const []) as List));
      }));
    }
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
