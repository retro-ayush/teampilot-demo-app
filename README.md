# teampilot-demo-app

A tiny login validator used as the live demo target for
[TeamPilot AI](https://github.com/retro-ayush/swtichhack).

It contains a **deliberately introduced, safe bug**: empty and whitespace
emails pass validation. TeamPilot's AI agents investigate, fix and test it in
the demo, and a human approves the merge.

```bash
python3 -m pytest -q    # 2 failures until the bug is fixed
```
