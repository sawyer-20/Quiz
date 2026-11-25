import 'dart:async';
import 'package:material_ui/material_ui.dart';
import 'dados.dart';
import 'marca.dart';
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
        home: EcraSplash(
          proximo: (c) => FutureBuilder<Banco>(
            future: _banco,
            builder: (c, s) {
              if (s.hasError) {
                return const Scaffold(
                  body: Center(
                    child: Padding(
                      padding: EdgeInsets.all(24),
                      child: Text('Não foi possível carregar as perguntas.\nCould not load the questions.', textAlign: TextAlign.center),
                    ),
                  ),
                );
              }
              if (!s.hasData) return const Scaffold(body: Center(child: CircularProgressIndicator()));
              return EcraInicio(banco: s.data!, lingua: _lingua, aoMudarLingua: (l) => setState(() => _lingua = l));
            },
          ),
        ),
      );
}

/// Board «1. Splash»: marca, nome e a linha «THE GAME OF KNOWLEDGE» em Cormorant.
class EcraSplash extends StatefulWidget {
  const EcraSplash({super.key, required this.proximo});
  final WidgetBuilder proximo;
  @override
  State<EcraSplash> createState() => _EcraSplashState();
}

class _EcraSplashState extends State<EcraSplash> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(milliseconds: 1400), () {
      if (!mounted) return;
      Navigator.of(context).pushReplacement(MaterialPageRoute(builder: widget.proximo));
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Center(
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            const Marca(tamanho: 88),
            const SizedBox(height: 18),
            const Logotipo(tamanho: 30),
            const SizedBox(height: 16),
            Text(T('pt-PT').tagline, style: estiloMarca(tamanho: 17, peso: FontWeight.w700, espaco: 4.5)),
          ]),
        ),
      );
}

/// Board «3. Topics» (só o essencial do modo solo): lista de tópicos.
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
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 20, 16, 24),
          children: [
            Row(children: [
              const Logotipo(tamanho: 20),
              const Spacer(),
              SegmentedButton<String>(
                showSelectedIcon: false,
                style: SegmentedButton.styleFrom(
                  backgroundColor: Cores.superficie,
                  foregroundColor: Cores.textoSuave,
                  selectedBackgroundColor: Cores.dourado,
                  selectedForegroundColor: Cores.fundo,
                  side: const BorderSide(color: Cores.linha),
                  textStyle: const TextStyle(fontWeight: FontWeight.w800),
                ),
                segments: const [ButtonSegment(value: 'pt-PT', label: Text('PT')), ButtonSegment(value: 'en-US', label: Text('EN'))],
                selected: {lingua},
                onSelectionChanged: (s) => aoMudarLingua(s.first),
              ),
            ]),
            const SizedBox(height: 22),
            Text(t.escolhaTopico, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w800, height: 1.2)),
            const SizedBox(height: 14),
            _CartaoTopico(
              titulo: t.misto,
              subtitulo: t.disponiveis(banco.perguntas.length, banco.perguntas.length < 10 ? banco.perguntas.length : 10),
              destaque: true,
              aoToque: () => _jogar(context, null),
            ),
            for (final n in nomes)
              _CartaoTopico(
                titulo: t.topico(n),
                subtitulo: t.disponiveis(topicos[n]!, topicos[n]! < 10 ? topicos[n]! : 10),
                aoToque: () => _jogar(context, n),
              ),
            const SizedBox(height: 14),
            Text(t.avisoBanco, style: const TextStyle(color: Cores.textoSuave, fontSize: 12, height: 1.4)),
          ],
        ),
      ),
    );
  }

  void _jogar(BuildContext context, String? topico) {
    Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => EcraJogo(perguntas: banco.sortear(topico: topico), lingua: lingua, banco: banco, topico: topico),
    ));
  }
}

class _CartaoTopico extends StatelessWidget {
  const _CartaoTopico({required this.titulo, required this.subtitulo, required this.aoToque, this.destaque = false});
  final String titulo;
  final String subtitulo;
  final VoidCallback aoToque;
  final bool destaque;
  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: Material(
          color: destaque ? Cores.superficie2 : Cores.superficie,
          borderRadius: BorderRadius.circular(16),
          child: InkWell(
            borderRadius: BorderRadius.circular(16),
            onTap: aoToque,
            child: Container(
              constraints: const BoxConstraints(minHeight: 64),
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: destaque ? Cores.dourado.withValues(alpha: 0.5) : Cores.linha),
              ),
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(titulo, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
                    const SizedBox(height: 2),
                    Text(subtitulo, style: const TextStyle(color: Cores.textoSuave, fontSize: 12)),
                  ]),
                ),
                const Icon(Icons.chevron_right_rounded, color: Cores.dourado),
              ]),
            ),
          ),
        ),
      );
}

/// Segundos por pergunta (a board mostra um temporizador de 10 s).
const segundosPorPergunta = 10;

class Resposta {
  Resposta(this.escolhida, this.certa, this.pontos, this.segundos);
  final int? escolhida; // null = tempo esgotado
  final bool certa;
  final int pontos;
  final int segundos;
}

/// Boards «5. Gameplay» e «6. Answer states».
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
  final _rolagem = ScrollController();
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
    _rolagem.dispose();
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
      _respostas.add(Resposta(escolha, certa, pontos, segundosPorPergunta - _restante));
    });
    // Em ecrãs pequenos a explicação fica abaixo das opções: desce até ela.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted && _rolagem.hasClients) {
        _rolagem.animateTo(_rolagem.position.maxScrollExtent, duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
      }
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
    if (_rolagem.hasClients) _rolagem.jumpTo(0);
    _iniciarTempo();
  }

  @override
  Widget build(BuildContext context) {
    final l = widget.lingua;
    final opcoes = _p.opcoes(l);
    final n = widget.perguntas.length;
    final fontes = _p.nomesFontes();
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
          child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Row(children: [
              IconButton(
                tooltip: t.inicio,
                onPressed: () => Navigator.of(context).popUntil((r) => r.isFirst),
                icon: const Icon(Icons.arrow_back_rounded, color: Cores.textoSuave),
              ),
              Expanded(
                child: Text(t.topico(_p.topico).toUpperCase(),
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontSize: 11, letterSpacing: 1.5, color: Cores.douradoClaro, fontWeight: FontWeight.w700)),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: Cores.dourado.withValues(alpha: 0.14),
                  border: Border.all(color: Cores.dourado.withValues(alpha: 0.4)),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Text('$_pontos ${t.pontos}', style: const TextStyle(color: Cores.douradoClaro, fontSize: 12, fontWeight: FontWeight.w800)),
              ),
            ]),
            const SizedBox(height: 6),
            Center(child: AnelTempo(restante: _restante, total: segundosPorPergunta)),
            const SizedBox(height: 12),
            Row(children: [
              for (var k = 0; k < n; k++) ...[
                Expanded(
                  child: Container(
                    height: 4,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(2),
                      color: k < _i ? Cores.dourado : (k == _i ? Cores.douradoClaro : Cores.superficie2),
                    ),
                  ),
                ),
                if (k < n - 1) const SizedBox(width: 6),
              ]
            ]),
            const SizedBox(height: 6),
            Text(t.perguntaDe(_i + 1, n), style: const TextStyle(fontSize: 11, letterSpacing: 1.1, color: Cores.textoSuave, fontWeight: FontWeight.w700)),
            const SizedBox(height: 10),
            // Enunciado, opções e explicação rolam; o cabeçalho e o botão ficam fixos.
            Expanded(
              child: SingleChildScrollView(
                controller: _rolagem,
                child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                  Text(_p.enunciado(l), style: const TextStyle(fontSize: 23, fontWeight: FontWeight.w800, height: 1.25)),
                  const SizedBox(height: 14),
                  for (var k = 0; k < opcoes.length; k++) _botaoOpcao(k, opcoes[k]),
                  if (_respondida)
                    Container(
                      margin: const EdgeInsets.only(top: 4),
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                      decoration: BoxDecoration(color: Cores.superficie, borderRadius: BorderRadius.circular(16)),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        if (_escolhida == null)
                          Padding(
                            padding: const EdgeInsets.only(bottom: 6),
                            child: Text(t.tempoEsgotado, style: const TextStyle(color: Cores.errado, fontWeight: FontWeight.w800, fontSize: 13)),
                          ),
                        if (_p.explicacao(l).isNotEmpty) Text(_p.explicacao(l), style: const TextStyle(fontSize: 13, height: 1.4)),
                        if (fontes.isNotEmpty) ...[
                          const SizedBox(height: 8),
                          Text('${t.fontes}: ${fontes.take(3).join(' · ')}', style: const TextStyle(fontSize: 12, color: Cores.textoSuave, height: 1.4)),
                        ],
                      ]),
                    ),
                ]),
              ),
            ),
            if (_respondida) ...[
              const SizedBox(height: 10),
              FilledButton(onPressed: _seguinte, child: Text(_i + 1 >= n ? t.verResultado : t.seguinte)),
            ],
          ]),
        ),
      ),
    );
  }

  /// Estados de cada opção. Antes da revelação: superfície. Depois: certa a verde com «Certo»,
  /// a tua errada a vermelho com «A tua resposta» (e a certa assinalada ao mesmo tempo), as restantes
  /// a azul neutro. O estado nunca depende só da cor. Transição curta, sem animações exageradas.
  static const duracaoEstado = Duration(milliseconds: 200);

  Widget _botaoOpcao(int k, String texto) {
    final letra = String.fromCharCode(65 + k);
    final certa = _respondida && k == _p.certa;
    final errada = _respondida && k == _escolhida && k != _p.certa;
    final neutra = _respondida && !certa && !errada;
    Color fundo = Cores.superficie;
    Color borda = Colors.transparent;
    Color emblemaFundo = Cores.superficie2;
    Color emblemaTexto = Cores.textoSuave;
    Color corTexto = Cores.texto;
    String? palavra;
    Color? corPalavra;
    if (certa) {
      fundo = Cores.certo.withValues(alpha: 0.16);
      borda = Cores.certo;
      emblemaFundo = Cores.certo;
      emblemaTexto = Cores.fundo;
      palavra = t.certo.replaceAll('!', '');
      corPalavra = Cores.certo;
    } else if (errada) {
      fundo = Cores.errado.withValues(alpha: 0.14);
      borda = Cores.errado;
      emblemaFundo = Cores.errado;
      emblemaTexto = Cores.fundo;
      palavra = t.tuaResposta;
      corPalavra = Cores.errado;
    } else if (neutra) {
      fundo = Cores.azul.withValues(alpha: 0.08);
      borda = Cores.azul.withValues(alpha: 0.30);
      emblemaFundo = Cores.azul.withValues(alpha: 0.22);
      emblemaTexto = Cores.textoSuave;
      corTexto = Cores.textoSuave;
    }
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        type: MaterialType.transparency,
        child: InkWell(
          key: Key('opcao_$k'),
          borderRadius: BorderRadius.circular(14),
          onTap: _respondida ? null : () => _responder(k),
          child: AnimatedContainer(
            key: Key('estado_$k'),
            duration: duracaoEstado,
            curve: Curves.easeOut,
            constraints: const BoxConstraints(minHeight: 56),
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            decoration: BoxDecoration(color: fundo, borderRadius: BorderRadius.circular(14), border: Border.all(color: borda, width: 1.5)),
            child: Row(children: [
              AnimatedContainer(
                duration: duracaoEstado,
                curve: Curves.easeOut,
                width: 30,
                height: 30,
                alignment: Alignment.center,
                decoration: BoxDecoration(shape: BoxShape.circle, color: emblemaFundo),
                child: Text(letra, style: TextStyle(fontWeight: FontWeight.w800, fontSize: 13, color: emblemaTexto)),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: AnimatedDefaultTextStyle(
                  duration: duracaoEstado,
                  style: TextStyle(fontFamily: fonteInterface, fontSize: 16, fontWeight: FontWeight.w700, color: corTexto),
                  child: Text(texto),
                ),
              ),
              if (palavra != null) ...[
                const SizedBox(width: 8),
                Text(palavra, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: corPalavra)),
              ],
            ]),
          ),
        ),
      ),
    );
  }
}

/// Board «7. Result».
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
    final media = respostas.isEmpty ? 0.0 : respostas.fold<int>(0, (s, r) => s + r.segundos) / respostas.length;
    var melhor = 0, atual = 0;
    for (final r in respostas) {
      atual = r.certa ? atual + 1 : 0;
      if (atual > melhor) melhor = atual;
    }
    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 20, 16, 24),
          children: [
            Text(t.resultado.toUpperCase(), style: const TextStyle(fontSize: 11, letterSpacing: 1.5, color: Cores.dourado, fontWeight: FontWeight.w700)),
            const SizedBox(height: 10),
            Center(child: Text('$pontos', style: estiloMarca(tamanho: 84, cor: Cores.douradoClaro, peso: FontWeight.w700))),
            Center(child: Text(t.pontos, style: const TextStyle(color: Cores.textoSuave))),
            const SizedBox(height: 18),
            Row(children: [
              _Medida(valor: '$acertos / ${perguntas.length}', rotulo: t.certasRotulo),
              const SizedBox(width: 10),
              _Medida(valor: '${media.toStringAsFixed(1)} s', rotulo: t.tempoMedio),
              const SizedBox(width: 10),
              _Medida(valor: '$melhor', rotulo: t.melhorSerie),
            ]),
            const SizedBox(height: 22),
            Text(t.revisao.toUpperCase(), style: const TextStyle(fontSize: 11, letterSpacing: 1.5, color: Cores.textoSuave, fontWeight: FontWeight.w700)),
            const SizedBox(height: 8),
            for (var k = 0; k < perguntas.length; k++)
              Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: Cores.superficie, borderRadius: BorderRadius.circular(14)),
                child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Icon(respostas[k].certa ? Icons.check_circle_rounded : Icons.cancel_rounded,
                      color: respostas[k].certa ? Cores.certo : Cores.errado, size: 20),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(perguntas[k].enunciado(lingua), style: const TextStyle(fontSize: 13, height: 1.3)),
                      const SizedBox(height: 4),
                      Text(perguntas[k].opcoes(lingua)[perguntas[k].certa], style: const TextStyle(color: Cores.certo, fontWeight: FontWeight.w700, fontSize: 13)),
                    ]),
                  ),
                ]),
              ),
            const SizedBox(height: 14),
            FilledButton(
              onPressed: () => Navigator.of(context).pushReplacement(MaterialPageRoute(
                builder: (_) => EcraJogo(perguntas: banco.sortear(topico: topico), lingua: lingua, banco: banco, topico: topico),
              )),
              child: Text(t.jogarOutra),
            ),
            TextButton(
              onPressed: () => Navigator.of(context).popUntil((r) => r.isFirst),
              style: TextButton.styleFrom(foregroundColor: Cores.textoSuave, minimumSize: const Size.fromHeight(52)),
              child: Text(t.voltarInicio, style: const TextStyle(fontWeight: FontWeight.w800, letterSpacing: 0.8)),
            ),
          ],
        ),
      ),
    );
  }
}

class _Medida extends StatelessWidget {
  const _Medida({required this.valor, required this.rotulo});
  final String valor;
  final String rotulo;
  @override
  Widget build(BuildContext context) => Expanded(
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 14),
          decoration: BoxDecoration(color: Cores.superficie, borderRadius: BorderRadius.circular(14), border: Border.all(color: Cores.linha)),
          child: Column(children: [
            Text(valor, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
            const SizedBox(height: 2),
            Text(rotulo, style: const TextStyle(fontSize: 11, color: Cores.textoSuave)),
          ]),
        ),
      );
}
