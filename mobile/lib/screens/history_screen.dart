import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api_client.dart';
import '../app_state.dart';
import '../models.dart';
import '../theme.dart';
import '../widgets.dart';
import 'compare_screen.dart';
import 'result_screen.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<HistoryItem> _items = const [];
  final Set<int> _selected = {};
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final page = await context.read<AppState>().api.history(limit: 100);
      if (!mounted) return;
      setState(() {
        _items = page.items;
        _selected.removeWhere(
            (id) => !page.items.any((item) => item.id == id));
        _loading = false;
      });
    } on ApiException catch (error) {
      if (!mounted) return;
      setState(() {
        _error = error.message;
        _loading = false;
      });
    }
  }

  Future<void> _open(HistoryItem item) async {
    try {
      final result = await context.read<AppState>().api.historyEntry(item.id);
      if (!mounted) return;
      await Navigator.of(context)
          .push(MaterialPageRoute(builder: (_) => ResultScreen(result: result)));
    } on ApiException catch (error) {
      _showSnack(error.message);
    }
  }

  Future<void> _delete(HistoryItem item) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete this analysis?'),
        content: Text(
            '${item.chosenCrop} · ${kDateFormat.format(item.createdAt)} will be removed permanently.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancel')),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: kDanger),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Delete'),
          ),
        ],
      ),
    );
    if (confirmed != true || !mounted) return;

    try {
      await context.read<AppState>().api.deleteHistoryEntry(item.id);
      _selected.remove(item.id);
      await _load();
    } on ApiException catch (error) {
      _showSnack(error.message);
    }
  }

  Future<void> _clearAll() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Clear all history?'),
        content: const Text('Every saved analysis for your account will be deleted.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancel')),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: kDanger),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Clear all'),
          ),
        ],
      ),
    );
    if (confirmed != true || !mounted) return;

    try {
      await context.read<AppState>().api.clearHistory();
      _selected.clear();
      await _load();
    } on ApiException catch (error) {
      _showSnack(error.message);
    }
  }

  Future<void> _compare() async {
    try {
      final result =
          await context.read<AppState>().api.compare(_selected.toList()..sort());
      if (!mounted) return;
      await Navigator.of(context)
          .push(MaterialPageRoute(builder: (_) => CompareScreen(result: result)));
    } on ApiException catch (error) {
      _showSnack(error.message);
    }
  }

  void _showSnack(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_error != null) {
      return Padding(
        padding: const EdgeInsets.all(16),
        child: ErrorBanner(message: _error!, onRetry: _load),
      );
    }
    if (_items.isEmpty) {
      return const EmptyState(
          message: 'No saved analyses yet.\nRun one from the Predict tab.');
    }

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  _selected.isEmpty
                      ? '${_items.length} saved analyses'
                      : '${_selected.length} selected (2–4 to compare)',
                  style: const TextStyle(color: Color(0xFF68756D), fontSize: 12),
                ),
              ),
              TextButton.icon(
                onPressed: _selected.length >= 2 && _selected.length <= 4
                    ? _compare
                    : null,
                icon: const Icon(Icons.compare_arrows, size: 18),
                label: const Text('Compare'),
              ),
              IconButton(
                tooltip: 'Clear all',
                onPressed: _clearAll,
                icon: const Icon(Icons.delete_sweep_outlined, color: kDanger),
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _load,
            child: ListView.separated(
              padding: const EdgeInsets.fromLTRB(16, 4, 16, 16),
              itemCount: _items.length,
              separatorBuilder: (_, __) => const SizedBox(height: 10),
              itemBuilder: (context, index) {
                final item = _items[index];
                final selected = _selected.contains(item.id);
                return Card(
                  child: ListTile(
                    onTap: () => _open(item),
                    leading: Checkbox(
                      value: selected,
                      activeColor: kAccent,
                      onChanged: (checked) => setState(() {
                        if (checked == true) {
                          _selected.add(item.id);
                        } else {
                          _selected.remove(item.id);
                        }
                      }),
                    ),
                    title: Text(
                      item.label?.isNotEmpty == true
                          ? '${item.label} · ${item.chosenCrop}'
                          : item.chosenCrop,
                      style: const TextStyle(fontWeight: FontWeight.w600),
                    ),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(kDateFormat.format(item.createdAt),
                            style: const TextStyle(fontSize: 12)),
                        Text(
                          'N ${item.soilInput.nitrogen.toStringAsFixed(0)} · '
                          'P ${item.soilInput.phosphorus.toStringAsFixed(0)} · '
                          'K ${item.soilInput.potassium.toStringAsFixed(0)} · '
                          'pH ${item.soilInput.ph.toStringAsFixed(1)} · '
                          '${formatYield(item.predictedYieldKgHa)}',
                          style: const TextStyle(fontSize: 11, color: Color(0xFF68756D)),
                        ),
                      ],
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete_outline, color: kDanger),
                      onPressed: () => _delete(item),
                    ),
                  ),
                );
              },
            ),
          ),
        ),
      ],
    );
  }
}
