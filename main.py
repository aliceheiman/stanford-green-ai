# main.py - The Stanford Green AI Club Website

# ----------------- IMPORTS
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime

# ----------------- BASE STYLES, COLOR, & FONTS
page_styles = Style(
"""
@import url('https://fonts.googleapis.com/css2?family=Inter&family=Roboto+Mono&family=Merriweather&display=swap');

:root {
    --primary-color: #397B5B;
    --light-color: #72EFAC;
    --gray-color: #F4F4F4;
    --secondary-color: #000138;
    --background-color: #1F0322;
}
p a {
    color: var(--primary-color) !important;
}
p, li {
    font-family: "Inter", sans-serif !important;
    color: #000;
}
h1, h2, h3, h4, h5 {
    font-family: "Inter", sans-serif !important;
    color: #000;
}
span {
    font-family: "Roboto Mono", monospace !important;}
}
.section {
    max-width: 800px !important;
    margin: 0 auto;
}
p.lift {
    text-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15)
}
.link-button p {
    font-family: "Roboto Mono", monospace !important;
    color: var(--light-color);
}
.link-button.outlined p {
    color: var(--primary-color);
}
.divround {
    border-radius: 8px;
}
.uk-list-bullet > li::before {
  display: none !important;
  content: none !important;
}
.uk-list-bullet > li {
  padding-left: 16px;
}
a.uk-slidenav-previous, a.uk-slidenav-next {
    padding: 10px;
}
"""
)

# ----------------- WEBPAGE
app, rt = fast_app(
    hdrs=(
        picolink,
        Theme.green.headers(mode="light"),
        page_styles,
    ),
    static_path="public",
    live=True,
)

@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str):
    return FileResponse(f"{fname}.{ext}")

# ----------------- COMPONENTS
# Below are components (parts of a page) written with HTMX.
# Each component is written with Python, but uses CSS and HTML
# elements. You can change any component by updating the returned
# blocks in each component.
#
# See FastHTML and MonsterUI (https://monsterui.answer.ai/api_ref/)
# for more details and examples.

def Section(tagtext: str, title: str, bcolor=None, *args, **kwargs):
    "Section with nice spacing including a header and any content"
    def _SectionContent(tagtext: str, title: str, bcolor=None, *args, **kwargs):
        divcls = "mt-10 section"
        divcls = divcls if bcolor is None else divcls + " p-4"
        return Div(
            Span(tagtext, style={"font-size": "14px", "color": "var(--primary-color)"}),
            H3(title, style={"font-size": "2rem"}, cls="mb-2"),
            *args,
            cls=divcls,
            **kwargs,
        )
    
    if bcolor is not None:
        return Div(
            _SectionContent(tagtext, title, bcolor, *args, **kwargs),
            style={"background-color": bcolor},
            cls="divround"
        )
    else:
        return _SectionContent(tagtext, title, bcolor, *args, **kwargs)
    
def LinkButton(title: str, link: str, outline=False, **kwargs):
    "Styles Link Button featuring letter spacing, link, and icon."
    btn_styles = {
        "height": "42px",
        "justify-content": "center",
        "padding": "0 10px",
        "border-radius": "20px"
    }
    if not outline:
        btn_styles["background"] = "var(--primary-color)"
        btn_styles["color"] = "var(--light-color)"
    else:
        btn_styles["background"] = "#ffffff"
        btn_styles["color"] = "var(--primary-color)"
        btn_styles["border"] = "2px solid var(--primary-color)"

    outlined = "outlined" if outline else ""

    return A(
        DivHStacked(
            P(title.upper()),
            UkIcon("move-right"),
            style=btn_styles,
            cls=f"space-x-2 link-button {outlined}",
        ),
        href=link,
        **kwargs,
    )

def ImageCaption(src: str, caption: str, source_text: str|None, source_link: str|None):
    if source_text is None:
        P_caption = P(caption, style={"text-align": "center"})
    else:
        P_caption = P(
            caption + " ",
            A(source_text, href=source_link, target="_blank"),
            style={"text-align": "center"}
        )
    return Img(
        P_caption,
        src=src,
    )

# --------- NAVBAR
# Here you can edit the links you want to display in the main navbar
def navbar_section():
    return (
        NavBar(
            A("About", href="/"),
            A("Events", href="/"),
            A("Hackathon", href="/"),
            A("Workshops", href="/"),
            A("Seminars", href="/"),
            A("Projects", href="/"),
            A("Join", href="/"),
            brand=A(Img(src="logo.png", width=150), href="/"),
            cls="ml-0 mr-0 mb-2",
        ),
    )

# --------- FOOTER
# Here you can edit the links you want to display in the footer
def SocialIcon(icon: str, link: str):
    return A(
        UkIcon(icon),
        href="/"
    )

def footer_section():
    current_year = str(datetime.now().year)
    return Div(
        Div(
            P("Stanford Green AI", style={"font-weight": "bold", "color": "var(--primary-color)"}),
            P("AI & Sustainability", style={"color": "var(--primary-color)"}),
            cls="gap-0",
        ),
        DivHStacked(
            SocialIcon("instagram", "/"),
            SocialIcon("youtube", "/"),
            SocialIcon("linkedin", "/"),
        ),
        DivHStacked(
            A("Home", href="/"),
            A("About", href="/"),
            A("Projects", href="/"),
            A("Join", href="/"),
            A("Events", href="/"),
            A("Resources", href="/"),
        ),
        DivCentered(P(f"{current_year} © Stanford Green AI"), cls="mt-6"),
        style={"background-color": "var(--gray-color)", "padding": "14px"},
        cls="mt-8 space-y-4",
    )

# ----------------- SECTIONS

def HeroSection():
    "Creates a hero-styled header with centered text and two buttons"

    cover_style = {
        "height": "40vh",
        "width": "100%",
        "position": "absolute",
        "top": "0",
        "left": "0",
    }

    return Div(
        Div(
            # Background image
            Img(
                src="green-patterns.png",
                style={
                    **cover_style,
                    "object-fit": "cover",
                    "z-index": "0",
                },
            ),
            # Transparent overlay
            Div(
                style={
                    **cover_style,
                    "background-color": "var(--primary-color)",
                    "z-index": "1",
                    "opacity": "0.6",
                }
            ),
            # Content container
            Div(
                P(
                    "At the intersection of Artificial Intelligence, sustainability, policy, and economics. Join us in building greener AI for sustainable development.",
                    style={
                        "color": "#fff",
                        "font-size": "24px",
                        "font-weight": "bold",
                        "text-align": "center",
                        "margin-bottom": "1rem",
                    },
                    cls="lift"
                ),
                DivHStacked(
                    LinkButton("Learn More", "/"),
                    LinkButton("Get Involved", "/", outline=True),
                ),
                style={
                    "position": "absolute",
                    "top": "50%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "width": "90%",
                    "padding": "10px",
                    "z-index": "2",
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center",
                    "text-align": "center",
                    "padding": "0",
                },
            ),
            style={"position": "relative", "height": "40vh", "overflow": "hidden"},
            cls="divround"
        )
    )

def OurMission():
    md = """Stanford GreenAI Institute is a student-driven community dedicated to advancing sustainable artificial intelligence.

We draw from two complementary pillars:

* **Green-in AI**: Designing and deploying AI systems that are energy efficient in both training use.

* **Green-by AI**: Leveraging AI to tackle environmental challenges and accelerate progress towards sustainable development.
"""
    return Section(
        "OUR MISSION",
        "Green-in AI & Green-by AI",
        None,
        render_md(md),
        ImageCaption("green-ai-workflow.jpg", "Green AI Algorithms.", "Source: (Bolón-Canedo et al., 2024)", "https://www-sciencedirect-com.stanford.idm.oclc.org/science/article/pii/S0925231224008671")
    )

def CurrentInitiatives():
    def InitiativeCard(title, info, description, src, link_text="Learn More", link="/", ):
        return Card(
            Img(src=src, style={"height": "200px", "width": "100%", "object-fit": "cover"}),
            H3(title),
            Span(info, style={"color": "primary-color"}),
            P(description, style={"margin": "16px 0"}),
            LinkButton(link_text, link)
        )

    initiatives = [
        InitiativeCard("Green-in AI Hackathon", "@ Stanford Climate Week, Oct 18 9am-9pm", "12-hour tech+policy hackathon to develop and shape energy-efficient AI tools.", "hackathon.png", "Learn More & Register", "/"),
        InitiativeCard("Hands-on Interdisciplinary Workshops in Green AI", "Every Week, Location TBD", "Hands-on sessions from sustainable computing, AI policy, to the economics of AI infrastructure.", "workshop.png", "See Workshop Schedule", "/"),
        InitiativeCard("Lunch Seminars and Industry Panels", "Lunch Provided, Location TBD", "Attend talks with Stanford faculty and Industry professionals advancing Green AI across disciplines.", "seminar.jpg", "Register Interest", "/")
    ]

    return Section(
        "ON-GOING",
        "Our Current Initiatives",
        "var(--gray-color)",
        Grid(
            *initiatives,
            cols_sm=1, cols_md=1, cols_lg=2
        )
        
    )

def Projects():
    def Project(title, description, imgsrc, link="/"):
        return Grid(
            Div(
                H3(title, style={"color": "#ffffff"}),
                P(description, style={"color": "#fff"}),
            ),
            Grid(
                Img(src=imgsrc, style={"height": "150px", "width": "100%", "object-fit": "cover"}),
                
                LinkButton("Learn More", link),
                style={"background-color": "#ffffff", "padding": "12px", "width": "100%", "border-radius": "8px"},
                cls="divround"
            ),
            style={"background-color": "var(--primary-color)", "padding": "18px"},
        )

    featured_projects = [
        Project("The Stanford Green AI Explorer", "Explore and track the GreenAI at Stanford University through our interactive dashboard.", "pattern.png", "/"),
        Project("Have a project idea?", "We welcome project ideas, just reach out and we would love to talk!", "pattern.png", "/"),
    ]

    return Section(
        "PROJECTS",
        "Discover and Participate in Green AI Projects at Stanford",
        None,
        Slider(*featured_projects)
    )

def RegisterSignup():
    return Grid(
        H3("Register your email for information on upcoming events and opportunities", style={"color": "#fff", "text-align": "center"}),
        LinkButton("Sign up", "/", outline=True),
        style={"background-color": "var(--primary-color)", "padding":"16px"},
        cls="divround"
    )

def Resources():
    md = """We curate tools, readings, and references for understanding and building Green AI.
* Check out the [Green AI Summit 2025](https://www.greenai.institute/2025summit)
* Our [Special Issue](https://www-sciencedirect-com.stanford.idm.oclc.org/special-issue/322671/innovative-environmental-solutions-towards-green-and-sustainable-artificial-intelligence) on Green and Sustainable Artificial Intelligence
* A great review article on Green AI by [(Bolón-Canedo et al., 2024)](https://www-sciencedirect-com.stanford.idm.oclc.org/science/article/pii/S0925231224008671)
* ...and much more!
"""

    return Section(
        "RESOURCES",
        "Stay up to date on Green AI at Stanford and beyond",
        None,
        render_md(md),
        RegisterSignup()
    )

def Contact():
    return Section(
        "CONTACT",
        "Sounds Interesting? We would love to collaborate!",
        None,
        LinkButton("Contact Us", "/")
    )

# ----------------- PAGES
# Below are the actual pages of the website, i.e. the pages
# that display when you type / or /routes in the url bar.

# --------- HOME PAGE
@rt("/")
def get():
    return Container(
        navbar_section(),
        HeroSection(),
        OurMission(),
        CurrentInitiatives(),
        Projects(),
        Resources(),
        Contact(),
        footer_section()
    )

serve()
