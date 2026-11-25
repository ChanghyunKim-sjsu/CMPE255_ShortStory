# Slide outline (13 slides, about 10 min)

Skeleton only: each slide has a one-line message, keyword bullets, a figure to draw, and a time budget.
Write the actual slide text and speaker script yourself. All numbers below are verified against the PDFs (see NOTES.md).

Time budget: 13 slides, about 45 s each = about 10 min. Cut slide 7 or 12 if running long.

---

## 1. Title (15 s)
- Message: what this talk is about.
- Title, your name, CMPE 255, date.
- Main paper: Xue, Tan, Ma, Ukkusuri, arXiv 2501.16656. Supplementary: IGSTGNN, FaST.

## 2. Hook: the ETA in your map app (45 s)
- Message: GNNs already run in a product you use daily.
- Google Maps ETA, GNN deployed 2021.
- Relative reduction of negative ETAs, 16% to 51%, 19 cities.
- Question for the talk: how does a graph model do that, and how do we know it works?
- Figure: screenshot-style mock of a route with ETA (draw your own, do not copy Google's image).

## 3. Problem: data mining in transportation networks (45 s)
- Message: two families of tasks.
- Prediction: speed, flow, demand, accidents.
- Operation: routing, traffic assignment, TSP-like problems.
- Data: sensors, GPS, taxis, bikes, flights (spatio-temporal).
- Figure: simple two-column diagram (Prediction | Operation) with examples.

## 4. Why graphs? (45 s)
- Message: roads are a network, neighbors influence each other.
- Sensors as nodes, edges by proximity or road connection.
- Other graphs: regions as nodes with flows as edges; bike stations.
- A plain table or image model ignores this structure.
- Figure (draw yourself): map -> graph.

## 5. GNN in one minute (60 s)
- Message: each node updates its state from its neighbors.
- Neighborhood aggregation; k layers see k hops. H(l+1) = f(H(l), A, W).
- Four names to know: GCN (fast, spectral simplification), GAT (attention), GraphSAGE (aggregate then concat with self), GIN (expressiveness).
- Figure (draw yourself): message passing on a 5-node graph, one step.

## 6. Standard recipe for traffic prediction (60 s)
- Message: spatial GNN + temporal module.
- Pipeline: sensor data -> GNN (space) -> LSTM / GRU / Transformer (time) -> forecast.
- Survey Table 3: 31 studies from 2023-2024, 16 use GCN.
- Common datasets: PEMS-BAY, METR-LA, PeMSD4, PeMSD8; larger: LargeST, UTD19, U.S. 20.
- Figure (draw yourself): block diagram of the pipeline.

## 7. Beyond forecasting (30 s)
- Message: GNNs also help with decisions, but evidence is thin.
- Operations: GNN gives continuous node scores, then rounding or tree search gives a discrete answer.
- Traffic assignment: link-flow error below 2%, but only on networks with at most hundreds of nodes (Sioux Falls etc.).
- Accidents: spatio-temporal GCNs; zero-inflated crash counts need probabilistic models.
- Figure: one small flow diagram "continuous output -> rounding -> solution".

## 8. Industry vs academia (45 s)
- Message: same models, different setting.
- Table from survey Table 4: Google (Graph Network, Huber, deployed), Amap (H-STGCN, L1, deployment not mentioned), Baidu (ConSTGAT, Huber + APE, deployed).
- Industry nodes = road segments, academia nodes = sensors.
- Industry code and data not released.
- Figure (draw yourself): comparison table, 2 columns (Academia | Industry).

## 9. How is it measured? (45 s)
- Message: metrics tell different stories.
- MAE (average error), RMSE (punishes big errors), MAPE (relative, unstable near zero).
- Horizons: 15 / 30 / 60 min ahead (12 steps of 5 min).
- Industry adds negative ETA: share of errors above a threshold.
- FaST also reports R2 and long horizons up to 672 steps (one week at 15 min).
- Figure: small formula strip plus one example number line showing why RMSE > MAE with an outlier.

## 10. Evidence 1: IGSTGNN, incidents help (60 s)
- Message: adding incident information improves forecasts, but gains are modest and data dependent.
- Idea: ICSF (attention from traffic state to incidents, masked by distance) + TIID (Gaussian decay of incident impact).
- Data: XTraffic, California 2023. Alameda 521 sensors, 14,687 incidents.
- Result: avg MAE 12.69 vs best baseline DSTAGNN 13.45 (-5.65%).
- Ablation (Alameda MAE): full 12.69; w/o ICSF 13.23; w/o TIID 13.23; w/o sensor attrs 13.21; w/o distance 13.20; w/o incident attrs 13.09.
- Careful: on Contra Costa all drops are only 0.7-1.2%. Not a win on every metric (12-step MAPE loses to DSTAGNN on two datasets).
- Figure: `figures/ablation_igstgnn.png` (done). Shows MAE increase vs full model on all three datasets, so the small Contra Costa gains are visible.

## 11. Evidence 2: FaST, scaling to big graphs (60 s)
- Message: attention and MoE can be made cheap enough for 8,600 nodes and week-long horizons.
- Problem: O(N^2) interactions run out of GPU memory (many models fail at 8,600 nodes, 672 steps, 48 GB GPU).
- Parts: temporal compression input, agent attention O(N^2) -> O(Na) (32 agents), heterogeneity-aware MoE (8 GLU experts, router with space/time-of-day/day-of-week biases).
- Memory at 672 steps: SD 3.7 GB vs GWNet 34.5 GB (-89.3%); GLA 17.4 GB vs BigST 28.5 GB (-38.9%).
- Ablation: every component helps (bars only in Fig 4, no numbers). Do not claim HA-MoE is largest everywhere.
- Figure: `figures/memory_fast_672.png` (done). Honest reading: FaST is not the smallest (DLinear, STID use less; on CA BigST is lower), but GWNet and STGCN run out of memory on GBA/GLA/CA while FaST runs. Do not say "lowest memory".

## 12. Open problems and my take (60 s)
- Message: your opinion, with the evidence behind it.
- Survey open problems: probabilistic prediction, simpler models (MLP can beat GNNs using time-of-day, day-of-week, sensor location; GLNN distillation), end-to-end operations, physics-informed GNNs, GNN + LLM, industry data sharing.
- Gaps I noticed: survey Section 4 has no ablation; no timing data for "GCN is efficient"; industry models unreproducible.
- Your question to answer: is the complexity needed? (compare IGSTGNN's small gains with MLP baselines)
- Figure: none needed, or a simple "academia gap" sketch.

## 13. Summary and references (30 s)
- 3 takeaways, each one sentence in your words.
- Reference list with arXiv links (same as README).
- Repo QR code or link.
- Figure: QR code to the GitHub repo.

---

## Figures to prepare (priority order)
1. Map -> graph (slide 4)
2. Message passing (slide 5)
3. Spatial GNN + temporal block diagram (slide 6)
4. IGSTGNN ablation bar chart (slide 10)
5. FaST GPU-memory chart (slide 11)
6. Academia vs industry table (slide 8)
7. Metrics strip (slide 9)

## Format notes
- 16:9, large fonts, 1 message per slide, max about 25 words of text per slide.
- Put sources on the slide footer (author, year, arXiv number).
- Export a PDF into this folder, then upload to SlideShare.
- Use your own drawings. Do not paste figures from the papers without citing them.
