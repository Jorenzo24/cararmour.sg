import sys, pathlib; sys.path.insert(0, sys.argv[1] if len(sys.argv)>1 else __import__("os").path.dirname(__file__))
from kit import *

def rays(x0, flat):
    # rayons incidents paralleles venant de la gauche, reflechis selon la surface
    out=[]; base=150
    surf = f'<line x1="{x0}" y1="{base}" x2="{x0+220}" y2="{base}" class="d-surface"/>' if flat else \
        '<polyline class="d-surface" points="'+" ".join(f"{x0+i*20},{base}" if i%2==0 else f"{x0+i*20-10},{base} {x0+i*20},{base-9}" for i in range(12))+f' {x0+220},{base}"/>'
    import math
    hits=[x0+40,x0+80,x0+120,x0+160]
    angles=[0,0,0,0] if flat else [-38,22,-12,40]
    for hx,da in zip(hits,angles):
        sx,sy=hx-70,base-110
        out.append(f'<line x1="{sx}" y1="{sy}" x2="{hx}" y2="{base-2}" class="d-in"/>')
        a=math.radians(-58+da); L=115
        ex,ey=hx+L*math.cos(a), base-2+L*math.sin(a)
        out.append(f'<line x1="{hx}" y1="{base-2}" x2="{ex:.1f}" y2="{ey:.1f}" class="d-out"/>')
    return surf+"".join(out)

light=f'''      <figure class="diagram" data-reveal>
        <svg viewBox="0 0 520 210" role="img" aria-labelledby="light-title">
          <title id="light-title">Light hitting a level clear coat reflects in one direction. On a clear coat full of fine scratches, it scatters in all directions.</title>
          {rays(20, True)}
          {rays(280, False)}
          <text class="d-label" x="20" y="190">Level clear coat</text>
          <text class="d-value" x="20" y="206">CLEAR, SHARP REFLECTION</text>
          <text class="d-label" x="280" y="190">Clear coat with swirl marks</text>
          <text class="d-value" x="280" y="206">LIGHT SCATTERS, PAINT LOOKS HAZY</text>
        </svg>
        <figcaption>Why swirl marks show: each scratch sends light off at a different angle. Schematic, not to scale.</figcaption>
      </figure>'''

def rrow(name, frm, to, val, hero=False):
    return f'''          <div class="range__row{' is-hero' if hero else ''}">
            <span class="range__name">{name}</span>
            <span class="range__track"><span class="range__bar" style="--from:{frm}%;--to:{to}%"></span></span>
            <span class="range__val">{val}</span>
          </div>'''
ticks="".join(f'<span style="--at:{v}%">{v}</span>' for v in (0,25,50,75,100))
thickness=f'''      <figure class="range" data-reveal aria-label="Thickness compared: a sheet of office paper is about 100 microns, a factory clear coat 35 to 55 microns, and one polishing step removes a few microns.">
        <p class="range__title" aria-hidden="true">Thickness, in microns</p>
{rrow("Sheet of office paper",0,100,"about 100 µm")}
{rrow("Factory clear coat",35,55,"35 to 55 µm")}
{rrow("One polishing step",0,3,"a few µm",True)}
        <div class="range__row range__row--axis" aria-hidden="true">
          <span></span>
          <span class="range__ticks">{ticks}</span>
          <span></span>
        </div>
        <figcaption>Typical values. Clear coat thickness varies from one maker to another, and the amount removed depends on the polish, the pad and the machine.</figcaption>
      </figure>'''

ba=f'''      <!-- AVANT / APRES : photos du client (2026-10-21), sources dans
           _src/sources/car-polishing-swirl-marks-*.png, recadrees en 16:10
           sans retouche colorimetrique. -->
      <figure class="ba" data-reveal style="--pos:50%">
        <div class="ba__frame">
          {img("car-polishing-swirl-marks-after",[460,700,1000,1200],1200,750,"Black bonnet after polishing, reflections sharp and free of swirl marks","(min-width:1100px) 704px, 100vw",'class="ba__img ba__img--after" loading="lazy"')}
          {img("car-polishing-swirl-marks-before",[460,700,1000,1200],1200,750,"The same black bonnet before polishing, covered in circular swirl marks","(min-width:1100px) 704px, 100vw",'class="ba__img ba__img--before" loading="lazy"')}
          <span class="ba__tag ba__tag--before" aria-hidden="true">Before</span>
          <span class="ba__tag ba__tag--after" aria-hidden="true">After</span>
          <span class="ba__handle" aria-hidden="true"></span>
          <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Slide to compare the paint before and after polishing">
        </div>
        <figcaption>The same panel under the same light, before and after polishing.</figcaption>
      </figure>'''

diptych=f'''      <div class="diptych" data-reveal>
        <figure class="photo">
          <div class="photo__frame">
            {img("car-polishing-dual-action-bonnet",[460,700,1000],1448,1086,"Dual-action polisher working across the bonnet of a red sports car","(min-width:760px) 352px, 100vw")}
          </div>
          <figcaption>A dual-action polisher on a painted bonnet.</figcaption>
        </figure>
        <figure class="photo">
          <div class="photo__frame">
            {img("car-detailing-team-singapore",[460,620,900],1514,1898,"Two detailers machine polishing a black Porsche 911","(min-width:760px) 352px, 100vw")}
          </div>
          <figcaption>Polishing is done panel by panel, under strong light.</figcaption>
        </figure>
      </div>'''

parts=[
 part(prose('''        <h2>What car polishing does</h2>
        <p>
          A car polish is an abrasive liquid. Worked across the paint with a machine, its fine
          abrasive particles cut, then break down, and level the very top of the
          <strong>clear coat</strong>, the transparent layer over the colour, until the defects in it
          disappear. A wax fills and hides marks for a few weeks. A polish removes them, which is
          why the result lasts.
        </p>
        <h3>Why swirl marks show</h3>
        <p>
          A swirl mark is a fine scratch in the clear coat, usually left by a dirty wash mitt, a
          rough towel or an automated brush wash. On its own each one is tiny. Under direct sun,
          thousands of them scatter the light, and the paint looks hazy, with circular patterns
          around the reflection of the sun.
        </p>'''),
      light,
      prose('''        <h3>Water spots</h3>
        <p>
          Water spots are the other common defect in Singapore. When rain or tap water dries on the
          paint, it leaves its minerals behind, and in strong sun they can etch into the clear coat.
          Fresh spots come off with a wash. Etched ones have to be polished out.
        </p>'''),
      cta("Book polishing")),
 part(prose('''        <h2>How much clear coat a polish removes</h2>
        <p>
          A factory clear coat is usually 35 to 55 microns thick, about half the thickness of a
          sheet of office paper. A polishing step typically removes only a few microns of it. That
          margin is what allows a well-kept car to be polished several times in its life, and it is
          also why repeated aggressive polishing eventually wears through.
        </p>'''),
      thickness,
      prose('''        <p>
          Before polishing, a careful detailer measures the paint with an electronic thickness
          gauge, panel by panel. The gauge reads all the layers together, which is enough to spot a
          thin panel or one that has been resprayed.
        </p>
        <h3>What polishing cannot remove</h3>
        <p>
          A scratch that has gone through the clear coat into the colour cannot be polished out
          without cutting too deep. A simple test: if a fingernail catches in it, the scratch is
          probably too deep for polishing alone and needs a touch-up or a respray. Stone chips and
          dents are beyond polishing too.
        </p>''')),
 part(prose('''        <h2>Machines and stages</h2>
        <p>
          Two kinds of machine do most of the work. The difference between them decides how fast a
          polisher cuts, and how forgiving it is.
        </p>'''),
      table(["Criterion","Rotary polisher","Dual-action polisher"],[
        ["How it moves","Spins on a single axis","Spins and oscillates around an offset"],
        ["Cutting power","<strong>High</strong>","Moderate"],
        ["Heat on the paint","High, the pad must keep moving","Lower"],
        ["Risk of holograms","Higher in inexperienced hands","<strong>Low</strong>"],
        ["Typical use","Heavy defects, by experienced hands","Most polishing and finishing work"]]),
      prose('''        <p>
          The work usually runs in stages. A coarser compound removes the deeper defects, then a
          finer polish removes the slight haze the compound leaves behind. On paint in good
          condition, a single one-step polish is often enough.
        </p>'''),
      diptych,
      steps([("Wash and decontamination","A thorough wash, an iron remover and a clay pass, so no grit is dragged around under the pad."),
             ("Inspection and measurement","Every panel is checked under strong light, and the paint thickness is measured before anything is removed."),
             ("Compounding, where needed","A coarser compound on the panels with deeper swirls and etched water spots."),
             ("Refining","A finer polish brings back clarity and removes any haze from the first stage."),
             ("Wipe-down and final check","Polishing oils are wiped off so the true finish can be judged under the light.")]),
      ba,
      cta("Book polishing")),
 part(prose('''        <h2>Polishing on its own, or before a coating</h2>
        <p>
          Freshly polished paint is bare. It starts collecting new marks and contamination from the
          first wash, so polishing is usually followed by protection: a wax for a few months, or a
          <a href="/what-is-ceramic-coating/">ceramic</a> or
          <a href="/what-is-graphene-coating/">nano graphene coating</a> for several years. The
          protection preserves the finish but does not improve it, so the polishing always comes
          first.
        </p>
        <p>
          Because it removes material, polishing is done when the paint needs it rather than on a
          fixed schedule. On a car washed with care, once every year or two is often enough. Careful
          washing is what keeps that interval long, and it is the main purpose of
          <a href="/coat-maintenance/">coat maintenance</a>.
        </p>'''),
      cta("Book polishing")),
]
faq=[
 ("Will polishing remove all scratches?","It removes swirl marks, water spots and light scratches that sit within the clear coat. A scratch deep enough to catch a fingernail usually goes through the clear coat and needs a touch-up or a respray instead."),
 ("Is polishing bad for the paint?","Each polishing step removes a few microns of clear coat out of the 35 to 55 a factory finish usually has. Done carefully, with the paint measured first, a car can be polished several times in its life. The risk comes from repeated, aggressive polishing."),
 ("What is the difference between polishing and waxing?","Polishing removes a thin layer of clear coat to level out defects. Waxing adds a protective layer on top without removing anything. A wax can hide light marks for a few weeks; polishing removes them."),
 ("Does a new car need polishing?","Often, lightly. New cars collect marks during transport, storage and pre-delivery washing. A gentle one-step polish before a coating makes sure the coating seals in a clean finish rather than those marks."),
 ("How long does car polishing take?","A light one-step polish on a car in good condition takes a couple of hours. A multi-stage polish on paint with heavy swirls can take most of a day."),
]
html_=page("/car-polishing/","Car Polishing Explained: Swirl Marks & Water Spots | Car Armour",
 "What car polishing removes, how much clear coat it takes off, rotary versus dual-action machines, and when to polish before a ceramic coating.",
 "polishing","Car polishing","Car Polishing Explained","Swirl marks, water spots and light scratches",
 "Polishing levels the clear coat by a few microns.",
 "It removes <strong>swirl marks</strong> and <strong>water spots</strong> and brings back a <strong>deep gloss</strong>.",
 "Book polishing",
 img("car-polishing-paint-correction",[460,700,900,1200],2530,1581,"Detailer machine polishing the wing of a dark car","(min-width:960px) 44vw, 100vw",'fetchpriority="high"'),
 parts,faq,"Book a<br>polishing","pol-faq")
pathlib.Path("_src/pages/car-polishing.html").write_text(html_)
