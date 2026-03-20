from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ProblemRecord:
    platform: str
    problem_id: str
    title: str
    difficulty_label: Optional[str] = None   # easy/medium/hard for LC
    rating: Optional[int] = None             # CF problem rating
    topics: List[str] = field(default_factory=list)
    solved_at: Optional[int] = None


@dataclass
class ContestRecord:
    contest_id: str
    contest_name: str
    rank: Optional[int] = None
    rating_change: Optional[int] = None
    old_rating: Optional[int] = None
    new_rating: Optional[int] = None
    attended_at: Optional[int] = None


@dataclass
class CodeforcesProfile:
    handle: str
    current_rating: Optional[int]
    max_rating: Optional[int]
    rank: Optional[str]
    max_rank: Optional[str]
    total_solved: int
    contests: List[ContestRecord]
    solved_problems: List[ProblemRecord]


@dataclass
class LeetCodeProfile:
    username: str
    total_solved: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    acceptance_rate: Optional[float]
    contest_rating: Optional[float]
    contest_count: int
    solved_problems: List[ProblemRecord]
    contests: List[ContestRecord]