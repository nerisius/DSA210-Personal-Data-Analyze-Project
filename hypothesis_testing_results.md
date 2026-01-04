# Hypothesis Testing Results

## Dataset Overview
- Total movies: 512  
- Favorite movies: 69  

---

## H1 — Genre Preferences and Favorite Movies

**Hypothesis**

- **H₀ (Null):** My liked movies are evenly distributed across genres; there is no significant relationship between genre and whether I like a movie.
- **H₁ (Alternative):** My liked movies tend to concentrate in specific genres or genre combinations rather than being evenly distributed across all genres.
**Method**
- Chi-square test of independence
- Significance level: α = 0.05

**Results**

| Genre | χ² statistic | p-value | Conclusion |
|------|-------------|--------|-----------|
| Comedy | 5.70 | 0.017 | **Reject H₀** |
| Science Fiction | 3.26 | 0.071 | Fail to reject H₀ |
| Drama | 3.00 | 0.083 | Fail to reject H₀ |
| Action | 2.73 | 0.099 | Fail to reject H₀ |
| Romance | 2.37 | 0.124 | Fail to reject H₀ |
| Other genres | < 2 | > 0.20 | Fail to reject H₀ |

**Interpretation**

Only the **Comedy** genre shows a statistically significant association with favorite status.  
For all other genres, there is insufficient evidence to conclude a relationship with user preferences.

---

## H2 — Bias Toward Specific Actors and Directors

### Hypothesis
- **H2₀ (Null Hypothesis):**  
  The movies I choose to watch do not show any bias toward specific actors or directors.

- **H2₁ (Alternative Hypothesis):**  
  I am more likely to choose movies that feature actors or directors I already know or like.

---

### Method
To test for actor and director bias, a **chi-square goodness-of-fit test** was conducted on the **top 3 most frequently appearing actors** in the favorite movies.

- **Observed frequencies:**  
  The number of times each of the top 3 actors appears in favorite movies.

- **Expected frequencies:**  
  A **uniform distribution**, assuming no preference among actors (each actor is equally likely).

This test evaluates whether favorite movies disproportionately feature specific actors beyond what would be expected by chance.

---

### Results

**Top 3 Cast Bias Test (Uniform Expected Distribution)**

- Chi-square statistic: **290.92**
- p-value: **0.0385**
- Significance level: **α = 0.05**

---

### Decision
Since the p-value (**0.0385**) is **less than the significance level (α = 0.05)**, the null hypothesis is **rejected**.

---

### Interpretation
The results provide **statistically significant evidence** that watched movies are not evenly distributed across actors. Instead, there is a clear **bias toward specific actors**, indicating that familiarity or personal preference influences movie selection.

This result supports the alternative hypothesis and suggests that **cast-based preferences play an important role** in determining which movies are watched.

---

## H3 — Preference for High-Rated Movies

### H3a — IMDb Ratings

**Hypothesis**

- **H₀:** Mean IMDb rating of watched movies ≤ 7.0  
- **H₁:** Mean IMDb rating of watched movies > 7.0  

**Method**
- One-sample t-test
- Threshold: IMDb = 7.0
- Significance level: α = 0.05

**Results**
- t-stat: 23.5787
- p-value: 6.1876

**Conclusion**
The null hypothesis is **rejected**, indicating that the average IMDb rating of watched movies is significantly higher than 6.5.

---

### H3b — Rotten Tomatoes Ratings

**Hypothesis**

- **H₀:** Mean Rotten Tomatoes score ≤ 70  
- **H₁:** Mean Rotten Tomatoes score > 70  

**Method**
- One-sample t-test
- Threshold: RT = 70%
- Significance level: α = 0.05

**Results**
- t-stat: 16.9950
- p-value: 1.0083

**Conclusion**
The null hypothesis is **rejected**, suggesting a strong preference for critically well-reviewed movies.

---

## Overall Interpretation

The hypothesis tests indicate that my movie-watching behavior is strongly **score-driven**: I tend to watch movies with higher IMDb and Rotten Tomatoes ratings, supporting the idea that critical scores influence the decision to watch a movie.

After watching a movie, **genre generally does not determine whether it becomes a favorite**, with one notable exception. The genre-based chi-square analysis shows a **statistically significant concentration of favorite movies in the Comedy genre**, suggesting that comedies are more likely to be added to my favorites list than other genres.

For all remaining genres, the null hypothesis of an even distribution cannot be rejected, indicating no strong preference once the movie has already been watched.

In contrast, the results for H2 reveal a **significant bias toward specific actors and directors**, implying that familiarity and personal affinity toward certain cast or crew members influence both movie selection and post-watch preference.

Overall, my favorites are shaped by a combination of **high critical scores, a selective genre preference (Comedy), and personal actor/director biases**, which helps explain why machine learning models struggle to generalize these preferences accurately.

