## Feature Engineering for Prod

#### Evan Welch

---

## About me

<br>

<!-- .slide: style="text-align: left;"> -->  
@fa[github gp-tip](github.com/evanfwelch)
@fa[linkedin-square gp-tip](linkedin.com/in/evanfwelch)
@fa[instagram gp-tip](evanfwelch)

---
<!-- .slide: style="text-align: left;"> -->
## Strategies we will cover:

- Building a Fake Data Ecosystem |
- Using a task scheduler |
- Chunking your "queries" wisely |
- Separating data and code |
- Using "Big Data" tools on small data |

<p class="fragment">
*Please interrupt at anytime!*
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

<br>

<p class="fragment">
#### Our database
@fa[database](http://api.reimaginebanking.com/)
</p>
---

### Possible analytical needs
- Do the customers fall into different spending cohorts? |
- Is spending predictive of other behaviors? |
- Do abrubt changes in spending indicate a life event? |


---
## Fake Data Ecosystem

### Why
* unit testing
* integration testing
* edge cases
* interpretability

---?code=generate_fake_data.py&lang=python&title=Fake Data Generator

@[1,3-30](Here we go)

---
## Use a task scheduler

#### Examples
* Luigi
* Airflow
* GNU make

Now walk through luigi example
---
## Chunk your "queries" wisely



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
