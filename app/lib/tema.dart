import 'package:material_ui/material_ui.dart';

/// Paleta provisória do QUIZLUX. A paleta e as boards oficiais do design não estão no
/// repositório: troquem os valores aqui (só este ficheiro) quando as tivermos.
class Cores {
  static const fundo = Color(0xFF0E1020);
  static const superficie = Color(0xFF1A1D33);
  static const destaque = Color(0xFFFFC857);
  static const texto = Color(0xFFF2F3F8);
  static const textoSuave = Color(0xFF9EA3C0);
  static const certo = Color(0xFF3DDC97);
  static const errado = Color(0xFFFF5C7A);
}

ThemeData temaQuizlux() => ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: Cores.fundo,
      colorScheme: const ColorScheme.dark(
        primary: Cores.destaque,
        surface: Cores.superficie,
        onSurface: Cores.texto,
      ),
      appBarTheme: const AppBarTheme(backgroundColor: Cores.fundo, foregroundColor: Cores.texto, elevation: 0),
    );
