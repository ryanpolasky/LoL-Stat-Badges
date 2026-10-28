<img src="https://github.com/AnderMendoza/AnderMendoza/raw/main/assets/line-neon.gif" width="100%" alt="Thick Decorative Bar">

# LoL Stat Badges 

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *About The Project*:

Have you ever wished you could display your accomplishments in League of Legends in the same way that you display your 
GitHub tech stack? No? Well too bad! Introducing **LoL Stat Badges**! Display your League of Legends rank on your GitHub 
README files or anywhere else that supports SVG embeds!

![Lol Self](https://api.ryanpolasky.com/lol/badge/NA1/Eggy/NEW)&nbsp;
![LoL Friend](https://api.ryanpolasky.com/lol/badge/NA1/Shua/EGGGY?rank_name=true)&nbsp;
![LoL Faker](https://api.ryanpolasky.com/lol/badge/KR/Hide%20on%20bush/KR1)&nbsp;

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *Tech Stack*: 

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)&nbsp;
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=for-the-badge&logo=cloudflareworkers&logoColor=white)&nbsp;
![Riot Games API](https://img.shields.io/badge/Riot_Games-D32936?style=for-the-badge&logo=riot-games&logoColor=white)&nbsp;

### *Tests*:
![CI](https://github.com/ryanpolasky/LoL-Stat-Badges/actions/workflows/ci.yml/badge.svg)

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *API Usage*: 

To display your degeneracy, follow the steps below:

- Embed the base URL - `https://api.ryanpolasky.com/lol/badge`
- Add your region ([options listed here](https://github.com/ryanpolasky/LoL-Stat-Badges/blob/main/src/regions.ts)) to the path - `https://api.ryanpolasky.com/lol/badge/NA1`
- Add your Riot ID name to the path - `https://api.ryanpolasky.com/lol/badge/NA1/Eggy`
  - If your Riot ID name has spaces, replace them with `%20` in the URL
- Add your Riot ID tag to the path - `https://api.ryanpolasky.com/lol/badge/NA1/Eggy/NEW`
- Embed your shame into your GitHub README - `![LoL Stat Badge](https://api.ryanpolasky.com/lol/badge/NA1/Eggy/NEW)&nbsp;`
  - The `&nbsp;` tag is simply for formatting, so feel free to omit it if desired :)

If you want the badge to show the name of the rank instead of your Riot ID, include `?rank_name=true` at end of your 
embed URL.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *Self-Hosting*:

It's a single Cloudflare Worker. Update the route in `wrangler.jsonc` to your own domain, then:

```sh
npm install
npx wrangler secret put RIOT_API_KEY
npx wrangler deploy
```

`npm test` runs the test suite. `scripts/gen-assets.py` regenerates `src/generated.ts` (rank icons + font widths) if you change anything in `assets/`.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="Thin Decorative Bar">

### *Next Steps*:
- Add additional styles to match the Shields.io styles [listed here](https://shields.io/docs/static-badges)
- Add support for specifying which ranked queue to use
  - Currently only functions with Solo/Duo queue
- ~~Check if Teamfight Tactics (TFT) support can be added & implement it if it can be~~
  - Looks like TFT can be added! 
- Add champion mastery as a style option
- ~~Add support for non-Latin/CJK characters~~
- Maybe create standardized Riot API wrapper package if one doesn't already exist

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
