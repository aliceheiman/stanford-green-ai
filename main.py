# main.py - The Stanford Green AI Club Website

# ----------------- IMPORTS
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime

# ----------------- LINKS & FORMS
general_interest_link = "https://forms.gle/P9Gr877opgAxsftJ7"
team_interest_link = "https://forms.gle/pBrZJNgp6PeqGN886"
all_events_link = "https://lu.ma/stanfordgreenai"
workshop_link = "https://lu.ma/stanfordgreenai?k=c&tag=workshop"
seminar_link = "https://lu.ma/stanfordgreenai?k=c&tag=seminar"

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
    max-width: 700px !important;
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
.uk-accordion p {
    margin-bottom: 12px;
}
"""
)

# ----------------- WEBPAGE
app, rt = fast_app(
    hdrs=(
        # picolink,
        Theme.green.headers(mode="light"),
        page_styles,
    ),
    static_path="public",
    live=True,
)

# @rt("/{fname:path}.{ext:static}")
# async def get(fname: str, ext: str): 
#     return FileResponse(f'public/{fname}.{ext}')

# @rt("/{dir}/{fname:path}.{ext:static}")
# async def get(dir: str, fname: str, ext: str): 
#     return FileResponse(f'public/{dir}/{fname}.{ext}')

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
    
def LinkButton(title: str, link: str, outline=False, targetblank=True, **kwargs):
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

    a_kwargs = {
        "href": link,
        **kwargs
    }
    if targetblank:
        a_kwargs["_target"] = "blank"

    return A(
        DivHStacked(
            P(title.upper()),
            UkIcon("move-right"),
            style=btn_styles,
            cls=f"space-x-2 link-button {outlined}",
        ),
        **a_kwargs,
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
def NavbarSection():
    return (
        NavBar(
            A("About", href="/about"),
            A("Events", href="https://lu.ma/stanfordgreenai"),
            A("Hackathon", href="https://lu.ma/3pkrjzk3"),
            A("Projects", href="/projects"),
            A("Blog", href="/blog/posts"),
            A("Contact", href="/contact"),
            A("Join", href=general_interest_link),
            brand=A(Img(src="/assets/logo.png", width=150), href="/"),
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

def FooterSection():
    current_year = str(datetime.now().year)
    return Div(
        Div(
            Img(src="/assets/logo.png", width=200),
        ),
        DivHStacked(
            SocialIcon("instagram", "/"),
            SocialIcon("youtube", "/"),
            SocialIcon("linkedin", "/"),
        ),
        DivHStacked(
            A("Home", href="/"),
            A("About", href="/about"),
            A("Contact", href="/contact"),
            A("Join", href="https://forms.gle/P9Gr877opgAxsftJ7"),
            A("Blog", href="/blog/posts"),
            A("Projects", href="/projects"),
            A("Events", href="https://lu.ma/stanfordgreenai"),
            A("Workshops", href="https://lu.ma/stanfordgreenai?k=c&tag=workshop"),
            A("Seminars", href="https://lu.ma/stanfordgreenai?k=c&tag=seminar"),
            A("Resources", href="/resources"),
        ),
        Iframe(src="https://docs.google.com/forms/d/e/1FAIpQLSecLXLmDEJz7_HYF6sgjlZURLkEypPEeORhZFYrj_Z0h69Msw/viewform?embedded=true", width="100%", height="300", frameborder="0", marginheight="0", marginwidth="0"),
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
                src="/assets/green-pattern.png",
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
                    LinkButton("Learn More", "/about", targetblank=False),
                    LinkButton("Get Involved", general_interest_link, outline=True),
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
    md = """Stanford GreenAI is a student-driven community dedicated to advancing sustainable artificial intelligence.

We draw from two complementary pillars:

* **Green-in AI**: Designing and deploying AI systems that are energy efficient in both training use.

* **Green-by AI**: Leveraging AI to tackle environmental challenges and accelerate progress towards sustainable development.

Learn more about [GreenAI Institute](https://www.greenai.institute/).
"""
    return Section(
        "OUR MISSION",
        "Green-in AI & Green-by AI",
        None,
        render_md(md),
        ImageCaption("/assets/green-ai-workflow.jpg", "Green AI Algorithms.", "Source: (Bolón-Canedo et al., 2024)", "https://www-sciencedirect-com.stanford.idm.oclc.org/science/article/pii/S0925231224008671")
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
        InitiativeCard("Green-in AI Hackathon", "@ Stanford Climate Week, Oct 18 9am-9pm", "12-hour tech+policy hackathon to develop and shape energy-efficient AI tools.", "/assets/hackathon.png", "Learn More & Register", "https://lu.ma/3pkrjzk3"),
        InitiativeCard("Hands-on Interdisciplinary Workshops in Green AI", "Every Week, Location TBD", "Hands-on sessions from sustainable computing, AI policy, to the economics of AI infrastructure.", "/assets/workshops.png", "See Workshop Schedule", workshop_link),
        InitiativeCard("Lunch Seminars and Industry Panels", "Lunch Provided, Location TBD", "Attend talks with Stanford faculty and Industry professionals advancing Green AI across disciplines.", "/assets/seminars.jpg", "Register Interest", seminar_link)
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
        Project("The Stanford Green AI Explorer", "Explore and track the GreenAI at Stanford University through our interactive dashboard.", "/assets/green-dots.png", "/"),
    ]

    return Section(
        "PROJECTS",
        "Discover and Participate in Green AI Projects at Stanford",
        None,
        Slider(*featured_projects),
        P("Have a project idea? ", A("Contact us.", href="/contact"))
    )

def CTA(text, link_text, link_href, cls=""):
    return Grid(
        H3(text, style={"color": "#fff", "text-align": "center"}),
        LinkButton(link_text, link_href, outline=True),
        style={"background-color": "var(--primary-color)", "padding":"16px"},
        cls="divround" + " " + cls
    )

def RegisterSignup():
    return Grid(
        H3("Register your interest to receive updates on upcoming events and opportunities!", style={"color": "#fff", "text-align": "center"}),
        LinkButton("Sign up", "https://forms.gle/P9Gr877opgAxsftJ7", outline=True),
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

def FAQ():
    return Section(
        "FAQ",
        "Frequently Asked Questions",
        "var(--gray-color)",
        Accordion(
            
            AccordionItem(
                "What is Green AI?",
                P('According to ', A("(Bolón-Canedo et al., 2024)", href="https://www-sciencedirect-com.stanford.idm.oclc.org/science/article/pii/S0925231224008671", target="_blank"),' Green AI is an "AI paradigm which incorporates sustainable practices and techniques in model design, training, and deployment that aim to reduce the associated environmental cost and carbon footprint."'),
                P("For more information, check out our ", A("Resources", "/resources"), "."),
            ),
            AccordionItem(
                "How do I join Stanford Green AI?",
                P("For general members, please ", A("register your interest here", href=general_interest_link), " and we will be in touch with the latest events and opportunities!"),
                P("If you are interested in joining the core team, please ", A("register your interest here", href=team_interest_link), ".")
            ),
            multiple=False,
            animation=True,
        ),
    ),

def Contact():
    return Section(
        "CONTACT",
        "Sounds Interesting? We would love to collaborate!",
        None,
        LinkButton("Contact Us", "/contact", targetblank=False)
    )

# ----------------- PAGES
# Below are the actual pages of the website, i.e. the pages
# that display when you type / or /routes in the url bar.

# --------- HOME PAGE
@rt("/")
def get():
    return Container(
        NavbarSection(),
        HeroSection(),
        OurMission(),
        CurrentInitiatives(),
        Projects(),
        Resources(),
        FAQ(),
        Contact(),
        FooterSection()
    )

# --------- ABOUT PAGE
def AboutUs():
    md_1 = """### Why Green AI?

AI offers significant potential to accelerate progress toward sustainable development, with applications ranging from crop health monitoring to improved access to healthcare.

But training, deploying, and using AI models consumes considerate amounts of energy and water. 

According to the [Bloomberg Intelligence 2024 Report on AI-Driven Energy Demands](https://assets.bbhub.io/professional/sites/41/Bloomberg-Intelligence-AI-Energy-Demand-Deep-Dive.pdf), infrastructure for AI and data centers could account for **17% of US energy consumption** by 2030.
"""
    md_2 = """### Who We Are

Stanford Green AI is the Stanford chapter of Green AI Institute, a collective of researchers, academics, professionals, and students committed to the integration of artificial intelligence and environmental sustainability.

We believe that collaboration is key to driving impactful change, and that artificial intelligence and our environment is a shared responsibility. That's why we welcome and encourage people from all majors and sectors to participate!

Join us on our mission to build AI that is both intelligent and sustainable!

Curious to learn more? Check out the [2025 Green AI Summit](https://www.youtube.com/embed/QjFHNz33wAs?si=7AvgSoKUX_ta226K) and our [Resources Page](/resources) to learn more.
"""

    return Section(
        "ABOUT",
        "Stanford Green AI",
        None,
        render_md(md_1),
        Grid(
            Iframe(width="100%", height="350", src="https://www.youtube.com/embed/dZokRm7esxU?si=Zz-O8aIKsf2KXHsc", title="YouTube video player", frameborder="0", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share", referrerpolicy="strict-origin-when-cross-origin", allowfullscreen=True),
            Iframe(width="100%", height="350", src="https://www.youtube.com/embed/QjFHNz33wAs?si=7AvgSoKUX_ta226K", title="YouTube video player", frameborder="0", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share", referrerpolicy="strict-origin-when-cross-origin", allowfullscreen=True),
            col_sm=1,
            col_md=2,
        ),
        render_md(md_2),
    )

def Team():
    def _TeamMember(name, role, major, email="", linkedin=None, github=None):
        def get_icon(major):
            major_icons = {
                "Computer Science": "binary",
                "Economics": "percent",
            }
            return major_icons.get(major, "badge")

        return Card(
            DivLAligned(
                DiceBearAvatar(name, h=24, w=24),
                Div(H3(name), P(role), Span(email))),
            footer=DivFullySpaced(
                DivHStacked(UkIcon(get_icon(major), height=16), P(major)),
                DivHStacked(
                    UkIconLink("mail", href=f"mailto:{email}"),
                    UkIconLink("linkedin", height=16, href=linkedin, _target="blank") if linkedin else None,
                    UkIconLink("github", height=16, href=github, _target="blank") if github else None,
                )
            ))
    team = [
        _TeamMember("Alice Heiman", "Stanford Green AI", "Computer Science", "aheiman@stanford.edu", "https://www.linkedin.com/in/alice-heiman/", "https://github.com/aliceheiman"),
        _TeamMember("Jerry Huang", "Green AI Institute", "Computer Science & Economics", "contact@greenai.institute", "", ""),
    ]
    return Section(
        "TEAM",
        "Our Team",
        "var(--gray-color)",
        Grid(*team, cols_sm=1, cols_md=1, cols_lg=2, cols_xl=3),
        CTA("Interested in joining the team?", "Register interest", "https://forms.gle/pBrZJNgp6PeqGN886", cls="mt-4"),
    )

@rt("/about")
def get():
    return Container(
        NavbarSection(),
        AboutUs(),
        Team(),
        FooterSection()
    )

# --------- CONTACT PAGE

def ContactBox():
    md = """For ideas, sponsorship opportunities or general inquiries, contact `aheiman@stanford.edu`."""

    return Section(
        "CONTACT",
        "We would love to hear from you",
        None,
        render_md(md)
    )

@rt("/contact")
def get():
    return Container(
        NavbarSection(),
        ContactBox(),
        Team(),
        FooterSection()
    )

# --------- PROJECTS PAGE

def SeeProjects():
    return Section(
        "OUR PROJECTS",
        "Explore Green-in and Green-by AI Projects",
        None,
        Alert(
            DivLAligned(UkIcon('info'), 
                    P("This page is currently under construction. Please check back soon!")),
                    cls=AlertT.info)
    )

@rt("/projects")
def get():
    return Container(
        NavbarSection(),
        SeeProjects(),
        # FooterSection()
    )

# --------- BLOG PAGE
@rt("/blog/posts/{postname}")
def get(postname: str):
    if postname != "":
        return Redirect(f"/blog/posts/{postname}.html")
    else:
        return Redirect("/blog/posts/index.html")

    # with open(f"public/blog/posts/{postname}/index.html") as f:
    #     post_content = f.read()
    # return Container(
    #     NavbarSection(),
    #     Html(post_content),
    #     FooterSection()
    # )

# --------- RESOURCES PAGE
@rt("/resources")
def get():
    return Redirect(f"/blog/posts/resources.html")


# --------- SERVE THE PAGE
serve()