# Predicting NHL Player Salary
Analysis by Charles Ramey for General Assembly Data Science Immersive Course - Capstone Project

---

### Problem Statement

In the National Hockey League (NHL), team executives lack a robust, data-driven solution to estimate player salaries, which hinder's their ability to perform effective roster building and financial planning. This stems from the inherent complexity of factors that drive player salaries, including their performance, the quality of the team's they have played for, and the value of contracts signed by similar players. This project seeks to design a data-driven approach that can leverage historical data and advanced modeling techniques to help NHL executives balance their budgets, invest in their rosters, and remain competitive within the league.

---

### Summary

Data was collected from various websites including [CapFriendly](https://www.capfriendly.com/), [MoneyPuck](https://moneypuck.com/), and [Hockey Reference](https://www.hockey-reference.com/). The data was scraped using Selenium WebDriver version 4.8.2 with the Google Chrome WebDriver manager. Historical contract signings dating from the conclusion of the 2010-11 season through the end of 2022 were scraped from CapFriendly, along with salary cap limits and active contracts through present day. Player stats, including stats for forwards, defensemen, and goalies were collected from MoneyPuck from the 2010-11 season through the 2022-23 season. Historical team standings were scraped from Hockey-Reference from the 2010-11 season through the 2022-23 season.

The vast majority of contracts signed are at or near the minimum salary, with fewer players earning higher-paying contracts. Team standing generally appears to have little impact on skater salaries, but a more noticeable impact on goalie salaries. Offensive stats like points are correlated to contract values for both forwards and defensemen, confirming that defensemen are a valuable asset in the NHL. Additionally, while contracts for skaters have generally increased as the NHL's salary cap limit has increase, salaries for goalies have remained relatively steady.

Models were trained separately for forwards, defense, and goalies based on the assumption that different stats drive contract value for each position. Several models were tested for each dataset, including linear regression, various tree methods, and ensemble models. For each dataset, the linear regression model performed the best, though performance was not spectacular, scoring a 0.80 on the training data and a 0.78 on the test data for forwards, but decreasing to 0.65 and 0.45 respectively for goalies.

This project also contains a [streamlit web application](https://nhl-salary-predictor.onrender.com/) that implements the models trained for each position to predict player value for the upcoming 2023-24 season based on their performance in the 2022-23 season. The app is still in development and not yet optimized.

---

### Conclusion and Recommendations

This project was designed to create a simple tool for predicting NHL player salary, an inherently complex and often intangible process. I was able to create such a tool, however, the complexity of the challenge combined with the fact that there are realistically only a couple thousand player signings in the last decade creates a significant obstalce to achieving a highly accurate salary prediction tool. The pitfalls are amplified for goalies, for whom there is even less data. Even if steps are taken to minimize the amount of data points that are removed (for example, choosing to include 2-way contracts, or expanding the analysis further back than 2010), the number of signings is still limited. Another major pitfall of this project is that the target variable is inherently time-dependent (salaries generally increase with time), yet the salary of an indivual player cannot be predicted using a time-series analysis due to the inherent independence of a single player's stats and salary. 

There are many avenues to continue to explore with this data, and additional steps can be taken outside of the time contraints of the General Assembly capstone project to further improve model performance and the user experience with the web application. Some recommendations and planned next steps include:
- Exploring the bimodality of the logarithmically transformed contract data.
- Training on the combined forwards and defense datasets.
    - These were originally trained separetly under the assumption that the different play style of forwards and defensemen would require unique models for each. Keeping this data combined allows the model to learn from more data and may improve model performance.
- Adjusting the data to a per-game basis.
    - For this iteration, data was left as is. A potential issue with this is that a player who played 60 games is likely to have relatively lower stats than if they played a full 82 games. The model does not account for partial seasons which may be a major hindrance to performance.
- Testing a wider variety of model hyperparameters
    - A more thorough grid search of hyperparameters for the various models may reveal more optimal parameters that improve model performance.
    
Overall, I learned a lot through this project, particularly about webscraping with Selenium, but also about experimental design. I believe there are multiple considerations I could have made early on in this project that could have improved the outcome, and I am looking forward to applying these lessons learned on my next project.

---

### Sources

1. [https://www.sportingnews.com/us/nhl/news/nhl-salary-cap-rules-explained/x1wwiew656afzelhsx4tnecz](https://www.sportingnews.com/us/nhl/news/nhl-salary-cap-rules-explained/x1wwiew656afzelhsx4tnecz)
2. [https://www.capfriendly.com/players/nazem-kadri](https://www.capfriendly.com/players/nazem-kadri)
3. [https://www.nhl.com/player/nazem-kadri-8475172](https://www.nhl.com/player/nazem-kadri-8475172)
4. [https://www.nhl.com/news/nazem-kadri-signs-seven-year-contract-with-flames/c-335317582](https://www.nhl.com/news/nazem-kadri-signs-seven-year-contract-with-flames/c-335317582)
5. [https://www.capfriendly.com/](https://www.capfriendly.com/)
6. [https://moneypuck.com/](https://moneypuck.com/)
7. [https://www.hockey-reference.com/](https://www.hockey-reference.com/)
8. [https://selenium-python.readthedocs.io/index.html](https://selenium-python.readthedocs.io/index.html)
9. [https://pandas.pydata.org/docs/index.html](https://pandas.pydata.org/docs/index.html)
10. [https://en.wikipedia.org/wiki/List_of_NHL_seasons](https://en.wikipedia.org/wiki/List_of_NHL_seasons)
11. [https://chat.openai.com/](https://chat.openai.com/)
12. [https://matplotlib.org/stable/api/index.html](https://matplotlib.org/stable/api/index.html)
13. [https://scikit-learn.org/stable/modules/classes.html](https://scikit-learn.org/stable/modules/classes.html)