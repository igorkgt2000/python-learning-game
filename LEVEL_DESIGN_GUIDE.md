# Level Design Guide - Python Learning Game

## 🎯 Learning Progression Overview

This document outlines the complete learning progression from beginner (Level 1) to expert (Level 30+).

### Philosophy
- **Progressive Difficulty**: Each level introduces ONE new concept
- **Build on Previous**: Concepts compound (loops use basic movement, functions use loops, etc.)
- **Clear Objectives**: Each level has a specific learning goal
- **Helpful Hints**: Every level provides guidance without giving away the solution
- **Multiple Solutions**: Most levels can be solved in different ways (encourage creativity)

---

## 📚 Level Progression (30 Levels)

### **PHASE 1: FUNDAMENTALS (Levels 1-5)**
**Concepts:** Basic movement, sequencing, turning

| Level | Concept | Description |
|-------|---------|-------------|
| 1 | Sequential commands | Straight line to goal |
| 2 | Turning | L-shaped path |
| 3 | Multiple turns | Zigzag path |
| 4 | Gem collection | Pick up gems on the way |
| 5 | Planning | More complex path |

---

### **PHASE 2: LOOPS (Levels 6-10)**
**Concepts:** For loops, range(), repetition

| Level | Concept | Description |
|-------|---------|-------------|
| 6 | For loop intro | Repeat move_forward() 5 times |
| 7 | Range calculations | Use range(n) dynamically |
| 8 | Nested movements | Move and turn in pattern |
| 9 | Spiral path | Create spiral using loop |
| 10 | Rectangle challenge | Draw rectangle with loops |

---

### **PHASE 3: CONDITIONALS (Levels 11-15)**
**Concepts:** If/else, boolean logic, sensing

| Level | Concept | Description |
|-------|---------|-------------|
| 11 | If statements | Check is_clear() before moving |
| 12 | Simple maze | Fork in the road |
| 13 | Conditional gems | Only collect certain gems |
| 14 | Elif chains | Multiple path choices |
| 15 | Complex maze | Full maze navigation |

---

### **PHASE 4: WHILE LOOPS (Levels 16-20)**
**Concepts:** While loops, unknown iterations, conditions

| Level | Concept | Description |
|-------|---------|-------------|
| 16 | While loop intro | Move until wall |
| 17 | Unknown distance | Navigate corridor of unknown length |
| 18 | While + gems | Collect all gems (unknown count) |
| 19 | Combined loops | Use both for and while |
| 20 | While + conditionals | Complex navigation |

---

### **PHASE 5: FUNCTIONS (Levels 21-25)**
**Concepts:** Function definitions, parameters, reusability

| Level | Concept | Description |
|-------|---------|-------------|
| 21 | Function definition | Create turn_right() function |
| 22 | Reusable patterns | Function for repeated pattern |
| 23 | Parameters | Function with distance parameter |
| 24 | Multiple functions | Several helper functions |
| 25 | Recursion intro | Simple recursive function |

---

### **PHASE 6: ADVANCED CONCEPTS (Levels 26-30)**
**Concepts:** Lists, nested loops, algorithms

| Level | Concept | Description |
|-------|---------|-------------|
| 26 | Lists | Use list to store positions |
| 27 | List iteration | Iterate through waypoints |
| 28 | Nested loops | Double for loop grid pattern |
| 29 | Algorithms | Implement search algorithm |
| 30 | Final challenge | Complex multi-concept level |

---

## 🎨 Level Design Best Practices

### Grid Size Recommendations
- **Beginner (1-5)**: 8x8 to 10x10 (small, easy to visualize)
- **Intermediate (6-20)**: 10x10 to 15x15 (more room for complexity)
- **Advanced (21-30)**: 12x12 to 20x20 (challenging puzzles)

### Gem Placement
- **Tutorial levels**: 0-2 gems (focus on movement)
- **Practice levels**: 3-5 gems (practice concept)
- **Challenge levels**: 5-10 gems (test mastery)

### Hint Writing
- **Never give solution**: Guide thinking, don't give code
- **Suggest concept**: "Try using a for loop" not "Use for i in range(5)"
- **Ask questions**: "How many times do you need to repeat this?"
- **Progressive hints**: If stuck, hint system can reveal more

### Difficulty Curve
```
Easy   ████░░░░░░░░░░░░░░░░  (Levels 1-5)
       ░░░░████░░░░░░░░░░░░  (Levels 6-10)
Medium ░░░░░░░░████░░░░░░░░  (Levels 11-15)
       ░░░░░░░░░░░░████░░░░  (Levels 16-20)
Hard   ░░░░░░░░░░░░░░░░████  (Levels 21-25)
Expert ░░░░░░░░░░░░░░░░░░░░  (Levels 26-30)
```

---

## 📝 Level JSON Format

```json
{
  "name": "Level Name",
  "description": "What the level teaches",
  "grid_size": [10, 10],
  "start_pos": [0, 0],
  "goal_pos": [9, 9],
  "obstacles": [[2, 2], [3, 3]],
  "gems": [[5, 5], [6, 6]],
  "hint": "Helpful guidance without giving away solution",
  "learning_objective": "What concept this level teaches",
  "difficulty": "beginner|intermediate|advanced|expert",
  "estimated_lines": 5
}
```

---

## ✅ Level Testing Checklist

For each level:
- [ ] Has clear learning objective
- [ ] Is solvable with taught concepts only
- [ ] Has multiple solution paths (if possible)
- [ ] Hint is helpful but not solution-giving
- [ ] Grid is visually clear and uncluttered
- [ ] Difficulty is appropriate for its position
- [ ] Estimated lines of code is accurate
- [ ] Has been play-tested

---

## 🚀 Implementation Status

- ✅ Levels 1-5: COMPLETE (Basic movement)
- 🔄 Levels 6-10: IN PROGRESS (Loops)
- ⏳ Levels 11-15: TODO (Conditionals)
- ⏳ Levels 16-20: TODO (While loops)
- ⏳ Levels 21-25: TODO (Functions)
- ⏳ Levels 26-30: TODO (Advanced)

---

*This is a living document. Update as levels are created and tested.*

