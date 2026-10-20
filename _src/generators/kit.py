"""Gabarit commun des pages service informationnelles."""
import json, html
B="{{booking}}"; WA="{{whatsapp}}"; PH="{{phoneDisplay}}"; HRS="{{hours}}"; ORI="{{origin}}"
ARROW='<svg class="ico" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def img(name, widths, w, h, alt, sizes, extra='loading="lazy"'):
    srcset=",\n                 ".join(f"/assets/img/{name}-{x}.webp {x}w" for x in widths)
    return (f'<img src="/assets/img/{name}-{widths[-1]}.webp"\n           srcset="{srcset}"\n'
            f'           sizes="{sizes}"\n           alt="{alt}" width="{w}" height="{h}" {extra} decoding="async">')

def photo(name, widths, w, h, alt, caption):
    return f'''      <figure class="photo" data-reveal>
        <div class="photo__frame">
          {img(name,widths,w,h,alt,"(min-width:1100px) 704px, 100vw")}
        </div>
        <figcaption>{caption}</figcaption>
      </figure>'''

def cta(label):
    return f'''      <p class="inline-cta" data-reveal>
        <a class="btn btn--primary" href="{B}">{label}</a>
      </p>'''

def prose(inner):
    return f'''      <div class="prose-col" data-reveal>
{inner}
      </div>'''

def part(*blocks):
    return '    <div class="article__part">\n'+"\n\n".join(blocks)+'\n    </div>'

def table(cols, rows, hero=None, cls=""):
    HC=' class="is-hero"'
    head="".join(f'<th scope="col"{HC if i==hero else ""}>{c}</th>' for i,c in enumerate(cols))
    body=""
    for r in rows:
        cells="".join(f'\n            <td data-th="{html.escape(cols[i+1])}"{HC if i+1==hero else ""}>{v}</td>' for i,v in enumerate(r[1:]))
        body+=f'\n          <tr>\n            <th scope="row">{r[0]}</th>{cells}\n          </tr>'
    return f'''      <div class="sheet-wide">
        <div class="table-scroll" data-reveal>
          <table class="table-compare {cls}">
            <thead><tr>{head}</tr></thead>
            <tbody>{body}
            </tbody>
          </table>
        </div>
      </div>'''

def steps(items):
    lis="\n".join(f'          <li class="step">\n            <h3>{t}</h3>\n            <p>{d}</p>\n          </li>' for t,d in items)
    return f'''      <div class="prose-col">
        <ol class="steps" data-reveal>
{lis}
        </ol>
      </div>'''

def page(route, title, desc, nav, crumb, h1, h1sub, lead_b, lead, btn, hero_img, parts, faq, cta_title, faq_id):
    faq_html="\n".join(f'''      <div class="accordion__item">
        <h3 style="margin:0"><button class="accordion__trigger" type="button" aria-expanded="false" aria-controls="{faq_id}-{i}"><span class="accordion__sign" aria-hidden="true"></span>{html.escape(q)}</button></h3>
        <div class="accordion__panel" id="{faq_id}-{i}"><div>
          <p>{html.escape(a)}</p>
        </div></div>
      </div>''' for i,(q,a) in enumerate(faq,1))
    ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},indent=2,ensure_ascii=False)
    meta=json.dumps({"route":route,"title":title,"description":desc,"ogType":"article","ogImage":"/assets/img/og-default.jpg","nav":nav},indent=2,ensure_ascii=False)
    return f'''<!--META {meta} -->

<!-- ─────────────────────── EN-TETE ─────────────────────── -->
<section class="page-hero">
  <div class="container container--wide">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Home</a></li>
        <li aria-current="page">{crumb}</li>
      </ol>
    </nav>

    <div class="page-hero__grid">
      <div data-reveal="0" data-reveal-on="load">
        <h1>{h1}<span>{h1sub}</span></h1>
        <p class="page-hero__lead">
          <strong>{lead_b}</strong>
          <span>{lead}</span>
        </p>
        <div class="cta-actions">
          <a class="btn btn--primary btn--lg" href="{B}">{btn}</a>
          <a class="btn btn--ghost btn--lg" href="{WA}" target="_blank" rel="noopener">WhatsApp {PH}</a>
        </div>
      </div>

      <figure class="page-hero__media" data-reveal="1" data-reveal-on="load">
        {hero_img}
      </figure>
    </div>
  </div>
</section>

<!-- ─────────────────── ARTICLE : colonne centrale ─────────────────── -->
<section class="article">
  <div class="sheet">

{chr(10).join(parts)}

  </div>
</section>

<!-- ─────────────────── FAQ ─────────────────── -->
<section class="section section--paper section--paper-grain">
  <div class="container container--narrow">
    <div class="section-head section-head--center">
      <div>
        <h2>{crumb} questions</h2>
      </div>
    </div>

    <div class="accordion accordion--panels" data-reveal>
{faq_html}
    </div>

<script type="application/ld+json">
{ld}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{ORI}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{crumb}", "item": "{ORI}{route}" }}
  ]
}}
</script>
  </div>
</section>

<!-- ─────────────────── CTA ─────────────────── -->
<section class="section section--sm cta-band section--edge">
  <div class="container container--wide">
    <div class="section-head section-head--split" style="margin-bottom:0">
      <div>
        <h2 class="mb-0">{cta_title}</h2>
      </div>
      <div>
        <p class="lead" style="margin-bottom:1.9rem">
          {HRS}.<br>
          Send us the model and the postal code.
        </p>
        <div class="cta-actions">
          <a class="btn btn--primary" href="{B}">{btn}</a>
          <a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp {PH}</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''
