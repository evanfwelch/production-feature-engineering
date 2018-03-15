## Feature Engineering for Prod

#### Evan Welch

---
<!-- .slide: style="text-align: left;"> -->  
## About me

<br>

@fa[github gp-tip](github.com/evanfwelch)
@fa[linkedin-square gp-tip](linkedin.com/in/evanfwelch)
@fa[instagram gp-tip](evanfwelch)
@fa[envelope gp-tip](evanfwelch@gmail.com)

<p class="fragment">
Get in touch!
</p>

Note: Majored in physics, lots of time in quantitative finance, got into ML, data science, wanted to affect customers
---
<!-- .slide: style="text-align: left;"> -->  
## Case Study Scenario

<ul style="list-style: none;">
<li class="fragment">@fa[bank](C1 is a bank ...)</li>
<li class="fragment">@fa[users](with millions of customers...)</li>
<li class="fragment">@fa[credit-card](each of whom has several cards...)</li>
<li class="fragment">@fa[shopping-cart](on which they make purchases...)</li>
<li class="fragment">@fa[building](at several different stores)</li>
<li class="fragment">@fa[utensils](...which belong to several categories:) @fa[car] @fa[coffee] @fa[utensils]</li>
</ul>

<p class="fragment">
@fa[database](http://api.reimaginebanking.com/)
</p>

---
<!-- .slide: style="text-align: left;"> -->  
## Possible Analytical Questions
- Do the customers fall into different spending cohorts? |
- Is spending predictive of other behaviors? |
- Do abrupt changes in spending indicate a life event? |


---
<!-- .slide: style="text-align: left;"> -->  
## To answer any of these

We'll need to:
- pull some data |
- transform data into features  |
- analyze/visualize/model something |

<p class="fragment">
*This talk focuses on feature engineering...*
</p>

<p class="fragment">
*but doing so at scale, without mistakes, for production*
</p>

---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:

- Using a task scheduler |
- Building a Fake Data Ecosystem |
- Chunking your "queries" wisely |
- Separating data and code |
- Using "Big Data" tools on small data |

<p class="fragment">
*Please interrupt at any time!*
</p>

---
<!-- .slide: style="text-align: left;"> -->  
## What's wrong with this picture?

```bash
cd my/project/folder

# get data
./download_lots_of_data.sh > data.json
echo "Done getting account, customer and merchant data"

# mine transactions for features
python generate_a_bunch_of_features.py
echo "Done mining transaction"

# run a jupyter notebook
jupyter nbconvert --to script my_machine_learning_model.ipynb
python my_machine_learning_model.py
```

---
<!-- .slide: style="text-align: left;"> -->  
## Strategy: use a task scheduler
- Airflow (by Airbnb) |
- GNU make |
- Celery |
- Luigi (by Spotify) |

<p class="fragment">
Let's look at luigi
</p>

---?code=pull_raw_data.py&lang=python&title=using luigi to schedule tasks
@[21-44](A simple luigi.Task that calls an API)
@[201-213](A more complex task that outer joins and flattens the data)

---
<!-- .slide: style="text-align: left;"> -->  
## Quick luigi demo...


---
<!-- .slide: style="text-align: left;"> -->  
## What do you do if:
- you're modeling a product that is in development |
- you're worried about outliers |
- your customers might have duplicate accounts |
- you need to prove your code works... |
- but the engineers don't have your data privileges |

---
<!-- .slide: style="text-align: left;"> -->  
## Strategy: build a fake data playground
- to anticipate changes |
- for unit testing |
- to model edge cases ... |
- and typical cases ... |
- and "happy path" cases ... |

<p class="fragment">
`python fake_data_generator.py`
</p>

---?code=generate_fake_data.py&lang=python&title=Fake Data Generator

@[228-248](This script deletes and re-generates the fake data)
@[9-11,26-39](Faker can easily generate fake business fields)
@[151-225](Randomly generate transaction data)
@[41-63](Clean up after yourself)

<p class="fragment">
*All the data we just queried was actually fake data*
</p>

---
<!-- .slide: style="text-align: left;"> -->  
## What do you do if:
- your model needs 6 months of transaction data... |
- joined against merchant details... |
- and customer profile info  ... |
- everything is working great (high AUC fist-pump) ... |

---
```sql
SELECT *
FROM transactions t
INNER JOIN accounts a
ON t.payer_id = a._id
INNER JOIN merchants m
ON t.merchant_id = m._id
...
WHERE t.trxn_dt between ('2017-06-01', '2017-12-31')
```
<p class="fragment">
but then one day passes...
</p>

---
<!-- .slide: style="text-align: left;"> -->  
## Strategy: Chunk your "queries" wisely

- isolate your API calls |
- think about history... |
- and the history of history... |
- user parameter injection |
- think about the velocity of the data |

---
```python
import sqlite3
conn = sqlite3.connect('my.db')
c = conn.cursor()

my_query = """
SELECT *
FROM transactions t
INNER JOIN accounts a
ON t.payer_id = a._id
INNER JOIN merchants m
ON t.merchant_id = m._id
...
WHERE t.trxn_dt between ({min_date}, {max_date})"""

...
for min_date, max_date in my_date_ranges:
  c.execute(my_query.format(
    min_date=min_date,
    max_date=max_date))
```

---?code=pull_raw_data.py&lang=python&title=Isolated requirements for ETL
@[205-213](Depending on isolated queries)

---
<!-- .slide: style="text-align: left;"> -->  
## How do we productionize this?
```python
import pandas as pd

total_spend = (pd.read_csv('some_data.csv')
                .dropna()
                .groupby('customer_id')
                .trxn_amt
                .sum())
```

---
<!-- .slide: style="text-align: left;"> -->  
## Separate *data* from *code*

#### and separate code into:
- filter |
- map |
- aggregate |

---
## Distributed processing on small data

### Why?
* can easily scale when you have more data (add more workers)
* deal with edge cases
* force yourself to not see whole picture up front
