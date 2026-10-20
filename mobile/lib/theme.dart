import 'package:flutter/material.dart';

/// AgriSmart palette (paper, forest green, gold) matching the Streamlit dashboard.
const Color kAccent = Color(0xFF244F3B);
const Color kClay = Color(0xFFB07D14); // darker gold so it stays readable as text
const Color kBackground = Color(0xFFF8F6EF);
const Color kSurface = Color(0xFFFCFAF5);
const Color kBorder = Color(0xFFDCD8CC);
const Color kDark = Color(0xFF213329);
const Color kWarn = Color(0xFF8A6414);
const Color kDanger = Color(0xFFB9483D);

ThemeData buildTheme() {
  final base = ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: kAccent, surface: kSurface),
    useMaterial3: true,
  );
  return base.copyWith(
    scaffoldBackgroundColor: kBackground,
    appBarTheme: const AppBarTheme(
      backgroundColor: kBackground,
      foregroundColor: kDark,
      elevation: 0,
      centerTitle: false,
    ),
    cardTheme: CardThemeData(
      color: kSurface,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: const BorderSide(color: kBorder),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: kSurface,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: kBorder),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: kAccent,
        minimumSize: const Size.fromHeight(48),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    ),
  );
}

Color statusColor(String status) {
  switch (status) {
    case 'Optimal':
      return kAccent;
    case 'Low':
      return kDanger;
    case 'High':
      return kWarn;
    default:
      return kDark;
  }
}
