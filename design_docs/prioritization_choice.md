# Prioritization Framework Recommendation

**Based on your context:**
- **Product Stage:** Early PMF, scaling – you have found initial product‑market fit and are growing fast.
- **Team Context:** Small team (solo developer / few collaborators) – need a simple yet data‑driven method.
- **Decision‑Making Need:** Too many ideas, unclear which to pursue – you need a systematic way to filter backlog.
- **Data Availability:** Some data – basic analytics and customer feedback exist, but not extensive usage metrics.

---

## Recommended Framework: **RICE** (Reach, Impact, Confidence, Effort)

**Why this framework fits:**
1. **Matches stage:** Early‑PMF teams benefit from a balanced view of reach and impact to prioritize features that drive adoption.
2. **Fits team size:** RICE scoring can be done quickly in a spreadsheet; it doesn’t require heavy tooling.
3. **Addresses need:** Provides a clear filter for many ideas, turning a long backlog into a ranked list.
4. **Leverages available data:** You have enough analytics to estimate Reach and Impact, and confidence can be expressed as a percentage.

**When to use it:**
- Quarterly or sprint‑planning sessions when the backlog exceeds 20‑30 items.
- When you want a transparent, quantifiable ranking to share with stakeholders.

**When NOT to use it:**
- If you had **minimal data** (pre‑product) – ICE or Value/Effort would be lighter.
- For **strategic, multi‑quarter bets** where reach isn’t the primary concern – consider Opportunity Scoring or Kano.

---

## How to Implement RICE

### Step 1: Define Scoring Criteria
- **Reach:** Estimate the number of users the feature will affect per month/quarter.
- **Impact:** Rate the expected benefit (1 = minimal, 2 = high, 3 = massive).
- **Confidence:** Express confidence in your Reach/Impact estimates as a % (50 % = low data, 80 % = good data).
- **Effort:** Estimate person‑months (include design, engineering, QA).

### Step 2: Score Each Feature
- Create a shared spreadsheet (Google Sheets, Airtable, or CSV).
- Involve the small team (you and any collaborators) to assign each metric.

### Step 3: Calculate RICE Score
```
RICE = (Reach × Impact × Confidence) / Effort
```
- Higher scores = higher priority.

### Step 4: Review & Adjust
- Sort by score, discuss the top 5‑10 items with any stakeholders (e.g., a mentor or a future teammate).
- Adjust for strategic considerations that RICE doesn’t capture (e.g., “this feature is a required dependency”).

---

## Example Scoring Template

| Feature | Reach (users/quarter) | Impact (1‑3) | Confidence (%) | Effort (person‑months) | RICE Score |
|---------|----------------------|--------------|----------------|------------------------|------------|
| Core ports & adapters | 8,000 | 3 | 80% | 2 | 96,000 |
| System 1 agent skeleton | 5,000 | 2 | 70% | 1.5 | 46,667 |
| Rule engine prototype | 4,000 | 2 | 60% | 1 | 48,000 |
| Recursion support | 3,000 | 3 | 50% | 2 | 22,500 |
| Demo script & docs | 2,000 | 1 | 90% | 0.5 | 36,000 |

**Priority order (high → low):** Core ports & adapters → Rule engine → Demo script → System 1 skeleton → Recursion support.

---

## Alternative Framework (if RICE feels too heavy)

**ICE** (Impact, Confidence, Ease) – removes Reach, making scoring faster when you lack usage numbers.

**Why it might work:**
- Simpler 3‑column scoring, quicker to complete.
- Still gives a relative ranking.

**Trade‑offs:**
- No visibility into how many users benefit.
- May over‑prioritize high‑impact but low‑reach items.

---

## Common Pitfalls & How to Avoid Them

1. **Over‑weighting Effort** – Don’t drop high‑impact items just because they need more work; consider strategic importance.
2. **Inflating Confidence** – Be honest; a 90 % confidence score when you have no data misleads the ranking.
3. **Ignoring Strategy** – RICE is a tool, not a decision; adjust the list for product vision or roadmap themes.

---

## Reassess When

- Your product moves from **early‑PMF** to **mature** – you may shift to **Opportunity Scoring** or **Kano**.
- Your team grows beyond a handful of people – you might adopt a more formal scoring workshop.
- Data collection improves – you can add a more precise Reach metric.

---

**Next step:** Run the RICE scoring session with the items listed in `epic_hypotheses.md` and record the scores in a spreadsheet. Use the resulting order to prioritize the implementation phases in the roadmap.
