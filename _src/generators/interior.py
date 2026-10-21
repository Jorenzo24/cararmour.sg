import sys, pathlib; sys.path.insert(0, sys.argv[1] if len(sys.argv)>1 else __import__("os").path.dirname(__file__))
from kit import *

ticks="".join(f'<span style="--at:{v}%">{v}%</span>' for v in (0,20,40,60,80,100))
humid=f'''      <figure class="humid" data-reveal role="img" aria-label="Relative humidity scale from 0 to 100 percent. The US Environmental Protection Agency advises keeping indoor humidity below 60 percent. Singapore's mean relative humidity is around 82 percent.">
        <div class="humid__scale" aria-hidden="true">
          <span class="humid__zone" style="--from:0%;--to:60%"></span>
          <span class="humid__zone is-risk" style="--from:60%;--to:100%"><em>Above recommended indoor levels</em></span>
          <span class="humid__mark" style="--at:82%"><b>82%</b><small>Singapore, annual mean</small></span>
          <span class="humid__limit" style="--at:60%"><small>60%</small></span>
        </div>
        <div class="humid__ticks" aria-hidden="true">{ticks}</div>
        <figcaption>Relative humidity. Sources: Meteorological Service Singapore, 1991–2020 mean; US Environmental Protection Agency guidance on indoor humidity and mould.</figcaption>
      </figure>'''

parts=[
 part(prose('''        <h2>What interior detailing covers</h2>
        <p>
          An interior detail goes further than a vacuum and a quick wipe. Every material in the
          cabin is cleaned with a method of its own, and the places a normal clean misses get
          attention by hand: air vents, seat rails, door pockets, the gaps around the gear lever
          and the seams of the seats, where dust and crumbs settle.
        </p>
        <p>
          Using the wrong product is the most common way interiors get damaged. A household
          degreaser dries out leather, a wet brush leaves water marks on a headliner, and a glossy
          dressing on the dashboard reflects into the windscreen.
        </p>'''),
      table(["Material","Usual problem","How it is treated"],[
        ["Leather","Body oils, dye transfer from clothing, dryness","pH-balanced leather cleaner and a soft brush, then a conditioner"],
        ["Fabric seats and carpets","Ground-in dirt, stains, odours","Thorough vacuum, shampoo, then hot-water extraction"],
        ["Plastics and trim","Dust, fingerprints, fading from UV","Interior cleaner, then a matt, non-greasy UV protectant"],
        ["Glass and screens","Hazy film on the inside of the glass, fingerprints","Dedicated glass cleaner; screens with a soft microfibre"],
        ["Headliner","Stains, sagging if soaked","Spot cleaning with as little moisture as possible"]]),
      photo("car-interior-detailing",[460,700,900],1520,950,"Gloved detailer brushing the dashboard of a tan leather interior","Soft brushes reach the seams and textures a cloth cannot."),
      cta("Book interior detailing")),
 part(prose('''        <h2>Humidity and the cabin</h2>
        <p>
          Singapore's mean relative humidity is around <strong>82&nbsp;percent</strong>, according to
          the Meteorological Service Singapore. The US Environmental Protection Agency advises keeping
          indoor humidity below 60&nbsp;percent to limit mould. A closed car in a humid carpark sits
          well above that line.
        </p>'''),
      humid,
      prose('''        <p>
          Mould needs moisture and something organic to feed on: crumbs, spilled drinks, skin
          cells, the dust held in carpets. Damp floor mats and food residue in a closed cabin
          provide both, and a musty smell is usually the first sign. The air-conditioning system can
          add to it, because its evaporator stays wet while the car is in use.
        </p>
        <h3>Why steam is used</h3>
        <p>
          A steam cleaner produces vapour above 100&nbsp;°C. Hot enough to sanitise surfaces, it
          lifts dirt from seams and textured plastics without soaking them in chemicals, and it
          dries quickly. That makes it well suited to cup holders, steering wheels, door handles
          and the other surfaces hands touch every day.
        </p>'''),
      cta("Book interior detailing")),
 part(prose('''        <h2>How an interior detail is done</h2>
        <p>
          The order matters: dry dirt comes out before anything gets wet, and the cabin is left to
          air before the doors are closed.
        </p>'''),
      steps([("Empty and dry vacuum","Mats and loose items come out. Seats, carpets, rails and boot are vacuumed, with brushes to loosen what is stuck in the fibres."),
             ("Steam and agitation","Vents, seams, cup holders and controls are steamed and brushed to release dirt and sanitise them."),
             ("Material by material","Leather, fabric, plastics and glass are each cleaned with their own product, from top to bottom."),
             ("Extraction","Fabric seats, carpets and mats are shampooed and extracted with hot water, then left to dry."),
             ("Final check and airing","Glass is finished streak-free, and the doors stay open for a while so the cabin can dry out.")]),
      cta("Book interior detailing")),
 part(prose('''        <h2>Keeping the cabin clean between details</h2>
        <p>
          A few habits make the result last much longer in Singapore's climate.
        </p>
        <ul class="factors">
          <li><strong>Dry the mats.</strong> Take wet floor mats out to dry rather than leaving them in a closed car.</li>
          <li><strong>No food left behind.</strong> Crumbs and drink spills are what feeds mould and odours.</li>
          <li><strong>Leather care.</strong> A wipe with a leather cleaner every few weeks and a conditioner every few months keep it supple.</li>
          <li><strong>A sunshade.</strong> It protects the dashboard and seats from UV and keeps the cabin cooler.</li>
          <li><strong>Air-conditioning.</strong> Running the fan with the compressor off for the last few minutes of a drive helps dry the evaporator.</li>
        </ul>
        <p>
          The outside deserves the same care. A coated car keeps its finish with
          <a href="/coat-maintenance/">regular maintenance</a>, and an
          <a href="/what-is-ceramic-coating/">overview of ceramic coating</a> explains why.
        </p>''')),
]
faq=[
 ("How long does interior detailing take?","From about an hour for a car that is cleaned regularly to most of a day for a heavily soiled cabin with stained fabric seats."),
 ("Can interior detailing remove bad smells?","Most odours come from something in the cabin: spilled drinks, food residue, damp carpets or mould. Removing the source with a thorough clean, steam and extraction usually removes the smell. Air fresheners only cover it."),
 ("Is steam safe on leather?","Used briefly, with the nozzle kept moving and a cloth to wipe straight after, yes. Prolonged steam can dry leather out, which is why it is always followed by a conditioner."),
 ("How often should a car interior be detailed?","Every three to six months suits most cars in daily use. Families with young children, pet owners and drivers who eat in the car often need it more."),
 ("Will the seats be wet afterwards?","Leather is dry straight away. Fabric seats and carpets that have been extracted stay slightly damp for a few hours, less if the car can be left in the shade with the windows open."),
]
html_=page("/car-interior-detailing/","Car Interior Detailing: What It Includes | Car Armour",
 "What a car interior detail covers, how each material is cleaned, why Singapore's humidity matters for the cabin and how to keep it clean.",
 "interior","Interior detailing","What a Car Interior Detailing Session Includes","Every material, its own method",
 "A deep clean of every surface you touch.",
 "<strong>Steam</strong>, <strong>vacuum</strong> and the right product for <strong>each material</strong>.",
 "Book interior detailing",
 img("car-interior-detailing-cabin",[460,700,1000,1200],1672,941,"Supercar cabin in carbon fibre and black Alcantara with orange stitching","(min-width:960px) 44vw, 100vw",'fetchpriority="high"'),
 parts,faq,"Book an interior<br>detailing","int-faq")
pathlib.Path("_src/pages/car-interior-detailing.html").write_text(html_)
