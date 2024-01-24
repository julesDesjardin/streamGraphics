### Stream Graphics

This python project is composed of 2 programs:
- An interface program
- A display program

The goal is to be able to show info (name, PRs, results, previous round...) while streaming a solve, either online or on a screen. This will also include a program to show the live results of a whole round.

This is firstly aimed towards Euro 2024, but I hope to be able to quickly publish it so anyone can use it in their comps. I am also making it as configurable as possible to help achieve this.

### Todo-list

- [x] Prototype with a few cubers
- [x] Ability to fetch WCIF from the WCA with a given comp ID
- [x] Automatically update menus to show available rounds and groups for each event
    - [ ] Improve layout when no groups have been assigned in a round or an event yet?
- [x] Generate buttons for cubers in the selected group
- [x] Have configurable thresholds to only show the best cubers in the group
    - Current implementation is based on seeding. For finals, it can be good to put back the seeding at a high value so all finalists are shown.
    - [ ] Have a button for finals/automatically detect finals and remove the seeding condition?
- [ ] Handle a big number of interesting competitors: scroll? Have a fixed maximum and prompt user to update threshold? Only show the top X, being stricter than the threshold?
- [ ] Handle separate stages
    - [ ] Configurable colors for each stage
    - [ ] One menu line per stage
    - [ ] Display buttons for each stage
- [ ] Choose what info to display for the selected cuber
- [ ] Fetch said info
    - [ ] PRs
    - [ ] Picture
    - [ ] Country flag
    - [ ] Previous round ranking and result
    - [ ] Live result: current ranking, BPA, WPA
- [ ] Generate recap page for a group, showing who is interesting in the group (useful both for camera crew and commentary team)
- [ ] Generate live results page
- [ ] Make it work on different computers: use a server to share files, or send files directly to clients, or have clients poll data from the server?