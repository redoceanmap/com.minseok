import 'package:flutter/material.dart';

void main() => runApp(const TaperApp());

/// 웹(`www/app/(seoul)/page.tsx`) 인트로와 동일한 와인/크림 테마.
class AppColors {
  static const background = Color(0xFFFAF7F2);
  static const surface = Color(0xFFFFFFFF);
  static const foreground = Color(0xFF1A1A1A);
  static const foregroundMuted = Color(0xFF6B6B6B);
  static const border = Color(0xFFE8E2D9);
  static const brand = Color(0xFF722F37);
  static const brandDeep = Color(0xFF4A1D24);
}

class TaperApp extends StatelessWidget {
  const TaperApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Taper',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: AppColors.background,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.brand,
          primary: AppColors.brand,
          surface: AppColors.surface,
        ),
        fontFamily: 'Pretendard',
      ),
      home: const IntroScreen(),
    );
  }
}

class _Chip {
  const _Chip(this.icon, this.label, this.prompt);
  final IconData icon;
  final String label;
  final String prompt;
}

class _Area {
  const _Area(this.name, this.category, this.change, this.note);
  final String name;
  final String category;
  final String change;
  final String note;
}

const _quickChips = [
  _Chip(Icons.storefront_outlined, '업종으로 찾기', '어떤 업종이 잘 될까요?'),
  _Chip(Icons.account_balance_wallet_outlined, '예산으로 찾기', '3000만원으로 시작할 수 있는 곳 알려주세요'),
  _Chip(Icons.place_outlined, '동네로 찾기', '성수동 상권 어때요?'),
  _Chip(Icons.bar_chart, '상권 비교', '성수동이랑 연남동 비교해주세요'),
  _Chip(Icons.auto_awesome_outlined, '추천받기', '지금 가장 핫한 동네 추천해주세요'),
];

const _trendingAreas = [
  _Area('성수동', '카페·디저트', '+12%', '젊은 손님이 늘고 있어요'),
  _Area('연남동', '베이커리', '+8%', '주말 매출이 강해요'),
  _Area('망원동', '외식업', '+6%', '객단가가 올라가요'),
  _Area('익선동', '야간 상권', '+5%', '밤에 사람이 모여요'),
];

String _greeting(int hour) {
  if (hour < 12) return '좋은 아침이에요';
  if (hour < 18) return '오후예요';
  return '오늘 하루 어땠어요';
}

class IntroScreen extends StatelessWidget {
  const IntroScreen({super.key});

  void _send(BuildContext context, String text) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          content: Text(text),
          backgroundColor: AppColors.brandDeep,
          behavior: SnackBarBehavior.floating,
        ),
      );
  }

  @override
  Widget build(BuildContext context) {
    final greeting = _greeting(DateTime.now().hour);

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 720),
            child: ListView(
              padding: const EdgeInsets.fromLTRB(20, 32, 20, 32),
              children: [
                Text(
                  greeting,
                  style: const TextStyle(
                    fontSize: 14,
                    color: AppColors.foregroundMuted,
                  ),
                ),
                const SizedBox(height: 12),
                _Headline(),
                const SizedBox(height: 28),
                _ChatInput(onSubmit: (t) => _send(context, t)),
                const SizedBox(height: 16),
                _ChipRow(onTap: (p) => _send(context, p)),
                const SizedBox(height: 56),
                _TrendingSection(onTap: (p) => _send(context, p)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _Headline extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return RichText(
      text: const TextSpan(
        style: TextStyle(
          fontSize: 34,
          fontWeight: FontWeight.w600,
          height: 1.3,
          letterSpacing: -0.5,
          color: AppColors.foreground,
        ),
        children: [
          TextSpan(text: '서울 상권,\n'),
          TextSpan(
            text: '숨겨진 기회',
            style: TextStyle(color: AppColors.brand),
          ),
          TextSpan(text: '를 찾아드릴게요'),
        ],
      ),
    );
  }
}

class _ChatInput extends StatefulWidget {
  const _ChatInput({required this.onSubmit});
  final ValueChanged<String> onSubmit;

  @override
  State<_ChatInput> createState() => _ChatInputState();
}

class _ChatInputState extends State<_ChatInput> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _submit() {
    final text = _controller.text.trim();
    if (text.isEmpty) return;
    widget.onSubmit(text);
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
        boxShadow: const [
          BoxShadow(
            color: Color(0x0A000000),
            blurRadius: 12,
            offset: Offset(0, 4),
          ),
        ],
      ),
      padding: const EdgeInsets.fromLTRB(16, 4, 8, 4),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              onSubmitted: (_) => _submit(),
              style: const TextStyle(
                fontSize: 16,
                color: AppColors.foreground,
              ),
              decoration: const InputDecoration(
                hintText: '어디서 장사를 시작해볼까요?',
                hintStyle: TextStyle(color: AppColors.foregroundMuted),
                border: InputBorder.none,
                isCollapsed: true,
                contentPadding: EdgeInsets.symmetric(vertical: 14),
              ),
            ),
          ),
          Material(
            color: AppColors.brand,
            shape: const CircleBorder(),
            child: InkWell(
              customBorder: const CircleBorder(),
              onTap: _submit,
              child: const Padding(
                padding: EdgeInsets.all(10),
                child: Icon(Icons.arrow_upward, size: 20, color: Colors.white),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ChipRow extends StatelessWidget {
  const _ChipRow({required this.onTap});
  final ValueChanged<String> onTap;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: [
        for (final chip in _quickChips)
          Material(
            color: AppColors.surface.withValues(alpha: 0.6),
            borderRadius: BorderRadius.circular(999),
            child: InkWell(
              borderRadius: BorderRadius.circular(999),
              onTap: () => onTap(chip.prompt),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(999),
                  border: Border.all(color: AppColors.border),
                ),
                padding:
                    const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(chip.icon, size: 15, color: AppColors.brand),
                    const SizedBox(width: 8),
                    Text(
                      chip.label,
                      style: const TextStyle(
                        fontSize: 14,
                        color: AppColors.foreground,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
      ],
    );
  }
}

class _TrendingSection extends StatelessWidget {
  const _TrendingSection({required this.onTap});
  final ValueChanged<String> onTap;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: const [
                Icon(Icons.trending_up, size: 18, color: AppColors.brand),
                SizedBox(width: 8),
                Text(
                  '지금 뜨는 동네',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: AppColors.foreground,
                  ),
                ),
              ],
            ),
            Text(
              '전체 보기',
              style: TextStyle(
                fontSize: 14,
                color: AppColors.foregroundMuted,
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        LayoutBuilder(
          builder: (context, constraints) {
            final isWide = constraints.maxWidth >= 520;
            final columns = isWide ? 4 : 2;
            const gap = 12.0;
            final cardWidth =
                (constraints.maxWidth - gap * (columns - 1)) / columns;
            return Wrap(
              spacing: gap,
              runSpacing: gap,
              children: [
                for (final area in _trendingAreas)
                  SizedBox(
                    width: cardWidth,
                    child: _AreaCard(
                      area: area,
                      onTap: () => onTap('${area.name} 상권 어때요?'),
                    ),
                  ),
              ],
            );
          },
        ),
      ],
    );
  }
}

class _AreaCard extends StatelessWidget {
  const _AreaCard({required this.area, required this.onTap});
  final _Area area;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.surface,
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: onTap,
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: AppColors.border),
          ),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    area.name,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: AppColors.foreground,
                    ),
                  ),
                  Text(
                    area.change,
                    style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: AppColors.brand,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              Text(
                area.category,
                style: const TextStyle(
                  fontSize: 12,
                  color: AppColors.foregroundMuted,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                area.note,
                style: const TextStyle(
                  fontSize: 12,
                  height: 1.3,
                  color: AppColors.foreground,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
