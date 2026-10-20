import sys, pathlib, math; sys.path.insert(0, sys.argv[1] if len(sys.argv)>1 else __import__("os").path.dirname(__file__))
from kit import *

def drop(cx, theta, area=1600, base=120):
    t=math.radians(theta)
    # aire constante : meme volume de goutte, seul l'angle change
    seg=lambda r: r*r*(t-math.sin(t)*math.cos(t))
    r=math.sqrt(area/(t-math.sin(t)*math.cos(t)))
    a=r*math.sin(t); h=r*(1-math.cos(t))
    large=1 if theta>90 else 0
    path=f'<path class="d-drop" d="M{cx-a:.1f},{base} A{r:.1f},{r:.1f} 0 {large} 1 {cx+a:.1f},{base} Z"/>'
    # tangente au point de contact droit
    tx=cx+a; L=34
    ang=math.pi-t
    tan=f'<line class="d-tan" x1="{tx:.1f}" y1="{base}" x2="{tx+L*math.cos(ang):.1f}" y2="{base-L*math.sin(ang):.1f}"/>'
    return path+tan, h
items=[(95,120,"Clean coating","OVER 90°: WATER BEADS"),(265,75,"Clogged surface","UNDER 90°: DROPS FLATTEN"),(435,25,"Bare paint","WATER SPREADS OUT")]
g=""
for cx,th,lab,val in items:
    d,h=drop(cx,th); g+=d
    g+=f'<text class="d-label" x="{cx}" y="150" text-anchor="middle">{lab}</text><text class="d-value" x="{cx}" y="168" text-anchor="middle">{val}</text>'
drops=f'''      <figure class="diagram" data-reveal>
        <svg viewBox="0 0 530 180" role="img" aria-labelledby="drops-title">
          <title id="drops-title">The same drop of water on three surfaces. On a clean coating it beads, with a contact angle over 90 degrees. On a clogged surface it flattens. On bare paint it spreads out.</title>
          <line class="d-surface" x1="0" y1="120" x2="530" y2="120"/>
          {g}
        </svg>
        <figcaption>The contact angle is the angle a drop makes with the surface. Above 90 degrees, a surface is called hydrophobic. Schematic.</figcaption>
      </figure>'''

parts=[
 part(prose('''        <h2>Why a coating stops beading</h2>
        <p>
          A coating rarely fails all at once. What happens first is that its surface clogs. Traffic
          film, minerals left by dried water and fine iron particles from brake dust settle on it
          and mask its water-repelling properties. The coating is still there underneath, but water
          no longer beads and dirt sticks more easily.
        </p>
        <p>
          Much of coat maintenance is simply removing that layer, so the coating can work as it did
          on the first day.
        </p>'''),
      drops,
      prose('''        <h3>A simple test at home</h3>
        <p>
          Spray water on a clean panel. Tight, round beads that roll off quickly mean the coating is
          doing its job. Flat, irregular drops that cling to the paint mean the surface needs
          decontaminating or a top-up.
        </p>'''),
      cta("Book coat maintenance")),
 part(prose('''        <h2>Washing a coated car</h2>
        <p>
          Washing is where a coating is kept or worn out. Most of the damage comes from the
          products and tools used, not from how often the car is washed.
        </p>'''),
      table(["Step","Do","Avoid"],[
        ["Shampoo","pH-neutral car shampoo","Dish soap and strong degreasers"],
        ["Method","Two buckets with grit guards and a clean mitt","One bucket and a sponge"],
        ["Drying","A soft, clean microfibre towel or an air blower","Old towels and rubber water blades"],
        ["Car wash","Hand wash or a touchless wash","<strong>Automated brush washes</strong>"],
        ["Timing","In the shade, on cool panels","In direct midday sun"]], hero=1),
      prose('''        <p>
          Washing in the sun is a particular problem in Singapore. The water dries before it can be
          rinsed off and leaves mineral spots, which are the most common reason a coating loses its
          beading. Bird droppings and tree sap should come off as soon as possible too: left to bake
          in the heat, they can etch through to the paint.
        </p>'''),
      cta("Book coat maintenance")),
 part(prose('''        <h2>What a maintenance session involves</h2>
        <p>
          Every few months, a more thorough session restores the surface. It goes further than a
          regular wash in two ways: it dissolves the contamination a shampoo cannot remove, and it
          renews the top of the coating.
        </p>'''),
      steps([("Decontamination wash","A pH-neutral pre-wash and contact wash, then an iron remover that dissolves embedded brake dust. The product turns purple as it reacts."),
             ("Clay, where needed","A gentle clay pass lifts what is still bonded to the surface, such as tar spots or overspray."),
             ("Silica top-up","A spray sealant based on silicon dioxide, the same compound as the coating, renews the surface and restores the beading."),
             ("Wheels and tyres","Rims are cleaned of brake dust and tar, and the tyres dressed.")]),
      prose('''        <p>
          The calendar depends on how the car lives. A car parked outdoors under trees needs
          attention more often than one that sleeps in a covered carpark.
        </p>'''),
      photo("doorstep-car-detailing-singapore",[460,700,1000],1000,600,"Car parked in a sheltered Singapore carpark","Covered parking spares a coating much of the rain and UV."),
      cta("Book coat maintenance")),
 part(prose('''        <h2>What shortens a coating's life</h2>
        <ul class="factors">
          <li><strong>Automated brush washes.</strong> The brushes hold grit from every car before yours.</li>
          <li><strong>Harsh chemicals.</strong> Strong alkaline cleaners and solvents wear the coating down faster than any weather.</li>
          <li><strong>Contamination left to bake.</strong> Droppings, sap and water spots etch in under the sun.</li>
          <li><strong>Skipped top-ups.</strong> Without them, the base layer takes all the wear.</li>
        </ul>
        <p>
          How long each type of coating lasts, and why the climate matters, is covered in the
          <a href="/what-is-ceramic-coating/">ceramic coating</a> and
          <a href="/what-is-graphene-coating/">nano graphene coating</a> guides.
        </p>''')),
]
faq=[
 ("How often should a coated car have a maintenance session?","Every few months suits most cars. Cars parked outdoors, under trees or near construction need it more often than cars kept in a covered carpark."),
 ("Can I take a coated car through an automatic car wash?","A touchless wash is fine. Automated brush washes are best avoided: the brushes carry grit from previous cars and leave fine scratches that dull the coating."),
 ("What is a silica top-up spray?","A spray sealant based on silicon dioxide, the main ingredient of ceramic coatings. Applied to a clean surface, it renews the top layer and restores beading, so the coating underneath takes less wear."),
 ("Does a coating mean I can wash the car less often?","It makes each wash quicker and easier, because dirt does not stick as well. Contamination still builds up, though, and left too long it masks the coating. Regular gentle washing keeps it working."),
 ("How do I remove bird droppings from a coated car?","As soon as possible: soak the dropping with water or a quick detailer for a minute, then lift it off with a soft microfibre without scrubbing. Left to bake in the sun, it can etch the surface."),
]
html_=page("/coat-maintenance/","How to Maintain a Coated Car in Singapore | Car Armour",
 "Why a coating stops beading, how to wash a coated car, what a maintenance session involves and what shortens a coating's life in Singapore.",
 "maintenance","Coat maintenance","How to Maintain a Coated Car","Keeping a coating at its best in Singapore's climate",
 "A coating performs only as well as it is washed.",
 "<strong>Gentle washing</strong> and a <strong>regular top-up</strong> keep it beading for years.",
 "Book coat maintenance",
 img("car-grooming-maintenance",[460,700,900],2534,1584,"Detailer wiping down a beaded black car","(min-width:960px) 44vw, 100vw",'fetchpriority="high"'),
 parts,faq,"Book a coat<br>maintenance","mnt-faq")
pathlib.Path("_src/pages/coat-maintenance.html").write_text(html_)
