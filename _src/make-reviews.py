import json, html, re, pathlib, datetime
R=json.load(open("_src/reviews.json"))
# Avis mitige de Nasri Haron ecarte en attendant l'accord du client
R=[r for r in R if r["name"]!="Nasri Haron"]
TAGS=[("coating","Coating",r"coat"),("polish","Polish",r"polish|shin|water ?mark|scratch"),
      ("maintenance","Maintenance",r"maintenance"),("interior","Interior",r"interior")]
def tags(t): return [k for k,_,rx in TAGS if re.search(rx,t,re.I)]
def initials(n):
    p=n.split(); return (p[0][0]+(p[-1][0] if len(p)>1 else "")).upper() if p[0].isascii() else n[0]
def date(d): return datetime.datetime.strptime(d,"%B %d, %Y").strftime("%B %Y")
feat=next(r for r in R if r["name"]=="Jenne Foo")
rest=[r for r in R if r is not feat]
counts={k:sum(k in tags(r["text"]) for r in R) for k,_,_ in TAGS}
chips='<button class="chip is-on" type="button" data-filter="all" aria-pressed="true">All <span>'+str(len(R))+'</span></button>'+"".join(
  f'<button class="chip" type="button" data-filter="{k}" aria-pressed="false">{lab} <span>{counts[k]}</span></button>' for k,lab,_ in TAGS if counts[k])
cards="\n".join(f'''        <article class="quote" data-tags="{' '.join(tags(r['text']))}">
          <p class="quote__text">{html.escape(r['text'])}</p>
          <footer class="quote__who"><span class="quote__avatar" aria-hidden="true">{html.escape(initials(r['name']))}</span><span><span class="quote__name">{html.escape(r['name'])}</span><span class="quote__meta">Facebook · {date(r['date'])}</span></span></footer>
        </article>''' for r in rest)
page=f'''<!--META {{
  "route": "/reviews/",
  "title": "Car Armour SG Reviews | Ceramic Coating & Detailing Customers",
  "description": "What customers say about Car Armour's ceramic coating, polishing, interior detailing and maintenance, done at their residence in Singapore.",
  "ogType": "website",
  "ogImage": "/assets/img/og-default.jpg",
  "nav": "reviews"
}} -->

<!-- Avis : source _src/reviews.json (30 avis Facebook recuperes sur l'ancien
     site, tous de 2021). Page generee par un script, a regenerer quand les avis
     Google arriveront. L'avis mitige de Nasri Haron est ecarte en attendant
     l'accord du client. Les avis citant Ivan sont publies tels quels. -->
<section class="reviews-hero">
  <div class="container container--wide">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Home</a></li>
        <li aria-current="page">Reviews</li>
      </ol>
    </nav>

    <div class="reviews-hero__grid">
      <div data-reveal="0" data-reveal-on="load">
        <h1>Car Armour SG Reviews</h1>
        <p class="page-hero__lead">
          <strong>What our customers say, in their own words.</strong>
          <span>Ceramic coating, polishing and maintenance, <strong>done at their residence</strong>.</span>
        </p>
        <div class="cta-actions">
          <a class="btn btn--primary btn--lg" href="{{{{booking}}}}">Book a slot</a>
        </div>
      </div>

      <blockquote class="featured-quote" data-reveal="1" data-reveal-on="load">
        <p>{html.escape(feat['text'])}</p>
        <footer><span class="quote__name">{html.escape(feat['name'])}</span><span class="quote__meta">Facebook · {date(feat['date'])}</span></footer>
      </blockquote>
    </div>
  </div>
</section>

<section class="section section--charcoal section--edge">
  <div class="container container--wide">
    <div class="chips" role="group" aria-label="Filter reviews by service" data-reveal>
      {chips}
    </div>

    <div class="quotes" data-reveal>
{cards}
    </div>

    <div class="leave-review" data-reveal>
      <h2>Had your car done by us?</h2>
      <div class="cta-actions">
        <a class="btn btn--ghost" href="https://www.facebook.com/pg/101224595060447/reviews/" target="_blank" rel="noopener">Review us on Facebook</a>
        <a class="btn btn--ghost" href="https://www.google.com/maps/search/?api=1&amp;query=Car+Armour+SG" target="_blank" rel="noopener">Review us on Google</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--sm cta-band section--edge">
  <div class="container container--wide">
    <div class="section-head section-head--split" style="margin-bottom:0">
      <div>
        <h2 class="mb-0">Treat your car<br>the right way</h2>
      </div>
      <div>
        <p class="lead" style="margin-bottom:1.9rem">
          {{{{hours}}}}.<br>
          Send us the model and the postal code.
        </p>
        <div class="cta-actions">
          <a class="btn btn--primary" href="{{{{booking}}}}">Book a slot</a>
          <a class="btn btn--ghost" href="{{{{whatsapp}}}}" target="_blank" rel="noopener">WhatsApp {{{{phoneDisplay}}}}</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''
pathlib.Path("_src/pages/reviews.html").write_text(page)
print(len(R), counts)
