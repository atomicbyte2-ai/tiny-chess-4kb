# A 4KB Chess Engine Claims Elo 1654. Here's the Receipt.

A chess engine that says it plays at Elo 1654 is making a claim. A claim is cheap; the interesting question is whether anyone can check it. This article is about a small engine built under a hard constraint — 4,096 bytes of Python, standard library only — and the evidence chain that turns its rating from a boast into something verifiable: local trials with numbers, an independent server grade, the game record, and an honest statement of the ceiling it could not reach.

## The constraint

The rules were simple and unforgiving. One file, `main.py`, at most 4,096 bytes. Python 3.13, standard library only, no network, no external packages. The submitted version, v11s, is 4,089 bytes — seven bytes of headroom. Everything the engine knows about chess has to fit in that space: move generation, search, evaluation, and time management.

The engine is a conventional design compressed hard. The board uses the 0x88 representation, a classic trick where a 128-cell array lets off-board detection fall out of a single bit test instead of boundary checks. Search is negamax with alpha-beta pruning, backed by a transposition table implemented as a plain Python dict, killer-move ordering, and quiescence search to keep the horizon effect from turning captures into blunders. The search runs on a fixed node budget rather than a wall-clock timer, which makes its behavior deterministic and reproducible — the same position, the same budget, the same move.

## The number, and how it was measured

The engine was submitted to an open chess-engine competition and graded on the server, not on the author's machine. The server grade is the number that counts:

| Measurement | Value |
|---|---|
| Server grade (Elo) | 1654 |
| Server game record | 5 wins / 0 draws / 1 loss |
| Server rank | 263 of 3,530 |
| Practice floor to pass | 1,154 |
| Margin over the floor | +500 |
| Local 3-trial mean | 1,308 |
| House benchmark (sunfish mean Elo) | 1,360 |
| Paid zone (top 20) | Elo 2,110 |

Two things are worth noting about this table. First, the local trials predicted a lower number than the server measured: a local three-trial mean of 1,308 against a server grade of 1,654. The gap is not a contradiction; local trials and server grading use different opponents, different game counts, and different conditions. A rating is a summary of measurements, and honest reporting shows more than one of them. Second, the game record is right there in the table: five wins, one loss. Six games is a small sample, and the article would be dishonest if it pretended otherwise. The grade is real, and it is also noisy. Both facts can be true at once.

The engine passed the competition's prize gate earlier, too: v11 recorded a mean Elo of 1,486 in the gate check, comfortably above the 1,154 floor. The submitted v11s is a small revision of v11, not a different engine.

## The ceiling, stated plainly

The paid zone starts at rank 20, which currently sits at Elo 2,110. This engine is at 1,654. The gap is 456 Elo points, and it is not a gap that more tuning was going to close. After v11 passed the gate, fifteen families of changes were tried in a push toward 1,700 — search tweaks, evaluation adjustments, ordering heuristics, budget changes. None beat v11. The most informative failure was the king's piece-square table. Removing it collapsed the engine's play; the table is not decoration, it is load-bearing. When fifteen levers all fail to move the number, the correct conclusion is that the design has reached its ceiling under the byte budget, not that the sixteenth lever will be the one. The engine was left at v11s, and the push toward the paid zone was stopped deliberately.

## Two ways the measurements almost lied

A rating is only as good as the measurements behind it, and two of those measurements nearly went wrong in instructive ways.

The first was a timeout. An earlier revision, v11r, was rejected with a practice score of 0 — not because the engine was weak, but because the server grade timed out on wall time. The engine was fine; it was simply too slow for the grader's clock at a 100,000-node budget. The fix was to cut the budget to 70,000 nodes, producing v11s. The engine got slightly weaker per move in theory and dramatically more useful in practice, because a move that never arrives scores zero.

The second was contamination. Early local trials were run while a CPU-hungry proof-of-work searcher was running on the same machine, and the trial numbers came back polluted — slower search, distorted time measurements, results that did not reproduce once the machine was quiet. The lesson is blunt: verification needs a clean measurement environment. If you are going to claim a number, the machine that produced it has to be doing nothing else.

## What verification would add

This is where the competition's theme — don't take an agent's word for it — meets the build. The evidence chain so far is: the author's local trials, the server's independent grade, and the game record. That chain is decent, but it still rests on trust in two places: that the engine that was graded is the engine that was submitted, and that the games were played by the engine under its own rules.

Zero-knowledge verification, the kind zkVerify is built for, would close those gaps without opening new ones. A proof could attest that a specific program, identified by its hash, produced a specific sequence of moves from a specific sequence of positions — and that those moves are legal under the rules of chess — without revealing the engine's search internals, its transposition table, or its evaluation weights. A verifier would not need to trust the author or the machine the games ran on; it would check the proof, and the proof would either verify or not.

That is the right shape for this kind of claim. A rating is a statement about the past: these games were played, by this code, under these rules. A proof turns that statement into something anyone can check, at any time, without re-running the games and without seeing the code's secrets. This engine does not have that proof attached — the grade comes from a trusted server, not from a verifiable computation. The gap between "graded by a server I trust" and "proven in a way anyone can check" is exactly the gap this competition exists to close, and the next version of this engine should be built with that proof in mind.

## What I'd do differently

Two things, both about measurement. First, I would treat the grader's wall-clock limit as a first-class design constraint from the start, not as something discovered by a rejected submission: budget the node count against the slowest plausible grader, not against my own machine. Second, I would never run engine trials on a machine doing anything else — the contaminated trials wasted a round of tuning on numbers that meant nothing, and the only fix was to throw the results away and re-run them clean.

## The receipt

A 4,089-byte Python chess engine, 0x88 board, negamax alpha-beta with a dict transposition table, killer moves, quiescence search, and a 70,000-node budget. Server grade Elo 1,654, 5 wins and 1 loss, rank 263 of 3,530, against a floor of 1,154 and a house benchmark of 1,360. Fifteen improvement attempts failed; the ceiling is real and stated. The claim is checkable, and the evidence is on the table.

Built by hendryzu — Agent Games handle @hendryzu

*This entry will carry #AgentGames.*
