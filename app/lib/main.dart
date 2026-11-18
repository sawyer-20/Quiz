import 'dart:async';
import 'package:material_ui/material_ui.dart';
import 'dados.dart';
import 'tema.dart';
import 'textos.dart';

void main() => runApp(const QuizluxApp());

class QuizluxApp extends StatefulWidget {
  const QuizluxApp({super.key});
  @override
  State<QuizluxApp> createState() => _QuizluxAppState();
}

class _QuizluxAppState extends State<QuizluxApp> {
  String _lingua = 'pt-PT';
  late final Future<Banco> _banco = Banco.carregar();

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'QUIZLUX',
        debugShowCheckedModeBanner: false,
        theme: temaQuizlux(),
        home: FutureBuilder<Banco>(
          future: _banco,
          builder: (c, s) {
            if (!s.hasData) {
              return const Scaffold(body: Center(child: CircularProgressIndicator()));
            }
            return EcraInicio(banco: s.data!, lingua: _lingua, aoMudarLingua: (l) => setState(() => _lingua = l));
          },
        ),
      );
}

class EcraInicio extends StatelessWidget {
  const EcraInicio({super.key, required this.banco, required this.lingua, required this.aoMudarLingua});
  final Banco banco;
  final String lingua;
  final ValueChanged<String> aoMudarLingua;

  @override
  Widget build(BuildContext context) {
    final t = T(lingua);
    final topicos = banco.topicos();
    final nomes = topicos.keys.toList()..sort((a, b) => t.topico(a).compareTo(t.topico(b)));
    return Scaffold(
      appBar: AppBar(
        title: Text(t.titulo, style: const TextStyle(letterSpacing: 4, fontWeight: FontWeight.w800, color: Cores.destaque)),
        actions: [
          SegmentedButton<String>(
            showSelectedIcon: false,
            segments: const [
              ButtonSegment(value: 'pt-PT', label: Text('PT')),
              ButtonSegment(value: 'en-US', label: Text('EN')),
            ],
            selected: {lingua},
            onSelectionChanged: (s) => aoMudarLingua(s.first),
          ),
          const SizedBox(width: 12),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(t.escolhaTopico, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
          const SizedBox(height: 12),
          _CartaoTopico(
            titulo: t.misto,
            subtitulo: t.perguntas(banco.perguntas.length < 10 ? banco.perguntas.length : 10),
            aoToque: () => _jogar(context, null),
          ),
          for (final n in nomes)
            _CartaoTopico(
              titulo: t.topico(n),
              subtitulo: t.perguntas(topicos[n]! < 10 ? topicos[n]! : 10),
              aoToque: () => _jogar(context, n),
            ),
          const SizedBox(height: 16),
          Text(t.avisoBanco, style: const TextStyle(color: Cores.textoSuave, fontSize: 12)),
        ],
      ),
    );
  }

  void _jogar(BuildContext context, String? topico) {
    final lista = banco.sortear(topico: topico);
    Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => EcraJogo(perguntas: lista, lingua: lingua, banco: banco, topico: topico),
    ));
  }
}

class _CartaoTopico extends StatelessWidget {
  const _CartaoTopico({required this.titulo, required this.subtitulo, required this.aoToque});
  final String titulo;
  final String subtitulo;
  final VoidCallback aoToque;
  @override
  Widget build(BuildContext context) => Card(
        color: Cores.superficie,
        margin: const EdgeInsets.only(bottom: 10),
        child: ListTile(
          title: Text(titulo, style: const TextStyle(fontWeight: FontWeight.w600)),
          subtitle: Text(subtitulo, style: const TextStyle(color: Cores.textoSuave)),
          trailing: const Icon(Icons.play_arrow_rounded, color: Cores.destaque),
          onTap: aoToque,
        ),
      );
}

const segundosPorPergunta = 20;

class Resposta {
  Resposta(this.escolhida, this.certa, this.pontos);
  final int? escolhida; // null = tempo esgotado
  final bool certa;
  final int pontos;
}

class EcraJogo extends StatefulWidget {
  const EcraJogo({super.key, required this.perguntas, required this.lingua, required this.banco, required this.topico});
  final List<Pergunta> perguntas;
  final String lingua;
  final Banco banco;
  final String? topico;
  @override
  State<EcraJogo> createState() => _EcraJogoState();
}

class _EcraJogoState extends State<EcraJogo> {
  int _i = 0;
  int _restante = segundosPorPergunta;
  int? _escolhida;
  bool _respondida = false;
  final List<Resposta> _respostas = [];
  Timer? _timer;

  T get t => T(widget.lingua);
  Pergunta get _p => widget.perguntas[_i];
  int get _pontos => _respostas.fold(0, (s, r) => s + r.pontos);

  @override
  void initState() {
    super.initState();
    _iniciarTempo();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _iniciarTempo() {
    _timer?.cancel();
    _restante = segundosPorPergunta;
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (_respondida) return;
      setState(() => _restante--);
      if (_restante <= 0) _responder(null);
    });
  }

  void _responder(int? escolha) {
    if (_respondida) return;
    final certa = escolha != null && escolha == _p.certa;
    // 100 pontos por resposta certa, mais até 100 de bónus pela rapidez.
    final pontos = certa ? 100 + (_restante * 100 ~/ segundosPorPergunta) : 0;
    _timer?.cancel();
    setState(() {
      _respondida = true;
      _escolhida = escolha;
      _respostas.add(Resposta(escolha, certa, pontos));
    });
  }

  void _seguinte() {
    if (_i + 1 >= widget.perguntas.length) {
      Navigator.of(context).pushReplacement(MaterialPageRoute(
        builder: (_) => EcraResultado(
            perguntas: widget.perguntas, respostas: _respostas, lingua: widget.lingua, banco: widget.banco, topico: widget.topico),
      ));
      return;
    }
    setState(() {
      _i++;
      _escolhida = null;
      _respondida = false;
    });
    _iniciarTempo();
  }

  @override
  Widget build(BuildContext context) {
    final l = widget.lingua;
    final opcoes = _p.opcoes(l);
    return Scaffold(
      appBar: AppBar(
        title: Text(t.topico(_p.topico)),
        actions: [Padding(padding: const EdgeInsets.only(right: 16), child: Center(child: Text('$_pontos ${t.pontos}', style: const TextStyle(color: Cores.destaque, fontWeight: FontWeight.w700))))],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(t.progresso(_i + 1, widget.perguntas.length), style: const TextStyle(color: Cores.textoSuave)),
            const SizedBox(height: 6),
            LinearProgressIndicator(
              value: _restante / segundosPorPergunta,
              color: _restante <= 5 ? Cores.errado : Cores.destaque,
              backgroundColor: Cores.superficie,
              minHeight: 8,
            ),
            const SizedBox(height: 20),
            Text(_p.enunciado(l), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w700, height: 1.3)),
            const SizedBox(height: 20),
            for (var k = 0; k < opcoes.length; k++) _botaoOpcao(k, opcoes[k]),
            if (_respondida) ...[
              const SizedBox(height: 8),
              Text(
                _escolhida == null ? t.tempoEsgotado : (_escolhida == _p.certa ? t.certo : t.errado),
                style: TextStyle(fontWeight: FontWeight.w800, fontSize: 18, color: _escolhida == _p.certa ? Cores.certo : Cores.errado),
              ),
              const SizedBox(height: 6),
              Expanded(child: SingleChildScrollView(child: Text(_p.explicacao(l), style: const TextStyle(color: Cores.textoSuave, height: 1.35)))),
              FilledButton(
                onPressed: _seguinte,
                child: Text(_i + 1 >= widget.perguntas.length ? t.verResultado : t.seguinte),
              ),
            ] else
              const Spacer(),
          ],
        ),
      ),
    );
  }

  Widget _botaoOpcao(int k, String texto) {
    Color cor = Cores.superficie;
    if (_respondida) {
      if (k == _p.certa) {
        cor = Cores.certo.withValues(alpha: 0.35);
      } else if (k == _escolhida) {
        cor = Cores.errado.withValues(alpha: 0.35);
      }
    }
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: cor,
        borderRadius: BorderRadius.circular(14),
        child: InkWell(
          key: Key('opcao_$k'),
          borderRadius: BorderRadius.circular(14),
          onTap: _respondida ? null : () => _responder(k),
          child: Padding(padding: const EdgeInsets.all(16), child: Text(texto, style: const TextStyle(fontSize: 16))),
        ),
      ),
    );
  }
}

class EcraResultado extends StatelessWidget {
  const EcraResultado({super.key, required this.perguntas, required this.respostas, required this.lingua, required this.banco, required this.topico});
  final List<Pergunta> perguntas;
  final List<Resposta> respostas;
  final String lingua;
  final Banco banco;
  final String? topico;

  @override
  Widget build(BuildContext context) {
    final t = T(lingua);
    final acertos = respostas.where((r) => r.certa).length;
    final pontos = respostas.fold<int>(0, (s, r) => s + r.pontos);
    return Scaffold(
      appBar: AppBar(title: Text(t.resultado)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Center(child: Text('$pontos', style: const TextStyle(fontSize: 64, fontWeight: FontWeight.w900, color: Cores.destaque))),
          Center(child: Text(t.pontos, style: const TextStyle(color: Cores.textoSuave))),
          const SizedBox(height: 8),
          Center(child: Text(t.acertos(acertos, perguntas.length), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w700))),
          const SizedBox(height: 20),
          Text(t.revisao, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
          const SizedBox(height: 8),
          for (var k = 0; k < perguntas.length; k++)
            Card(
              color: Cores.superficie,
              child: ListTile(
                leading: Icon(respostas[k].certa ? Icons.check_circle : Icons.cancel, color: respostas[k].certa ? Cores.certo : Cores.errado),
                title: Text(perguntas[k].enunciado(lingua), style: const TextStyle(fontSize: 14)),
                subtitle: Text(perguntas[k].opcoes(lingua)[perguntas[k].certa], style: const TextStyle(color: Cores.certo)),
              ),
            ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () => Navigator.of(context).pushReplacement(MaterialPageRoute(
              builder: (_) => EcraJogo(perguntas: banco.sortear(topico: topico), lingua: lingua, banco: banco, topico: topico),
            )),
            child: Text(t.jogarOutra),
          ),
          TextButton(onPressed: () => Navigator.of(context).popUntil((r) => r.isFirst), child: Text(t.inicio)),
        ],
      ),
    );
  }
}
