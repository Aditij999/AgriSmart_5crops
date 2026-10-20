import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app_state.dart';
import 'chat_screen.dart';
import 'dashboard_screen.dart';
import 'history_screen.dart';
import 'predict_screen.dart';

/// Bottom-nav shell. The history tab is rebuilt on selection so it always
/// reflects predictions made in the other tabs.
class HomeShell extends StatefulWidget {
  const HomeShell({super.key});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int _index = 0;
  Key _historyKey = UniqueKey();

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AppState>().user;
    final pages = [
      DashboardScreen(onNewAnalysis: () => setState(() => _index = 1)),
      const PredictScreen(),
      HistoryScreen(key: _historyKey),
      const ChatScreen(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('AgriSmart DSS 🌾'),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.account_circle_outlined),
            onSelected: (value) {
              if (value == 'logout') context.read<AppState>().logout();
            },
            itemBuilder: (context) => [
              PopupMenuItem(
                enabled: false,
                child: Text('Signed in as ${user?.username ?? ''}'),
              ),
              const PopupMenuItem(value: 'logout', child: Text('Log out')),
            ],
          ),
        ],
      ),
      body: IndexedStack(index: _index, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (index) => setState(() {
          _index = index;
          if (index == 2) _historyKey = UniqueKey();
        }),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard_outlined), label: 'Dashboard'),
          NavigationDestination(icon: Icon(Icons.science_outlined), label: 'Predict'),
          NavigationDestination(icon: Icon(Icons.history), label: 'History'),
          NavigationDestination(icon: Icon(Icons.chat_bubble_outline), label: 'Chat'),
        ],
      ),
    );
  }
}
