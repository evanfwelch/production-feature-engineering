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

<p class="fragment">
Quick luigi demo
</p>

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
WHERE t.trxn_dt between ('2017-12-01', '2017-12-10')
```
<p class="fragment">
but then one day passes...
<\p>

---
<!-- .slide: style="text-align: left;"> -->  
## Strategy: Chunk your "queries" wisely

- isolate your API calls |
- think about history... |
- and the history of history... |

---
## Separate data from code

### and separate code into
* filter
* map
* aggregate

---
## Distributed processing on small data

### Why?
* can easily scale when you have more data (add more workers)
* deal with edge cases
* force yourself to not see whole picture up front

---


---?code=reference/swagger.json&lang=json&title=Capital One Hackathon API


@[1,3-6](Present code found within any repo source file.)
@[8-18](Without ever leaving your slideshow.)
@[19-28](Using GitPitch code-presenting with (optional) annotations.)

---

@title[JavaScript Block]

<p><span class="slide-title">JavaScript Block</span></p>

```javascript
// Include http module.
var http = require("http");

// Create the server. Function passed as parameter
// is called on every request made.
http.createServer(function (request, response) {
  // Attach listener on end event.  This event is
  // called when client sent, awaiting response.
  request.on("end", function () {
    // Write headers to the response.
    // HTTP 200 status, Content-Type text/plain.
    response.writeHead(200, {
      'Content-Type': 'text/plain'
    });
    // Send data and end response.
    response.end('Hello HTTP!');
  });

// Listen on the 8080 port.
}).listen(8080);
```

@[1,2](You can present code inlined within your slide markdown too.)
@[9-17](Displayed using code-syntax highlighting just like your IDE.)
@[19-20](Again, all of this without ever leaving your slideshow.)

---?gist=onetapbeyond/494e0fecaf0d6a2aa2acadfb8eb9d6e8&lang=scala&title=Scala GIST

@[23](You can even present code found within any GitHub GIST.)
@[41-53](GIST source code is beautifully rendered on any slide.)
@[57-62](And code-presenting works seamlessly for GIST too, both online and offline.)

---

## Template Help

- [Code Presenting](https://github.com/gitpitch/gitpitch/wiki/Code-Presenting)
  + [Repo Source](https://github.com/gitpitch/gitpitch/wiki/Code-Delimiter-Slides), [Static Blocks](https://github.com/gitpitch/gitpitch/wiki/Code-Slides), [GIST](https://github.com/gitpitch/gitpitch/wiki/GIST-Slides)
- [Custom CSS Styling](https://github.com/gitpitch/gitpitch/wiki/Slideshow-Custom-CSS)
- [Slideshow Background Image](https://github.com/gitpitch/gitpitch/wiki/Background-Setting)
- [Slide-specific Background Images](https://github.com/gitpitch/gitpitch/wiki/Image-Slides#background)
- [Custom Logo](https://github.com/gitpitch/gitpitch/wiki/Logo-Setting) [TOC](https://github.com/gitpitch/gitpitch/wiki/Table-of-Contents) [Footnotes](https://github.com/gitpitch/gitpitch/wiki/Footnote-Setting)

---

## Go GitPitch Pro!

<br>
<div class="left">
    <i class="fa fa-user-secret fa-5x" aria-hidden="true"> </i><br>
    <a href="https://gitpitch.com/pro-features" class="pro-link">
    More details here.</a>
</div>
<div class="right">
    <ul>
        <li>Private Repos</li>
        <li>Private URLs</li>
        <li>Password-Protection</li>
        <li>Image Opacity</li>
        <li>SVG Image Support</li>
    </ul>
</div>

---

### Questions?

<br>

@fa[twitter gp-contact](@gitpitch)

@fa[github gp-contact](gitpitch)

@fa[medium gp-contact](@gitpitch)

---?image=assets/image/gitpitch-audience.jpg&opacity=100

@title[Download this Template!]

### <span class="white">Get your presentation started!</span>
### [Download this template @fa[external-link gp-download]](https://gitpitch.com/template/download/white)
