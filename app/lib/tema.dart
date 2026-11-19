import 'package:material_ui/material_ui.dart';

/// Paleta oficial do QUIZLUX (indicada pelo Andre em 19/11/2026).
/// As boards do design (quizlux-design.zip) ainda não chegaram ao repositório.
class Cores {
  static const fundo = Color(0xFF0B1428);
  static const superficie = Color(0xFF152747);
  static const superficie2 = Color(0xFF1C345A);
  static const dourado = Color(0xFFC6A45A);
  static const douradoClaro = Color(0xFFE5CD8F);
  static const azul = Color(0xFF4389D9);
  static const texto = Color(0xFFF5F5F2);
  static const textoSuave = Color(0xFFAABBD5);
  static const linha = Color(0xFF26426B);
  static const certo = Color(0xFF4CC38A);
  static const errado = Color(0xFFE26D6D);

  /// Compatibilidade com o código anterior: o destaque é o dourado.
  static const destaque = dourado;
}

/// Manrope na interface; Cormorant Garamond só nos momentos de marca.
const fonteInterface = 'Manrope';
const fonteMarca = 'CormorantGaramond';

TextStyle estiloMarca({double tamanho = 28, Color cor = Cores.douradoClaro, FontWeight peso = FontWeight.w600, double espaco = 0}) =>
    TextStyle(fontFamily: fonteMarca, fontSize: tamanho, color: cor, fontWeight: peso, letterSpacing: espaco);

ThemeData temaQuizlux() => ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      fontFamily: fonteInterface,
      scaffoldBackgroundColor: Cores.fundo,
      colorScheme: const ColorScheme.dark(
        primary: Cores.dourado,
        onPrimary: Cores.fundo,
        secondary: Cores.azul,
        surface: Cores.superficie,
        onSurface: Cores.texto,
        outline: Cores.linha,
      ),
      cardTheme: CardThemeData(
        color: Cores.superficie,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14), side: const BorderSide(color: Cores.linha)),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: Cores.dourado,
          foregroundColor: Cores.fundo,
          minimumSize: const Size.fromHeight(52),
          textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        ),
      ),
      appBarTheme: const AppBarTheme(backgroundColor: Cores.fundo, foregroundColor: Cores.texto, elevation: 0),
    );
