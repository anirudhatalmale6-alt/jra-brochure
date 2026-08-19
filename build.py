"""Builds the JRA tri-fold brochure in two forms.

  JRA-Brochure-PRINT.pdf        11 x 8.5in, no marks - hand this to a copy shop
                                or print it in the office.
  JRA-Brochure-PRESS.pdf        11.5 x 9in, artwork bled 1/8in past trim, with
                                crop marks and fold ticks - hand this to a
                                commercial printer.

Fonts, logo, photo and QR are embedded as base64, so both files are
self-contained and render the same on any machine.

Panel geometry, both sheets:
  OUTSIDE  [ flap 3.625" ][ back cover 3.6875" ][ front cover 3.6875" ]
  INSIDE   [ panel 1 3.6875" ][ panel 2 3.6875" ][ flap inner 3.625" ]
The flap is 1/16in narrower on purpose - it folds inside, and three equal
thirds would buckle against the spine.
"""
import base64, pathlib, subprocess

ROOT = pathlib.Path('/var/lib/freelancer/projects/40266451/jra-brochure')
A = ROOT / 'assets'

W_FLAP, W_WIDE = 3.625, 3.6875
BLEED, MARK = 0.125, 0.125          # bleed, and length of a crop mark


def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()


FONT_SERIF = b64(ROOT / 'fonts/SourceSerif4.ttf', 'font/ttf')
FONT_SANS = b64(ROOT / 'fonts/Karla.ttf', 'font/ttf')
LOGO_W = b64(A / 'jra-logo-white.png', 'image/png')
LOGO_N = b64(A / 'jra-logo-navy.png', 'image/png')
PHOTO = b64(A / 'jra-photo.jpg', 'image/jpeg')
QR = b64(A / 'jra-qr.png', 'image/png')

NAVY, GOLD, MIST, PAPER = '#02275b', '#c8a24a', '#f5f6f8', '#ffffff'

IC = {
    'shield': '<path d="M12 2.5 4.5 5.6v6.2c0 4.7 3.2 8.3 7.5 9.7 4.3-1.4 7.5-5 7.5-9.7V5.6z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="m8.6 12.1 2.4 2.4 4.5-4.7" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>',
    'target': '<circle cx="12" cy="12" r="8.4" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="12" r="4.4" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/>',
    'clock': '<circle cx="12" cy="12" r="8.4" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 7v5.3l3.4 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    'badge': '<circle cx="12" cy="9.4" r="5.6" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m8.4 14.2-1.3 6.3 4.9-2.6 4.9 2.6-1.3-6.3" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    'mic': '<rect x="9.1" y="2.9" width="5.8" height="10.6" rx="2.9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M5.9 11.2a6.1 6.1 0 0 0 12.2 0M12 17.3v3.8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    'doc': '<path d="M14 2.8H6.9a1.6 1.6 0 0 0-1.6 1.6v15.2a1.6 1.6 0 0 0 1.6 1.6h10.2a1.6 1.6 0 0 0 1.6-1.6V7.4z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M14 2.8v4.6h4.7M8.6 12.4h6.8M8.6 16h6.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    'globe': '<circle cx="12" cy="12" r="8.6" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M3.4 12h17.2M12 3.4c2.2 2.4 3.4 5.4 3.4 8.6s-1.2 6.2-3.4 8.6c-2.2-2.4-3.4-5.4-3.4-8.6S9.8 5.8 12 3.4Z" fill="none" stroke="currentColor" stroke-width="1.5"/>',
    'phone': '<path d="M7.6 3.4h-2A2.4 2.4 0 0 0 3.2 6c.5 8.3 7.5 15.3 15.8 15.8a2.4 2.4 0 0 0 2.6-2.4v-2a1.6 1.6 0 0 0-1.2-1.5l-3.2-.8a1.6 1.6 0 0 0-1.6.6l-1 1.3a13.4 13.4 0 0 1-5.9-5.9l1.3-1a1.6 1.6 0 0 0 .6-1.6L9.8 4.6a1.6 1.6 0 0 0-1.6-1.2Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    'mail': '<rect x="2.9" y="5.1" width="18.2" height="13.8" rx="2" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m3.6 6.4 8.4 6 8.4-6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
    'pin': '<path d="M12 21.4s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="10.2" r="2.6" fill="none" stroke="currentColor" stroke-width="1.7"/>',
    'screen': '<rect x="2.8" y="4.2" width="18.4" height="12.4" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M8.4 20.2h7.2M12 16.6v3.6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    'people': '<circle cx="9" cy="8.4" r="3.4" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M2.9 20.1a6.1 6.1 0 0 1 12.2 0" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M16.2 5.4a3.4 3.4 0 0 1 0 6.6M17 14.6a6.1 6.1 0 0 1 4.1 5.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    'chat': '<path d="M20.6 12.6c0 4-3.9 7.2-8.6 7.2a10 10 0 0 1-2.7-.4l-5 1.6 1.6-4a6.7 6.7 0 0 1-2.5-5c0-4 3.8-7.2 8.6-7.2s8.6 3.2 8.6 7.2Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
}


def icon(name, px=15):
    return (f'<svg viewBox="0 0 24 24" style="width:{px}px;height:{px}px">{IC[name]}</svg>')


def disc(name, px=27):
    return (f'<span class="disc" style="width:{px}px;height:{px}px">'
            f'<svg viewBox="0 0 24 24" style="width:{px*0.56:.0f}px;height:{px*0.56:.0f}px">'
            f'{IC[name]}</svg></span>')


INTERPRETATION = ['In-Person Interpretation', 'Virtual Interpretation',
                  'Simultaneous Interpretation', 'Consecutive Interpretation',
                  'Court Interpretation', 'Medical / Healthcare Interpretation',
                  'Government Agencies', 'Conferences &amp; Meetings', 'Community Events']
TRANSLATION = ['Document Translation', 'Legal Documents', 'Medical Documents',
               'Business Documents', 'Personal Documents', 'Certified Translations']
PILLARS = [('shield', 'Professional &amp; Confidential', 'Your information is safe with us.'),
           ('target', 'Accurate &amp; Reliable', 'Precision in every word we deliver.'),
           ('clock', 'Fast Response Times', 'On time, every time, when you need us.'),
           ('badge', 'Experienced Professionals', 'Skilled linguists you can trust.')]
INDUSTRIES = [('shield', 'Healthcare', 'Appointments, consultations, discharge instructions.'),
              ('doc', 'Legal', 'Depositions, hearings, contracts, sworn statements.'),
              ('people', 'Education', 'Parent meetings, IEPs, school correspondence.'),
              ('globe', 'Business', 'Negotiations, training, HR, customer support.'),
              ('badge', 'Government', 'Public agencies, benefits, civic services.'),
              ('chat', 'Community', 'Events, outreach, faith and non-profit work.')]
LANGUAGES = ['Haitian Creole', 'Spanish', 'English', 'French', 'Portuguese']
MODES = [('people', 'In-Person'), ('screen', 'Virtual'), ('mic', 'Simultaneous'),
         ('chat', 'Consecutive'), ('doc', 'Translation')]


def li(items):
    return ''.join(f'<li>{x}</li>' for x in items)


CSS = f"""
@font-face {{ font-family:'JRA Serif'; src:url({FONT_SERIF}) format('truetype');
              font-weight:200 900; font-display:block; }}
@font-face {{ font-family:'JRA Sans'; src:url({FONT_SANS}) format('truetype');
              font-weight:200 800; font-display:block; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:'JRA Sans',sans-serif; color:#1d2733; background:#9aa0a8;
        -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.sheet {{ width:11in; height:8.5in; display:flex; overflow:hidden; background:#fff; }}
.panel {{ height:8.5in; position:relative; overflow:hidden; }}
.w-wide {{ width:{W_WIDE}in; }}
.w-flap {{ width:{W_FLAP}in; }}
h1,h2,h3,.serif {{ font-family:'JRA Serif',serif; }}

/* ---------------- front cover ---------------- */
.front {{ background:{NAVY}; color:#fff; display:flex; flex-direction:column; }}
.front .arc {{ position:absolute; width:7.4in; height:7.4in; border-radius:50%;
               border:1.6px solid rgba(200,162,74,.42); top:-2.6in; left:-2.5in; }}
.front .arc2 {{ position:absolute; width:9in; height:9in; border-radius:50%;
                border:1.1px solid rgba(255,255,255,.13); bottom:-4.6in; right:-3.4in; }}
.front .crest {{ position:absolute; top:0; right:0; width:1.5in; height:1.5in;
                 background:{GOLD}; clip-path:polygon(100% 0,100% 100%,0 0); opacity:.9; }}
.cov-top {{ padding:.6in .4in 0; text-align:center; position:relative; z-index:2; }}
.cov-logo {{ width:2.6in; display:block; margin:0 auto .18in; }}
.cov-rule {{ width:1.05in; height:2px; background:{GOLD}; margin:.18in auto; }}
.cov-tag {{ font-family:'JRA Serif',serif; font-style:italic; font-size:10.2pt;
            color:#e9dcbe; white-space:nowrap; }}
.cov-photo {{ margin-top:.3in; height:2.02in; width:100%;
              border-top:3px solid {GOLD}; border-bottom:3px solid {GOLD};
              background-image:url({PHOTO}); background-size:cover;
              background-position:center 11%; position:relative; z-index:2; }}
.cov-head {{ position:relative; z-index:2; padding:.28in .4in 0; text-align:center; }}
.cov-head h1 {{ font-size:25pt; line-height:1.06; font-weight:700; letter-spacing:-.2px; }}
.cov-head h1 em {{ font-style:normal; color:{GOLD}; display:block; }}
.cov-sub {{ font-size:9.4pt; line-height:1.5; color:#c3cee2; margin-top:.13in; }}
.cov-foot {{ margin-top:auto; position:relative; z-index:2; text-align:center;
             padding:0 .3in .4in; }}
.cov-quote {{ font-family:'JRA Serif',serif; font-size:12.6pt; line-height:1.34; color:#fff; }}
.cov-quote b {{ color:{GOLD}; font-weight:600; display:block; }}
.cov-web {{ margin-top:.22in; font-size:9.4pt; font-weight:700; letter-spacing:.7px;
            color:#fff; border-top:1px solid rgba(255,255,255,.22); padding-top:.15in; }}

/* ---------------- shared ---------------- */
.pad {{ padding:.42in .32in; height:100%; display:flex; flex-direction:column; }}
.eyebrow {{ font-size:7.6pt; letter-spacing:2.4px; font-weight:700; color:{GOLD};
            text-transform:uppercase; }}
.sec-h {{ font-family:'JRA Serif',serif; font-size:16.4pt; line-height:1.1;
          color:{NAVY}; font-weight:700; margin:.07in 0 .13in; }}
.hr {{ height:2px; background:{GOLD}; width:.72in; margin-bottom:.18in; }}
p.body {{ font-size:9.4pt; line-height:1.56; color:#39465a; }}
.disc {{ display:inline-flex; align-items:center; justify-content:center;
         background:{NAVY}; color:#fff; border-radius:50%; flex:0 0 auto; }}
.note {{ background:#fff; border:1px solid #e2e6ec; border-left:3px solid {NAVY};
         padding:.14in .15in; font-size:8.5pt; line-height:1.46; color:#39465a; }}
.note b {{ color:{NAVY}; }}
.cta {{ background:{GOLD}; color:{NAVY}; text-align:center; padding:.155in .1in;
        font-weight:800; font-size:10.2pt; letter-spacing:.8px; text-transform:uppercase; }}

/* ---------------- flap, outer face ---------------- */
.flapout {{ background:{MIST}; }}
.flapout .bigq {{ font-family:'JRA Serif',serif; font-size:19.4pt; line-height:1.12;
                  color:{NAVY}; font-weight:700; }}
.flapout .bigq span {{ color:{GOLD}; }}
.pillars {{ margin-top:.24in; display:flex; flex-direction:column; gap:.15in; }}
.pill {{ display:flex; gap:.13in; align-items:flex-start; background:#fff;
         border:1px solid #e2e6ec; border-left:3px solid {GOLD}; padding:.115in .14in; }}
.pill h4 {{ font-size:9pt; color:{NAVY}; text-transform:uppercase; letter-spacing:.5px;
            font-weight:800; line-height:1.2; }}
.pill p {{ font-size:8.3pt; color:#5b6779; line-height:1.42; margin-top:2px; }}
.qcard {{ margin-top:.26in; border-top:1px solid #dde2e9; border-bottom:1px solid #dde2e9;
          padding:.2in .05in; text-align:center; font-family:'JRA Serif',serif;
          font-size:12.2pt; line-height:1.3; color:{NAVY}; }}
.qcard b {{ display:block; color:{GOLD}; font-weight:600; }}
.strip {{ margin-top:auto; background:{NAVY}; color:#fff; padding:.17in .16in;
          text-align:center; }}
.strip .k {{ color:{GOLD}; font-weight:800; font-size:9.2pt; letter-spacing:1.1px; }}
.strip .v {{ font-size:8.3pt; color:#cfd9ea; margin-top:2px; }}

/* ---------------- back cover ---------------- */
.back .logo {{ width:2.05in; display:block; margin-bottom:.2in; }}
.contact {{ margin-top:.04in; display:flex; flex-direction:column; gap:.13in; }}
.crow {{ display:flex; gap:.13in; align-items:flex-start; }}
.crow .k {{ font-size:7.4pt; letter-spacing:1.5px; text-transform:uppercase;
            color:#8794a8; font-weight:700; }}
.crow .v {{ font-size:9.9pt; color:{NAVY}; font-weight:700; line-height:1.28;
            word-break:break-word; }}
.crow .v small {{ display:block; font-weight:400; font-size:8.2pt; color:#5b6779;
                  margin-top:1px; }}
.qrbox {{ margin-top:.22in; border:1px solid #dfe4ea; padding:.15in;
          display:flex; gap:.16in; align-items:center; }}
.qrbox img {{ width:1.1in; height:1.1in; display:block; }}
.qrbox .t {{ font-size:8.4pt; line-height:1.4; color:#39465a; }}
.qrbox .t b {{ display:block; color:{NAVY}; font-size:9pt; margin-bottom:3px; }}
.tagline {{ text-align:center; font-family:'JRA Serif',serif; font-style:italic;
            font-size:10pt; color:{NAVY}; margin-top:.16in; }}
.modes {{ margin-top:auto; display:flex; border-top:1px solid #e2e6ec; padding-top:.15in; }}
.mode {{ text-align:center; color:{NAVY}; flex:1 1 0; min-width:0; padding:0 1px; }}
.mode span {{ display:block; font-size:5.4pt; letter-spacing:.1px; font-weight:700;
              margin-top:3px; text-transform:uppercase; color:#5b6779; line-height:1.15; }}

/* ---------------- inside ---------------- */
.svc {{ list-style:none; margin-top:.04in; }}
.svc li {{ font-size:9.3pt; line-height:1.34; color:#39465a; padding:.07in 0 .07in .21in;
           border-bottom:1px solid #eceff3; position:relative; }}
.svc li:before {{ content:''; position:absolute; left:0; top:.142in; width:5px; height:5px;
                  background:{GOLD}; transform:rotate(45deg); }}
.svc li:last-child {{ border-bottom:none; }}
.panel-head {{ display:flex; gap:.14in; align-items:center; margin-bottom:.13in; }}
.photoband {{ margin-top:auto; height:1.42in; border-top:3px solid {GOLD};
              background-image:url({PHOTO}); background-size:cover;
              background-position:center 30%; }}
.langs {{ display:flex; flex-wrap:wrap; gap:.07in; margin-top:.11in; }}
.langs span {{ font-size:8.3pt; font-weight:700; color:{NAVY}; background:#eef1f6;
               border:1px solid #dde3ec; padding:.055in .11in; }}
.langs span.more {{ background:{NAVY}; color:#fff; border-color:{NAVY}; }}
.ind {{ display:flex; flex-direction:column; gap:.13in; margin-top:.03in; }}
.ind .row {{ display:flex; gap:.13in; align-items:flex-start; }}
.ind h4 {{ font-size:9.1pt; color:{NAVY}; font-weight:800; letter-spacing:.3px; }}
.ind p {{ font-size:8.2pt; color:#5b6779; line-height:1.42; margin-top:1px; }}
.step {{ display:flex; gap:.13in; align-items:flex-start; padding:.095in 0; }}
.step .n {{ flex:0 0 auto; width:.235in; height:.235in; border-radius:50%; background:{NAVY};
            color:#fff; font-size:8.4pt; font-weight:800; display:flex;
            align-items:center; justify-content:center; }}
.step .x {{ font-size:8.7pt; line-height:1.42; color:#39465a; }}
.step .x b {{ color:{NAVY}; display:block; font-size:9.1pt; }}
.ribbon {{ background:{NAVY}; color:#fff; text-align:center; padding:.19in .14in;
           margin-top:auto; }}
.ribbon b {{ font-family:'JRA Serif',serif; display:block; font-size:12.4pt; line-height:1.22; }}
.ribbon i {{ display:block; font-style:italic; color:{GOLD}; font-size:10pt; margin-top:3px; }}
.flapin {{ background:{MIST}; }}

/* ---------------- press furniture ---------------- */
.page {{ position:relative; width:{11+2*(BLEED+MARK)}in; height:{8.5+2*(BLEED+MARK)}in;
         background:#fff; overflow:hidden; }}
.under {{ position:absolute; left:{MARK}in; top:{MARK}in;
          width:{11+2*BLEED}in; height:{8.5+2*BLEED}in; display:flex; }}
.art {{ position:absolute; left:{MARK+BLEED}in; top:{MARK+BLEED}in; }}
.mk {{ position:absolute; background:#000; }}
.fold {{ position:absolute; background:#000; opacity:.65; }}
"""

OUTSIDE_BG = [MIST, PAPER, NAVY]
INSIDE_BG = [PAPER, PAPER, MIST]

FRONT = f"""
  <section class="panel w-wide front">
    <div class="arc"></div><div class="arc2"></div><div class="crest"></div>
    <div class="cov-top">
      <img class="cov-logo" src="{LOGO_W}" alt="JRA Interpretation and Translation Services, LLC">
      <div class="cov-rule"></div>
      <div class="cov-tag">Precision in Language &nbsp;&middot;&nbsp; Excellence in Service</div>
    </div>
    <div class="cov-photo"></div>
    <div class="cov-head">
      <h1>Interpretation<em>&amp; Translation</em></h1>
      <div class="cov-sub">Professional language services for businesses,
        government, healthcare, legal and community.</div>
    </div>
    <div class="cov-foot">
      <div class="cov-quote">&ldquo;Bridging Languages.<b>Connecting People.&rdquo;</b></div>
      <div class="cov-web">WWW.JRAINTERPRETATION.COM</div>
    </div>
  </section>"""

BACK = f"""
  <section class="panel w-wide back"><div class="pad">
    <img class="logo" src="{LOGO_N}" alt="JRA">
    <div class="eyebrow">Let's connect</div>
    <div class="sec-h">Get the language support<br>you need to move forward.</div>
    <div class="hr"></div>
    <div class="contact">
      <div class="crow">{disc('phone',24)}<div><div class="k">Telephone</div>
        <div class="v">(954) 325-9553</div></div></div>
      <div class="crow">{disc('globe',24)}<div><div class="k">Website</div>
        <div class="v">www.JRAinterpretation.com</div></div></div>
      <div class="crow">{disc('mail',24)}<div><div class="k">Email</div>
        <div class="v">Contact@jrainterpretation.com</div></div></div>
      <div class="crow">{disc('pin',24)}<div><div class="k">Service area</div>
        <div class="v">Serving Clients Nationwide
        <small>In-Person &amp; Virtual Services Available</small></div></div></div>
    </div>
    <div class="qrbox">
      <img src="{QR}" alt="Scan to open www.jrainterpretation.com">
      <div class="t"><b>Scan to learn more</b>Point your phone camera at the code to
        open our website and request an interpreter.</div>
    </div>
    <div class="cta">Request an Interpreter Today</div>
    <div class="tagline">Precision in Language &middot; Excellence in Service</div>
    <div class="modes">
      {''.join(f'<div class="mode">{icon(i)}<span>{n}</span></div>' for i, n in MODES)}
    </div>
  </div></section>"""

FLAP_OUT = f"""
  <section class="panel w-flap flapout"><div class="pad">
    <div class="eyebrow">Who we are</div>
    <div class="bigq">Clear communication.<br><span>Stronger connections.</span></div>
    <div class="hr" style="margin-top:.15in"></div>
    <p class="body">We provide accurate, confidential, and professional interpretation
      and translation services for businesses, organizations, government agencies,
      legal professionals, healthcare providers and individuals.</p>
    <div class="pillars">
      {''.join(f'<div class="pill">{disc(i,26)}<div><h4>{t}</h4><p>{d}</p></div></div>'
               for i, t, d in PILLARS)}
    </div>
    <div class="qcard">&ldquo;Bridging Languages.<b>Connecting People.&rdquo;</b></div>
    <div class="strip">
      <div class="k">SERVING CLIENTS NATIONWIDE</div>
      <div class="v">In-Person &amp; Virtual Services Available</div>
    </div>
  </div></section>"""

INSIDE_1 = f"""
  <section class="panel w-wide"><div class="pad" style="padding-bottom:0">
    <div class="panel-head">{disc('mic',30)}<div>
      <div class="eyebrow">Our services</div>
      <div class="sec-h" style="margin:0">Interpretation</div></div></div>
    <div class="hr"></div>
    <p class="body">Spoken language support, on site or connected remotely, so every
      person in the room understands what is being said - and is understood.</p>
    <ul class="svc">{li(INTERPRETATION)}</ul>
    <div class="note" style="margin-top:.18in"><b>Not sure which one you need?</b>
      Tell us who is meeting, where, and for how long. We will recommend the right
      format and confirm availability.</div>
    <div class="photoband" style="margin-left:-.32in; margin-right:-.32in"></div>
  </div></section>"""

INSIDE_2 = f"""
  <section class="panel w-wide"><div class="pad">
    <div class="panel-head">{disc('doc',30)}<div>
      <div class="eyebrow">Our services</div>
      <div class="sec-h" style="margin:0">Translation</div></div></div>
    <div class="hr"></div>
    <p class="body">Written documents rendered faithfully, formatted to match the
      original, and certified when an agency, a school or a court requires it.</p>
    <ul class="svc">{li(TRANSLATION)}</ul>
    <div class="note" style="margin-top:.2in"><b>Certified translation.</b>
      Delivered with a signed statement of accuracy, for the offices that ask for
      one. Tell us who will receive the document and we will prepare it to suit.</div>
    <div style="margin-top:.22in">
      <div class="eyebrow">Languages we support</div>
      <div class="langs">{''.join(f'<span>{l}</span>' for l in LANGUAGES)}
        <span class="more">and many more</span></div>
    </div>
    <div class="ribbon"><b>All languages.<br>All industries.</b>
      <i>One trusted partner.</i></div>
  </div></section>"""

FLAP_IN = f"""
  <section class="panel w-flap flapin"><div class="pad">
    <div class="eyebrow">Industries we serve</div>
    <div class="sec-h">Wherever language<br>gets in the way.</div>
    <div class="hr"></div>
    <div class="ind">
      {''.join(f'<div class="row">{disc(i,24)}<div><h4>{n}</h4><p>{d}</p></div></div>'
               for i, n, d in INDUSTRIES)}
    </div>
    <div style="margin-top:.24in">
      <div class="eyebrow">Requesting an interpreter</div>
      <div class="steps">
        <div class="step"><div class="n">1</div><div class="x"><b>Tell us what you need</b>
          Language, date, time, and location or virtual.</div></div>
        <div class="step"><div class="n">2</div><div class="x"><b>We confirm</b>
          You get a matched linguist and a written confirmation.</div></div>
        <div class="step"><div class="n">3</div><div class="x"><b>We deliver</b>
          On time, on site or online - every time.</div></div>
      </div>
    </div>
    <div class="cta" style="margin-top:auto">Call (954) 325-9553</div>
  </div></section>"""

SHEETS = [('outside', FLAP_OUT + BACK + FRONT, OUTSIDE_BG),
          ('inside', INSIDE_1 + INSIDE_2 + FLAP_IN, INSIDE_BG)]


def marks_html():
    """Crop marks at the four trim corners and fold ticks top and bottom."""
    T = MARK + BLEED                      # distance from media edge to trim
    pw, ph = 11 + 2 * T, 8.5 + 2 * T
    h = []
    for x in (T, T + 11):                 # vertical trim lines -> horizontal marks
        for y in (T, T + 8.5):
            h.append(f'<div class="mk" style="left:{x-0.0025}in;top:{0 if y==T else ph-MARK}in;'
                     f'width:.5pt;height:{MARK}in"></div>')
    for y in (T, T + 8.5):                # horizontal trim lines -> vertical marks
        for x in (T, T + 11):
            h.append(f'<div class="mk" style="top:{y-0.0025}in;left:{0 if x==T else pw-MARK}in;'
                     f'height:.5pt;width:{MARK}in"></div>')
    for fx in (T + W_FLAP, T + W_FLAP + W_WIDE):   # fold positions
        for top in (0, ph - MARK * 0.7):
            h.append(f'<div class="fold" style="left:{fx-0.0025}in;top:{top}in;'
                     f'width:.5pt;height:{MARK*0.7}in"></div>')
    return ''.join(h)


def build(mode):
    pages = []
    for _, body, bg in SHEETS:
        sheet = f'<div class="sheet">{body}</div>'
        if mode == 'clean':
            pages.append(sheet)
        else:
            under = ''.join(
                f'<div style="width:{w}in;background:{c}"></div>'
                for w, c in zip([W_FLAP + BLEED, W_WIDE, W_WIDE + BLEED], bg))
            pages.append(f'<div class="page">{marks_html()}'
                         f'<div class="under">{under}</div>'
                         f'<div class="art">{sheet}</div></div>')
    size = ('11in 8.5in' if mode == 'clean'
            else f'{11+2*(BLEED+MARK)}in {8.5+2*(BLEED+MARK)}in')
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>JRA Interpretation and Translation Services - Tri-Fold Brochure</title>'
            f'<style>{CSS}\n@page{{size:{size};margin:0}}'
            f'\n.sheet,.page{{page-break-after:always}}'
            f'\n.sheet:last-child,.page:last-child{{page-break-after:auto}}</style>'
            f'</head><body>{"".join(pages)}</body></html>')
    out = ROOT / f'brochure-{mode}.html'
    out.write_text(html)
    return out, size


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1200, 'height': 900})
        for mode, pdf in [('clean', 'JRA-Brochure-PRINT.pdf'), ('press', 'JRA-Brochure-PRESS.pdf')]:
            src, size = build(mode)
            w, h = size.split()
            pg.goto('file://' + str(src), wait_until='networkidle')
            pg.wait_for_timeout(1000)
            pg.pdf(path=str(ROOT / pdf), width=w, height=h, print_background=True,
                   margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
            print(mode, pdf, (ROOT / pdf).stat().st_size, 'bytes')
            if mode == 'clean':
                for i, name in enumerate(['outside', 'inside']):
                    pg.evaluate(f"document.querySelectorAll('.sheet')[{i}].scrollIntoView()")
                    pg.wait_for_timeout(300)
                    pg.screenshot(path=str(ROOT / f'preview-{name}.png'))
        b.close()

    for f in ('JRA-Brochure-PRINT.pdf', 'JRA-Brochure-PRESS.pdf'):
        print('---', f)
        subprocess.run(['pdfinfo', str(ROOT / f)])
