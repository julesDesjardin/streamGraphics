### Stream Graphics

This python project is composed of 3 programs:
- An interface program
- A cards program
- A time tower program

The goal is to be able to show info (name, PRs, results, previous round...) while streaming a solve, either online or on a screen. The time tower shows the live results of a whole round, mostly for live scoretaken finals (also works for first rounds results).

This project has been successfully used in many WCA competitions. For more information on Setup and using this project, contact me via Github or via my WCA email (format is [first letter of my first name][last name]@worldcubeassociation.org). I am planning to make a video tutorial very soon.

### Previous versions/Release note

v1.0:
- Support 4 Cards in parallel.
- Support animated background for opening a Card, loop it as background, and closing it.
- Support time tower showing names with A. BCD, flag of the competitor and current average/best time.
- Support expanding a single line of the tower (coordinating with the Card) to show full name and all times.
- Support a custom text to be used in presentation mode of Cards.
- Support a custom image instead of the WCA Avatar.

### Future versions

Planned features for v2.0:
- Support retrocompatibility: when loading a JSON from an earlier version, fill it with default values for new features.
- Support local communication instead of Telegram for 1-PC use, and easier development.
- Support any number of Cards, to adapt to all screen sizes/Card sizes.
- Replace the Taiwan flag with the WCA "Chinese Taipei" flag.
- Support both "A. BCD" and Full Name for the TimeTower.
- Support adding BPA and WPA on the TimeTower when reaching solve 4.
- Support new Blind Best Of 5 format.