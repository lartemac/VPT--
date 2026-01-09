---
name: game-logic
description: 游戏逻辑开发，专长于7局4胜制比赛系统、流局判定、胜负优先级规则。适用于麻将、扑克等竞技类游戏。核心规则：1.正常击杀 > 2.流局判定 > 3.平局。触发关键词：游戏、7局4胜、流局、比赛、胜负判定。
allowed-tools: Bash, Read, Write, Edit
model: sonnet
---

# 游戏逻辑开发 Skill

## 核心规则体系

### 胜负优先级（不可更改）
```
1. 正常击杀（最高优先级）
   ↓
2. 流局判定（中等优先级）
   ↓
3. 平局（最低优先级）
```

### 7局4胜制规则
```
比赛局数：7局
胜利条件：先获得4胜的一方获胜
特殊规则：流局不计入胜负，但消耗一局
```

## 何时激活此 Skill

当用户提及以下关键词时，自动激活此 Skill：
- **游戏类型**：游戏、比赛、竞技
- **赛制**：7局4胜、BO7、Best of 7
- **特殊规则**：流局、麻将、和局、平局

## 核心功能实现

### 1. 比赛状态管理

#### 数据结构设计
```python
# game_state.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

class GameResult(Enum):
    """比赛结果枚举"""
    PENDING = "pending"        # 进行中
    PLAYER_A_WIN = "a_win"    # 玩家A获胜
    PLAYER_B_WIN = "b_win"    # 玩家B获胜
    DRAW = "draw"             # 平局（理论上不应出现）
    ABORTED = "aborted"       # 中止

class RoundResult(Enum):
    """单局结果枚举（按优先级排序）"""
    NORMAL_KILL = "normal_kill"  # 正常击杀（优先级1）
    FLOW_GAME = "flow_game"      # 流局（优先级2）
    DRAW = "draw"                # 平局（优先级3）

@dataclass
class RoundState:
    """单局状态"""
    round_number: int           # 局数（1-7）
    player_a_score: int        # 玩家A得分
    player_b_score: int        # 玩家B得分
    result: Optional[RoundResult]  # 本局结果
    winner: Optional[str]      # 获胜玩家（'A' 或 'B'）
    is_flow_game: bool = False # 是否流局
    details: dict = None       # 详细信息

@dataclass
class MatchState:
    """比赛状态"""
    player_a_wins: int = 0      # 玩家A胜场数
    player_b_wins: int = 0      # 玩家B胜场数
    round_history: List[RoundState] = None  # 局历史
    current_round: int = 0      # 当前局数
    match_result: Optional[GameResult] = None  # 比赛结果
    winner: Optional[str] = None # 获胜玩家

    def __post_init__(self):
        if self.round_history is None:
            self.round_history = []
```

### 2. 胜负判定逻辑（核心）

#### 判定流程
```python
# game_logic.py
from game_state import RoundState, MatchState, RoundResult, GameResult

class GameJudge:
    """游戏裁判类"""

    @staticmethod
    def judge_round(
        player_a_score: int,
        player_b_score: int,
        is_flow_game: bool = False,
        special_conditions: dict = None
    ) -> RoundResult:
        """判定单局结果

        Args:
            player_a_score: 玩家A得分
            player_b_score: 玩家B得分
            is_flow_game: 是否流局
            special_conditions: 特殊条件（如特殊牌型、技能等）

        Returns:
            RoundResult: 本局结果

        判定优先级：
        1. 正常击杀（一方得分 > 0，另一方 = 0）
        2. 流局（双方得分 = 0，或满足流局条件）
        3. 平局（双方得分 > 0 且相等）
        """
        # 优先级1：正常击杀
        if player_a_score > 0 and player_b_score == 0:
            return RoundResult.NORMAL_KILL
        elif player_b_score > 0 and player_a_score == 0:
            return RoundResult.NORMAL_KILL

        # 优先级2：流局判定
        if is_flow_game:
            return RoundResult.FLOW_GAME
        if player_a_score == 0 and player_b_score == 0:
            return RoundResult.FLOW_GAME

        # 优先级3：平局
        if player_a_score == player_b_score:
            return RoundResult.FLOW_GAME  # 相等分数视为流局

        # 默认情况：分数不相等，但都不是0
        # 根据7局4胜制规则，判定高分者获胜
        if player_a_score > player_b_score:
            return RoundResult.NORMAL_KILL
        else:
            return RoundResult.NORMAL_KILL

    @staticmethod
    def determine_round_winner(
        result: RoundResult,
        player_a_score: int,
        player_b_score: int
    ) -> Optional[str]:
        """确定本局获胜者

        Args:
            result: 局结果
            player_a_score: 玩家A得分
            player_b_score: 玩家B得分

        Returns:
            'A', 'B', 或 None（流局）
        """
        if result == RoundResult.FLOW_GAME:
            return None  # 流局无获胜者

        if result == RoundResult.NORMAL_KILL:
            if player_a_score > player_b_score:
                return 'A'
            elif player_b_score > player_a_score:
                return 'B'

        return None  # 平局或异常情况

    @staticmethod
    def check_match_over(player_a_wins: int, player_b_wins: int) -> bool:
        """检查比赛是否结束

        Args:
            player_a_wins: 玩家A胜场数
            player_b_wins: 玩家B胜场数

        Returns:
            bool: 比赛是否结束
        """
        # 7局4胜制：一方先达到4胜即结束
        return player_a_wins >= 4 or player_b_wins >= 4

    @staticmethod
    def determine_match_winner(player_a_wins: int, player_b_wins: int) -> Optional[str]:
        """确定比赛获胜者

        Args:
            player_a_wins: 玩家A胜场数
            player_b_wins: 玩家B胜场数

        Returns:
            'A', 'B', 或 None（比赛未结束）
        """
        if player_a_wins >= 4:
            return 'A'
        elif player_b_wins >= 4:
            return 'B'
        return None
```

### 3. 比赛流程控制

#### 比赛管理器
```python
# match_manager.py
from game_state import MatchState, RoundState, RoundResult, GameResult
from game_logic import GameJudge

class MatchManager:
    """比赛管理器"""

    def __init__(self):
        self.match_state = MatchState()
        self.judge = GameJudge()

    def start_round(self) -> int:
        """开始新的一局

        Returns:
            int: 局数
        """
        # 检查比赛是否已结束
        if self.match_state.match_result:
            raise Exception('比赛已结束，无法开始新局')

        # 检查是否已达到7局
        if self.match_state.current_round >= 7:
            raise Exception('已达到最大局数（7局）')

        # 开始新局
        self.match_state.current_round += 1
        return self.match_state.current_round

    def end_round(
        self,
        player_a_score: int,
        player_b_score: int,
        is_flow_game: bool = False,
        details: dict = None
    ) -> RoundState:
        """结束当前局

        Args:
            player_a_score: 玩家A得分
            player_b_score: 玩家B得分
            is_flow_game: 是否流局
            details: 详细信息

        Returns:
            RoundState: 本局状态
        """
        # 判定本局结果
        result = self.judge.judge_round(
            player_a_score,
            player_b_score,
            is_flow_game
        )

        # 确定获胜者
        winner = self.judge.determine_round_winner(
            result,
            player_a_score,
            player_b_score
        )

        # 更新胜场数
        if winner == 'A':
            self.match_state.player_a_wins += 1
        elif winner == 'B':
            self.match_state.player_b_wins += 1

        # 创建局状态
        round_state = RoundState(
            round_number=self.match_state.current_round,
            player_a_score=player_a_score,
            player_b_score=player_b_score,
            result=result,
            winner=winner,
            is_flow_game=(result == RoundResult.FLOW_GAME),
            details=details or {}
        )

        # 添加到历史
        self.match_state.round_history.append(round_state)

        # 检查比赛是否结束
        if self.judge.check_match_over(
            self.match_state.player_a_wins,
            self.match_state.player_b_wins
        ):
            match_winner = self.judge.determine_match_winner(
                self.match_state.player_a_wins,
                self.match_state.player_b_wins
            )
            self.match_state.winner = match_winner
            self.match_state.match_result = GameResult.PLAYER_A_WIN if match_winner == 'A' else GameResult.PLAYER_B_WIN

        return round_state

    def get_match_summary(self) -> dict:
        """获取比赛摘要

        Returns:
            dict: 比赛摘要
        """
        return {
            'match_result': self.match_state.match_result.value if self.match_state.match_result else 'pending',
            'winner': self.match_state.winner,
            'player_a_wins': self.match_state.player_a_wins,
            'player_b_wins': self.match_state.player_b_wins,
            'total_rounds': self.match_state.current_round,
            'rounds': [
                {
                    'round': r.round_number,
                    'score_a': r.player_a_score,
                    'score_b': r.player_b_score,
                    'result': r.result.value,
                    'winner': r.winner,
                    'is_flow_game': r.is_flow_game
                }
                for r in self.match_state.round_history
            ]
        }
```

### 4. 流局判定逻辑（麻将示例）

#### 麻将流局判定
```python
# mahjong_flow_game.py

class MahjongFlowGameJudge:
    """麻将流局判定器"""

    @staticmethod
    def is_flow_game(
        remaining_tiles: int,
        is_riichi: bool = False,
        four_wind_discard: bool = False,
        four_kong: bool = False,
        triple_ron: bool = False
    ) -> bool:
        """判定是否流局

        Args:
            remaining_tiles: 剩余牌数
            is_riichi: 是否有人立直
            four_wind_discard: 是否四风连打
            four_kong: 是否四杠散了
            triple_ron: 是否三家和了

        Returns:
            bool: 是否流局
        """
        # 规则1：荒牌（牌墙摸完）
        if remaining_tiles == 0:
            return True

        # 规则2：四风连打（第一轮四家都打出同一风牌）
        if four_wind_discard:
            return True

        # 规则3：四杠散了（两家以上开杠，总计4个杠）
        if four_kong:
            return True

        # 规则4：三家和了（一炮三响）
        if triple_ron:
            return True

        return False

    @staticmethod
    def determine_flow_game_winner(
        player_tenpai: List[bool],
        player_riichi: List[bool]
    ) -> Optional[List[int]]:
        """流局时判定获胜者（听牌者得分）

        Args:
            player_tenpai: 玩家是否听牌 [东,南,西,北]
            player_riichi: 玩家是否立直 [东,南,西,北]

        Returns:
            List[int]: 获胜玩家列表（索引0-3），None表示无人听牌
        """
        if not any(player_tenpai):
            return None  # 无人听牌

        winners = []
        for i, tenpai in enumerate(player_tenpai):
            if tenpai:
                winners.append(i)

        return winners
```

### 5. 完整示例：7局4胜制比赛

#### 示例代码
```python
# example_match.py
from match_manager import MatchManager

def simulate_match():
    """模拟一场7局4胜制比赛"""

    # 创建比赛管理器
    manager = MatchManager()

    print("=== 7局4胜制比赛开始 ===\n")

    # 模拟7局比赛
    match_results = [
        # (玩家A得分, 玩家B得分, 是否流局)
        (100, 0, False),  # 第1局：A获胜
        (0, 150, False),  # 第2局：B获胜
        (80, 0, False),   # 第3局：A获胜
        (0, 0, True),     # 第4局：流局
        (120, 0, False),  # 第5局：A获胜
        (0, 90, False),   # 第6局：B获胜
        (110, 0, False),  # 第7局：A获胜（4胜3负）
    ]

    for round_num, (score_a, score_b, is_flow) in enumerate(match_results, 1):
        # 开始新局
        manager.start_round()
        print(f"--- 第{round_num}局 ---")

        # 结束局
        round_state = manager.end_round(score_a, score_b, is_flow)

        # 显示结果
        result_text = {
            'normal_kill': '正常击杀',
            'flow_game': '流局',
            'draw': '平局'
        }[round_state.result.value]

        winner_text = f"玩家{round_state.winner}" if round_state.winner else "无（流局）"
        print(f"结果: {result_text}, 获胜者: {winner_text}")
        print(f"比分: A {score_a} - {score_b} B")
        print(f"累计胜场: A {manager.match_state.player_a_wins} - {manager.match_state.player_b_wins} B")

        # 检查比赛是否结束
        if manager.match_state.match_result:
            print(f"\n=== 比赛结束 ===")
            print(f"获胜者: 玩家{manager.match_state.winner}")
            print(f"最终比分: {manager.match_state.player_a_wins} - {manager.match_state.player_b_wins}")
            break

        print()

    # 显示比赛摘要
    print("\n=== 比赛摘要 ===")
    summary = manager.get_match_summary()
    for round_data in summary['rounds']:
        flow_mark = " [流局]" if round_data['is_flow_game'] else ""
        print(f"第{round_data['round']}局: A {round_data['score_a']} - {round_data['score_b']} B, 获胜者: {round_data['winner']}{flow_mark}")

if __name__ == '__main__':
    simulate_match()
```

#### 输出示例
```
=== 7局4胜制比赛开始 ===

--- 第1局 ---
结果: 正常击杀, 获胜者: 玩家A
比分: A 100 - 0 B
累计胜场: A 1 - 0 B

--- 第2局 ---
结果: 正常击杀, 获胜者: 玩家B
比分: A 0 - 150 B
累计胜场: A 1 - 1 B

--- 第3局 ---
结果: 正常击杀, 获胜者: 玩家A
比分: A 80 - 0 B
累计胜场: A 2 - 1 B

--- 第4局 ---
结果: 流局, 获胜者: 无（流局）
比分: A 0 - 0 B
累计胜场: A 2 - 1 B

--- 第5局 ---
结果: 正常击杀, 获胜者: 玩家A
比分: A 120 - 0 B
累计胜场: A 3 - 1 B

--- 第6局 ---
结果: 正常击杀, 获胜者: 玩家B
比分: A 0 - 90 B
累计胜场: A 3 - 2 B

--- 第7局 ---
结果: 正常击杀, 获胜者: 玩家A
比分: A 110 - 0 B
累计胜场: A 4 - 2 B

=== 比赛结束 ===
获胜者: 玩家A
最终比分: 4 - 2

=== 比赛摘要 ===
第1局: A 100 - 0 B, 获胜者: A
第2局: A 0 - 150 B, 获胜者: B
第3局: A 80 - 0 B, 获胜者: A
第4局: A 0 - 0 B, 获胜者: None [流局]
第5局: A 120 - 0 B, 获胜者: A
第6局: A 0 - 90 B, 获胜者: B
第7局: A 110 - 0 B, 获胜者: A
```

## 边界情况处理

### 1. 全流局情况
```python
# 如果7局全部流局，如何判定？
def handle_all_flow_games():
    """处理全部流局的情况"""
    manager = MatchManager()

    for i in range(7):
        manager.start_round()
        manager.end_round(0, 0, is_flow_game=True)

    # 最终状态：双方都是0胜
    if manager.match_state.player_a_wins == 0 and manager.match_state.player_b_wins == 0:
        # 特殊规则：延长赛或平局
        print("全部流局，进入延长赛或判定为平局")
        # 根据具体游戏规则处理
```

### 2. 异常终止
```python
def abort_match(manager: MatchManager, reason: str):
    """中止比赛"""
    manager.match_state.match_result = GameResult.ABORTED
    print(f"比赛中止: {reason}")
    # 根据中止时的胜场数判定获胜者，或直接取消比赛
```

## 测试用例

```python
# test_game_logic.py
import unittest
from game_logic import GameJudge
from game_state import RoundResult

class TestGameJudge(unittest.TestCase):

    def setUp(self):
        self.judge = GameJudge()

    def test_normal_kill_a_wins(self):
        """测试：玩家A正常获胜"""
        result = self.judge.judge_round(100, 0, is_flow_game=False)
        self.assertEqual(result, RoundResult.NORMAL_KILL)

    def test_normal_kill_b_wins(self):
        """测试：玩家B正常获胜"""
        result = self.judge.judge_round(0, 150, is_flow_game=False)
        self.assertEqual(result, RoundResult.NORMAL_KILL)

    def test_flow_game_both_zero(self):
        """测试：双方0分，流局"""
        result = self.judge.judge_round(0, 0, is_flow_game=False)
        self.assertEqual(result, RoundResult.FLOW_GAME)

    def test_explicit_flow_game(self):
        """测试：显式流局"""
        result = self.judge.judge_round(10, 20, is_flow_game=True)
        self.assertEqual(result, RoundResult.FLOW_GAME)

    def test_draw_equal_scores(self):
        """测试：分数相等，视为流局"""
        result = self.judge.judge_round(50, 50, is_flow_game=False)
        self.assertEqual(result, RoundResult.FLOW_GAME)

if __name__ == '__main__':
    unittest.main()
```

## 与其他 Skill 的协作

- **python-tutoring**：学习 Python 游戏开发基础
- **weapp-development**：开发微信小程序游戏
- **quantitative-trading**：应用概率论和统计分析

---

**最后更新**：2026-01-10
**适用游戏**：麻将、扑克、卡牌等竞技类游戏
**核心规则**：7局4胜制，胜负优先级（正常击杀 > 流局 > 平局）
