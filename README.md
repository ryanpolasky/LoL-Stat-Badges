<img src="https://github.com/AnderMendoza/AnderMendoza/raw/main/assets/line-neon.gif" width="100%" alt="Thick Decorative Bar">

# LoL Stat Badges 

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *About The Project*:

Have you ever wished you could display your accomplishments in League of Legends in the same way that you display your 
GitHub tech stack? No? Well too bad! Introducing **LoL Stat Badges**! Display your League of Legends rank on your GitHub 
README files or anywhere else that supports SVG embeds!

![LoL Unranked](https://lol-stat-badges.onrender.com/badge/NA1/BadPunOTD/NA1?rank_name=True)&nbsp;
![Lol Self](https://lol-stat-badges.onrender.com/badge/NA1/Eggo/WFLE)&nbsp;
![LoL Friend](https://lol-stat-badges.onrender.com/badge/NA1/Shua/EGGGY?rank_name=true)&nbsp;
![LoL Faker](https://lol-stat-badges.onrender.com/badge/KR/Hide%20on%20bush/KR1)&nbsp;
![LoL Other Friend](https://lol-stat-badges.onrender.com/badge/NA1/Solomon/NA0?rank_name=true)&nbsp;

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *Tech Stack*: 

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)&nbsp;
![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)&nbsp;
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)&nbsp;
![Riot Games API](https://img.shields.io/badge/Riot_Games-D32936?style=for-the-badge&logo=riot-games&logoColor=white)&nbsp;

### *Tests*:
![Linting](https://github.com/ryanpolasky/LoL-Stat-Badges/actions/workflows/pylint.yml/badge.svg)
![Security](https://github.com/ryanpolasky/LoL-Stat-Badges/actions/workflows/security-scan.yml/badge.svg)
![Deployment](https://github.com/ryanpolasky/LoL-Stat-Badges/actions/workflows/deployment-test.yml/badge.svg)

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *API Usage*: 

To display your degeneracy, follow the steps below:

- Embed the base URL - `https://lol-stat-badges.onrender.com/badge`
- Add your region ([options listed here](https://github.com/ryanpolasky/LoL-Stat-Badges/blob/main/app/config.py)) to the path - `https://lol-stat-badges.onrender.com/badge/NA1`
- Add your Riot ID name to the path - `https://lol-stat-badges.onrender.com/badge/NA1/Eggo`
  - If your Riot ID name has spaces, replace them with `%20` in the URL
  - Note: This API currently does not work with 
- Add your Riot ID tag to the path - `https://lol-stat-badges.onrender.com/badge/NA1/Eggo/WFLE`
- Embed your shame into your GitHub README - `![LoL Stat Badge](https://lol-stat-badges.onrender.com/badge/NA1/Eggo/WFLE)&nbsp;`
  - The `&nbsp;` tag is simply for formatting, so feel free to omit it at will

If you want the badge to show the name of the rank instead of your Riot ID, include `?rank_name=true` at end of your 
embed URL.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *Next Steps*:
- Figure out a way to measure the length of a username for dynamic badge sizing
  - Current method is decent, but certain names can lead to shorter/longer than necessary badges
- Add additional styles to match the Shields.io styles [listed here](https://shields.io/docs/static-badges)
- Add caching
  - Might not be necessary as the main use case is GitHub, which already caches for at least a day
- Finalize Python tests
- Add support for specifying which ranked queue to use
  - Currently only functions with Solo/Duo queue
- ~~Check if Teamfight Tactics (TFT) support can be added & implement it if it can be~~
  - Looks like TFT can be added! 
- Add champion mastery as a style option
- ~~Add support for non-Latin/CJK characters~~
- Maybe create standardized Riot API Python wrapper package if one doesn't already exist

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *Issues/Contact*:
If a red badge renders with "ERROR" written on it, double-check your arguments, as one or more argument is invalid.
If there are any issues with the API, or if you need to contact me for any other reason, please use my Email or LinkedIn below! 

<div align="center">
  <a href="mailto:ryanpolasky@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white&color=black"  alt="Gmail"/></a>
  <a href="https://www.linkedin.com/in/ryan-polasky/"><img src="https://img.shields.io/badge/LinkedIn-%2312100E.svg?&style=for-the-badge&logo=linkedin&logoColor=white&color=black"  alt="LinkedIn"/></a>
  <a href="https://www.instagram.com/ryanpolasky"><img src="https://img.shields.io/badge/Instagram-%2312100E.svg?&style=for-the-badge&logo=instagram&logoColor=white&color=black"  alt="Instagram"/></a>
  <a href="https://ryanpolasky.com/"><img src="https://img.shields.io/badge/website-000000?style=for-the-badge&logo=About.me&logoColor=white&color=black"  alt="Personal Website"/></a>
</div>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">
