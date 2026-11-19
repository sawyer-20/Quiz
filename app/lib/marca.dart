import 'package:material_ui/material_ui.dart';
import 'tema.dart';

/// Marca: um anel com cauda (um Q e um temporizador), como na board Brand.
class MarcaPainter extends CustomPainter {
  MarcaPainter({this.cor = Cores.dourado});
  final Color cor;
  @override
  void paint(Canvas canvas, Size size) {
    final k = size.width / 32;
    final p = Paint()
      ..color = cor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.6 * k
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(Offset(15 * k, 15 * k), 10 * k, p);
    canvas.drawLine(Offset(20.5 * k, 20.5 * k), Offset(27 * k, 27 * k), p);
  }

  @override
  bool shouldRepaint(covariant MarcaPainter old) => old.cor != cor;
}

class Marca extends StatelessWidget {
  const Marca({super.key, this.tamanho = 44});
  final double tamanho;
  @override
  Widget build(BuildContext context) => SizedBox(width: tamanho, height: tamanho, child: CustomPaint(painter: MarcaPainter()));
}

/// «QUIZ» a marfim e «LUX» a dourado, Manrope 800 com espaçamento largo.
class Logotipo extends StatelessWidget {
  const Logotipo({super.key, this.tamanho = 28});
  final double tamanho;
  @override
  Widget build(BuildContext context) {
    final base = TextStyle(fontFamily: fonteInterface, fontWeight: FontWeight.w800, fontSize: tamanho, letterSpacing: tamanho * 0.2);
    return Row(mainAxisSize: MainAxisSize.min, children: [
      Marca(tamanho: tamanho * 1.5),
      SizedBox(width: tamanho * 0.3),
      Text.rich(TextSpan(style: base.copyWith(color: Cores.texto), children: [
        const TextSpan(text: 'QUIZ'),
        TextSpan(text: 'LUX', style: base.copyWith(color: Cores.dourado)),
      ])),
    ]);
  }
}

/// Anel do temporizador (72 px na board): arco dourado que se esgota; vermelho nos últimos segundos.
class AnelTempo extends StatelessWidget {
  const AnelTempo({super.key, required this.restante, required this.total, this.tamanho = 72});
  final int restante;
  final int total;
  final double tamanho;
  @override
  Widget build(BuildContext context) => Semantics(
        label: '$restante / $total s',
        child: SizedBox(
          width: tamanho,
          height: tamanho,
          child: CustomPaint(
            painter: _AnelPainter(restante / total, restante <= 3 ? Cores.errado : Cores.dourado),
            child: Center(child: Text('$restante', style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 24, color: Cores.texto))),
          ),
        ),
      );
}

class _AnelPainter extends CustomPainter {
  _AnelPainter(this.fracao, this.cor);
  final double fracao;
  final Color cor;
  @override
  void paint(Canvas canvas, Size size) {
    final r = (size.width - 8) / 2;
    final c = Offset(size.width / 2, size.height / 2);
    final fundo = Paint()
      ..color = Cores.superficie2
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5;
    final arco = Paint()
      ..color = cor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(c, r, fundo);
    canvas.drawArc(Rect.fromCircle(center: c, radius: r), -1.5708, 6.28318 * fracao, false, arco);
  }

  @override
  bool shouldRepaint(covariant _AnelPainter old) => old.fracao != fracao || old.cor != cor;
}
