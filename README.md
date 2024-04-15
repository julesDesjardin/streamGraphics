### Stream Graphics

This python project is composed of 3 programs:
- An interface program
- A cards program
- A time tower program

The goal is to be able to show info (name, PRs, results, previous round...) while streaming a solve, either online or on a screen. The time tower shows the live results of a whole round, mostly for live scoretaken finals (also works for first rounds results).

This is firstly aimed towards Euro 2024, but I hope to be able to quickly publish it so anyone can use it in their comps. I am also making it as configurable as possible to help achieve this.

### Todo-list

[Google Sheets with deadlines](https://docs.google.com/spreadsheets/d/1NyOFqkn8wd3MUwsVURFHJPGzXx22HR3kDGemK3fnU-s/edit?usp=sharing)

- [x] Prototype with a few cubers
- [x] Ability to fetch WCIF from the WCA with a given comp ID
- [x] Automatically update menus to show available rounds and groups for each event
    - [ ] Improve layout when no groups have been assigned in a round or an event yet?
- [x] Generate buttons for cubers in the selected group
- [x] Have configurable thresholds to only show the best cubers in the group
    - Current implementation is based on seeding. For finals, it can be good to put back the seeding at a high value so all finalists are shown.
    - [ ] Have a button for finals/automatically detect finals and remove the seeding condition?
- [x] Add Settings Save/Load button
- [ ] Handle a big number of interesting competitors: scroll? Have a fixed maximum and prompt user to update threshold? Only show the top X, being stricter than the threshold?
- [ ] Handle separate stages
    - [ ] Configurable colors for each stage
    - [ ] One menu line per stage
    - [ ] Display buttons for each stage
- [ ] Support a customizable number of cameras
- [x] Choose what info to display for the selected cuber
- [ ] Fetch said info
    - [x] PRs
    - [ ] Picture
    - [ ] Country flag
    - [x] Previous round ranking and result
- [ ] Get live results from a cuber + BPA, WPA, ranking (potential rankings ?)
- [ ] Generate recap page for a group, showing who is interesting in the group (useful both for camera crew and commentary team)
- [x] Make it work on different computers: Use a Telegram Channel
    - [x] Make the Telegram channel ID and bot tokens a part of Settings instead of hardcoded in a Common/Secrets.py
- [ ] Make a TimeTower
    - [x] Get name, results, and rank them
    - [ ] Get flags
    - [ ] Filter by country/region
    - [ ] Animate ?