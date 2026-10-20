import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api_client.dart';
import '../app_state.dart';
import '../models.dart';
import '../theme.dart';
import '../widgets.dart';
import 'result_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key, required this.onNewAnalysis});

  final VoidCallback onNewAnalysis;

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  late Future<({int total, List<HistoryItem> items})> _future;

  @override
  void initState() {
    super.initState();
    _future = context.read<AppState>().api.history(limit: 5);
  }

  void _reload() {
    setState(() => _future = context.read<AppState>().api.history(limit: 5));
  }

  Future<void> _open(int id) async {
    final api = context.read<AppState>().api;
    final result = await api.historyEntry(id);
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => ResultScreen(result: result)),
    );
  }

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();

    return RefreshIndicator(
      onRefresh: () async => _reload(),
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            'Welcome, ${state.user?.fullName?.isNotEmpty == true ? state.user!.fullName : state.user?.username ?? ''}',
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: kDark),
          ),
          const SizedBox(height: 4),
          const Text(
            'Jowar · Groundnut · Cotton · Sugarcane · Wheat',
            style: TextStyle(color: Color(0xFF68756D), fontSize: 12),
          ),
          const SizedBox(height: 16),
          FilledButton.icon(
            onPressed: widget.onNewAnalysis,
            icon: const Icon(Icons.play_arrow),
            label: const Text('Run a new analysis'),
          ),
          const SizedBox(height: 20),
          FutureBuilder<({int total, List<HistoryItem> items})>(
            future: _future,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Padding(
                  padding: EdgeInsets.all(24),
                  child: Center(child: CircularProgressIndicator()),
                );
              }
              if (snapshot.hasError) {
                final error = snapshot.error;
                return ErrorBanner(
                  message: error is ApiException ? error.message : '$error',
                  onRetry: _reload,
                );
              }

              final data = snapshot.data!;
              if (data.items.isEmpty) {
                return const SectionCard(
                  title: 'No analyses yet',
                  icon: Icons.eco_outlined,
                  child: Text(
                    'Run your first analysis from the Predict tab — every run is '
                    'saved here so you can open, compare and delete it later.',
                  ),
                );
              }

              final latest = data.items.first;
              return Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: StatTile(
                          label: 'Latest target crop',
                          value: latest.chosenCrop,
                          hint: latest.recommendedCrop != null &&
                                  latest.recommendedCrop != latest.chosenCrop
                              ? 'Model suggests ${latest.recommendedCrop}'
                              : 'Matches model suggestion',
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: StatTile(
                          label: 'Latest yield estimate',
                          value: formatYield(latest.predictedYieldKgHa),
                          hint: kDateFormat.format(latest.createdAt),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: StatTile(
                          label: 'Saved analyses',
                          value: '${data.total}',
                          hint: 'Stored privately for your account',
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: StatTile(
                          label: 'Latest soil (N-P-K)',
                          value:
                              '${latest.soilInput.nitrogen.toStringAsFixed(0)}-${latest.soilInput.phosphorus.toStringAsFixed(0)}-${latest.soilInput.potassium.toStringAsFixed(0)}',
                          hint: 'pH ${latest.soilInput.ph.toStringAsFixed(1)}',
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  SectionCard(
                    title: 'Recent analyses',
                    icon: Icons.history,
                    child: Column(
                      children: [
                        for (final item in data.items)
                          ListTile(
                            contentPadding: EdgeInsets.zero,
                            title: Text(item.label?.isNotEmpty == true
                                ? '${item.label} · ${item.chosenCrop}'
                                : item.chosenCrop),
                            subtitle: Text(
                                '${kDateFormat.format(item.createdAt)} · ${formatYield(item.predictedYieldKgHa)}'),
                            trailing: const Icon(Icons.chevron_right),
                            onTap: () => _open(item.id),
                          ),
                      ],
                    ),
                  ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
}
