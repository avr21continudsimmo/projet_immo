"""

Config file for Streamlit App

"""

from member import Member


TITLE = "pyPredImmo"

TEAM_MEMBERS = [
    Member(
        name = "Yvan Aubrée",
        linkedin_url = 'https://www.linkedin.com/in/yvan-aubree-700b84a0/',
        github_url = 'https://github.com/Yaub44'
    ),
    Member(
        name = "Ameth Ba El Hadji"
    ),
    Member(
        name = "Lionel Fèvre",
        linkedin_url = "https://www.linkedin.com/in/lionel-fevre-03978284/",
        github_url = "https://github.com/linol"
    ),
    Member(
        name = "Benjamin Leblanc",
        linkedin_url = "https://www.linkedin.com/in/benjamin-leblanc-data/",
        github_url = "https://github.com/leblanc-benjamin"
    ),
    Member(
        name = "Charles de Valois",
        linkedin_url = "https://www.linkedin.com/in/charleshenridevalois/",
        github_url = "https://github.com/chvalois"
    )
]

PROMOTION = "Promotion Bootcamp Data Scientist - April 2021"
