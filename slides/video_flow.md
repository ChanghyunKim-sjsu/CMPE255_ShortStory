# Video flow (target about 11.5 min; the assignment asks for 10 to 15 min)

Slides: 14 in the pptx (slide 10 = optional metrics example). Talking points are prompts, not a script. Say them in your own words.
Pace: about 130 words per minute. If a slide needs more than the time below, cut words, not slides.

| # | Slide | Time | Cumulative | What to cover (prompts) | Transition to next |
|---|-------|------|------------|-------------------------|--------------------|
| 1 | Title | 0:15 | 0:15 | Who you are, the main paper, what the viewer will know at the end | "Let me start with something you use every day." |
| 2 | Hook: ETA | 0:45 | 1:00 | Google Maps ETA, 16-51% fewer negative ETAs in 19 cities. Why this is a data mining problem | "To see how, we first need to see roads as data." |
| 3 | Two problem families | 0:45 | 1:45 | Prediction vs operation, one example each | "Both start by describing the network as a graph." |
| 4 | Road network = graph | 0:45 | 2:30 | Map to nodes and edges, why neighbors matter | "Now, how does a model use that graph?" |
| 5 | GNN in one minute | 1:00 | 3:30 | Neighbors send messages, node updates, k layers = k hops, 4 names in one phrase each | "How do people actually build a traffic model with it?" |
| 6 | Standard recipe | 1:00 | 4:30 | GNN for space, sequence model for time, 31 studies, 16 use GCN, datasets | "Forecasting is not the only use." |
| 7 | Beyond forecasting | 0:30 | 5:00 | Operations, traffic assignment limit (hundreds of nodes), accidents | "What changes when a company deploys this?" |
| 8 | Industry vs academia | 0:45 | 5:45 | Road segments vs sensors, negative ETA, code and data not released | "How do we judge any of these models?" |
| 9 | Metrics | 0:45 | 6:30 | MAE, RMSE, MAPE, negative ETA, horizons | "A quick example makes this concrete." |
| 10 | Metrics example (optional) | 0:30 | 7:00 | Same MAE, different RMSE; MAPE near zero; say it is made-up | "Now to real evidence from two recent papers." |
| 11 | IGSTGNN | 1:00 | 8:00 | Incidents as extra input, 5.65% lower MAE on Alameda, ablation, small gains on Contra Costa | "That paper adds information. The next one is about scale." |
| 12 | FaST | 1:00 | 9:00 | 8,600 nodes, 672 steps, memory chart, GWNet and STGCN out of memory, not the lowest memory | "So what do I make of all this?" |
| 13 | Open problems and my take | 1:30 | 10:30 | Open problems, your opinion with evidence, gaps you noticed | "Let me wrap up." |
| 14 | Summary | 0:45 | 11:15 | 3 takeaways, references, repo link | End |

Total about 11:15. Cut slide 10 and you land near 10:45, still above the 10 min minimum. Do not go below 10:00.

## Recording checklist
- Record each section in one take or use a screen recorder that lets you trim (QuickTime, Zoom local recording, OBS).
- Show the slides full screen. Camera optional; ask the instructor if it must be visible.
- Speak to the chart: point at the exact bar or number you mention.
- Do one test of 30 seconds to check audio level.
- Say the sources out loud once (for example "Xue et al., 2025").
- Keep numbers exactly as on the slides (see NOTES.md for the verified list).

## Upload
- GitHub blocks files over 100 MB. A 10-15 min 1080p video is usually bigger.
- Option A: upload to YouTube (unlisted) and put the link in README. Confirm with the instructor that this is allowed.
- Option B: compress to under 100 MB (720p, H.264) and put it in `video/`.
- Option C: Git LFS in the repo.
- Add the link or file path to the README table, then check the link while logged out.
