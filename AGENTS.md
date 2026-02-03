# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## Language Preference

**Default language: Korean (한국어)**

- **Documentation** (docs/, plans/, README files): Write in Korean
- **Code comments**: Write in Korean for better team understanding
- **Commit messages**: Write in Korean
- **Code/variables/functions**: Use English (industry standard)
- **AGENTS.md itself**: Keep in English (shared community guideline)

When generating content, default to Korean unless the content type requires English (e.g., code identifiers).

## 1. Ask First, Code Later

**Use AskUserQuestion when anything is unclear. Assumptions are expensive.**

**When to ask (use AskUserQuestion tool):**
- Multiple valid approaches exist → Present options, don't pick silently
- Requirements are vague → Clarify before writing code
- User's intent is ambiguous → Ask what they actually want
- Scope is unclear → "Should I also handle X?" beats guessing
- Trade-offs exist → Surface them: "Fast vs. flexible?"
- Error details are missing → "What error did you see?" before debugging

**Red flags you're assuming too much:**
- "I'll just..." → Stop. Is this what they want?
- "Probably they mean..." → Ask instead
- "Let me try this approach..." → Why this one? Ask if unsure
- "I'll add X just in case..." → Do they need X? Ask

**Examples:**
```
❌ Bad: User says "it's not working" → Start debugging blind
✅ Good: Ask "What error message do you see?" or "What did you expect to happen?"

❌ Bad: User says "add validation" → Pick rules yourself
✅ Good: Ask "What should be validated? Email format? Length limits?"

❌ Bad: Multiple solutions possible → Pick one silently
✅ Good: Ask "Approach A is faster, B is more flexible. Which matters more?"
```

**Rule:** If you're about to make an assumption, use AskUserQuestion instead.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:**
- Clarifying questions (AskUserQuestion) come BEFORE implementation, not after
- Fewer unnecessary changes in diffs
- Fewer rewrites due to overcomplication or wrong assumptions
- User says "yes, that's what I meant" not "no, I meant..."
