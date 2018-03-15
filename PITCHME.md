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

Note: When all of you join companies/interview, zoom out and get big picture data view


---
<!-- .slide: style="text-align: left;"> -->  

## Possible Analytical Questions
- Do the customers fall into different spending cohorts? |
- Is spending predictive of other behaviors? |
- Do abrupt changes in spending indicate a life event? |

Note: In Seattle we work on digital products to improve customer financial health, here are some potential questions
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

Note: Whether it's a dashboard, a simple KPI, or an ML model, you're analytical plan will share some basic steps
---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:


- Using a task scheduler |
- Building a Fake Data Ecosystem |
- Chunking your "queries" wisely |
- Separating data from operations |
- Using "Big Data" tools on small data |

<p class="fragment">
*Please interrupt at any time!*
</p>

Note: Feature engineering--lots of great ideas online, on kaggle, in scikit-learn docs on *what* to engineer. We'll focus on some best practices for how to execute that plan and get it into prod. Prepare to never be done.
---
<!-- .slide: style="text-align: left;"> -->  
## What's wrong with this picture?


```bash
cd my/project/folder

# get all raw data bank from the APIs
./download_lots_of_data.sh > data.json
# Contents of this file ^^^
# curl -X GET https://api.reimaginebanking.com/customers?key=$API_KEY > customers.json
# curl -X GET https://api.reimaginebanking.com/merchants?key=$API_KEY > merchants.json
# curl -X GET https://api.reimaginebanking.com/accounts?key=$API_KEY > accounts.json
# curl -X GET https://api.reimaginebanking.com/purchases?key=$API_KEY > transactions.json
echo "Done getting account, customer and merchant data"

# mine transactions for features
python generate_a_bunch_of_features.py
echo "Done mining transaction"

# run a jupyter notebook
jupyter nbconvert --to script my_machine_learning_model.ipynb
python my_machine_learning_model.py
```

Note: all data in one pull, what if dates change..., what if data gets deleted... python script might succeed on incomplete data... what if there's a mistake in the notebook? what packages do i need to run the notebook? can i send this to a colleague?
---
<!-- .slide: style="text-align: left;"> -->  
## Strategy: use a task scheduler

- GNU make |
- Celery |
- Airflow (by Airbnb) |
- Luigi (by Spotify) |

<p class="fragment">
Let's look at luigi
</p>

Note: obviously projects evolve organically, and the above is ok for many cases, but anything you MIGHT want to re-run or get feedback on, I highly suggest using a task scheduler to build a pipeline
---
<!-- .slide: style="text-align: left;"> -->  
## Quick luigi demo...


Note: show live demo first

---?code=pull_raw_data.py&lang=python&title=using luigi to schedule tasks
@[21-44](A simple luigi.Task that calls an API)
@[205-219](A more complex task that outer joins and flattens the data)

Note: so the goal is to get transactions, joined up with customers and merchant info... no feature engineering YET
---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:
* ~~Using a task scheduler~~
* Building a Fake Data Ecosystem
* Chunking your "queries" wisely
* Separating data from operations
* Using "Big Data" tools on small data

---
<!-- .slide: style="text-align: left;"> -->  
## What do you do if:

- you're modeling on a product that is still under development |
- you're worried about outliers |
- the "real data" is quite small |
- customers have multiple accounts or devices |
- you need to prove your code works... |
- but the engineers don't have your data privileges |

Note: Ok so we just went through how to pull data in an organized, modular way, but what do you do if
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

Note: sometimes for a project we want the ability to generate a whole bunch of fake, extreme or ultra-realistic values

---?code=generate_fake_data.py&lang=python&title=Fake Data Generator

@[228-248](This script deletes and re-generates the fake data)
@[9-11,26-39](Faker can easily generate fake business fields)
@[151-225](Randomly generate transaction data)
@[41-63](Clean up after yourself)

<p class="fragment">
*All the data we just queried was actually fake data*
</p>

Note: For this talk i wrote a module that populates the hackathon API with fake data
---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:
* ~~Using a task scheduler~~
* ~~Building a Fake Data Ecosystem~~
* Chunking your "queries" wisely
* Separating data from operations
* Using "Big Data" tools on small data

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

Note: what's wrong here? this query has everything joined to everything, hard coded dates
---
<!-- .slide: style="text-align: left;"> -->  
## Strategy: Chunk your "queries" wisely
- isolate your API calls |
- think about history... |
- and the history of history... |
- use parameter injection |
- think about the velocity of the data |

Note: there are some considerations to querying more repeatable... whether api or SQL
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

Note: consider running your queries within python... param subbing... version on GH... credentials...

---?code=pull_raw_data.py&lang=python&title=Isolated requirements for ETL
@[209-214](Depending on isolated queries)

---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:
* ~~Using a task scheduler~~
* ~~Building a Fake Data Ecosystem~~
* ~~Chunking your "queries" wisely~~
* Separating data from operations
* Using "Big Data" tools on small data

---
<!-- .slide: style="text-align: left;"> -->  

## Ok, so say we want to make some features....
- total, average, and count ...
- of credit card transactions...
- per `customer_id` (not just `account_id`)
- in several categories: `food`, `bar`, `gas`, ...
- for particular time windows ...

Note: so let's say for our project we want to make a whole bunch of transaction features

---
<!-- .slide: style="text-align: left;"> -->  
## Here's the pandas way...

```python
import pandas as pd

df = pd.read_csv('some_data.csv')

total_spend = (df.loc[df.trxn_dt == '2017-12-01', :]
                .dropna()
                .groupby('customer_id')
                .trxn_amt
                .sum())
```
<p class="fragment">
But how do we productionize this?
</p>

Note: here's a pandasy simple "feature", what are some things wrong here? date, dropna vulnerable to more columns, trxn_amt hardcoded, sum not easily swappable

---
<!-- .slide: style="text-align: left;"> -->  
## Separate *data* from *operations*

#### and separate code into:
- filtering functions |
- cleaning/replacing/imputing data |
- mapping new columns |
- aggregate/reduce functions |


<p class="fragment">
Let's look at an example from `exploration.ipynb`
</p>

Note: data can be big or small, training or test, and transformations can be chained together... re-used, imported.. analyzed... unit tested


---?code=exploration.py&lang=python&title=feature engineering code

---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:
* ~~Using a task scheduler~~
* ~~Building a Fake Data Ecosystem~~
* ~~Chunking your "queries" wisely~~
* ~~Separating data from operations~~
* Using "Big Data" tools on small data

---
<!-- .slide: style="text-align: left;"> -->  

## What do you do if:
- Your model is working on 500MB of data... |
- on your laptop... |
- You get a MemoryError ... |
- and you need to run this in the cloud... |

Note: Ok so lets say you've followed all the advice. using a task scheduler, fake data, very modular queries, nicely written transformations... but you want to SCALE
---
<!-- .slide: style="text-align: left;"> -->  


## Use distributed processing before you *need* it
- to scale from 100 rows to 100GB |
- to avoid rewriting your code |
- even to "look-ahead" bias |

<p class="fragment">
Back to `exploration.py` to use dask.
</p>

Note: anyone used distributed processing? spark? hadoop? Dask? Let's take a look.

---?code=exploration.py&lang=python&title=using dask to distribute feature engineering
@[5-6](dask and dask/distributed library)
@[119](set up a local connection to scheduler)
@[122-123](can basically treat it like Pandas)

---
<!-- .slide: style="text-align: left;"> -->

## Demo of `dask.distributed`

---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:
* ~~Using a task scheduler~~
* ~~Building a Fake Data Ecosystem~~
* ~~Chunking your "queries" wisely~~
* ~~Separating data from operations~~
* ~~Using "Big Data" tools on small data~~

Note: run exploration.py with dask distributed... set up workers and go to interface first
---
<!-- .slide: style="text-align: left;"> -->
## Ask me anything!

---
<!-- .slide: style="text-align: left;"> -->  
## Reach out!

@fa[github gp-tip](github.com/evanfwelch/production-feature-engineering)
@fa[linkedin-square gp-tip](linkedin.com/in/evanfwelch)
@fa[envelope gp-tip](evanfwelch@gmail.com)
@fa[instagram gp-tip](evanfwelch)
