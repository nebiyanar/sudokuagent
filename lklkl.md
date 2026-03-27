# 🚛 Hybrid MILP & Matheuristic Optimization Model

This project presents a hybrid framework combining:

* 📐 Time-Based MILP
* 🧠 Spatio-Temporal K-Means Matheuristic

---

## 📐 Mathematical Model (MILP)

### Sets

* **K**: Set of trucks
  $$
  k \in K = {0, \dots, n_{\text{trucks}} - 1}
  $$

* **M**: Set of machines
  $$
  i, j \in M
  $$

* **F**: Failed machines
  $$
  F \subset M
  $$

* **Oₖ**: Mid-day location of truck k

* **D**: Depot

* **Vₖ**: Node set
  $$
  V_k = {O_k} \cup M \cup {D}
  $$

---

### Parameters

* Travel time:
  $$
  dist_{ij}
  $$

* Service duration:
  $$
  sd_i
  $$

* Time window:
  $$
  [tw_{s_i},\ tw_{e_i}]
  $$

* Truck start time:
  $$
  \tau_k
  $$

* Penalties:
  $$
  \lambda_f,\ \lambda_d,\ P_{\text{late}}
  $$

* Big-M:
  $$
  M_{ij}
  $$

---

### Decision Variables

* Routing:
  $$
  x_{kij} \in {0,1}
  $$

* Activation:
  $$
  y_k \in {0,1}
  $$

* Arrival time:
  $$
  T_i \ge 0
  $$

* Slack (heuristic):
  $$
  S_i \ge 0
  $$

* Failure delay:
  $$
  L_i = T_i - failed_at_i
  $$

* MTZ variable:
  $$
  u_i \in \mathbb{R}
  $$

---

### Objective Function

$$
\min Z =
\lambda_f \sum_{i \in F} L_i

* \lambda_d \sum_{i \in M} (demand_rate_i \cdot T_i)
* P_{\text{late}} \sum_{i \in M} S_i
  $$

---

### Constraints

#### 🔹 Flow Conservation

$$
\sum_{k \in K} \sum_{i \in {O_k} \cup M,\ i \ne j} x_{kij} = 1
\quad \forall j \in M
$$

---

#### 🔹 Route Continuity

$$
\sum_{j \in M \cup {D}} x_{k, O_k, j} = y_k
\quad \forall k \in K
$$

$$
\sum_{i \in {O_k} \cup M} x_{kij}
=================================

\sum_{h \in M \cup {D}} x_{kjh}
\quad \forall j \in M,\ \forall k \in K
$$

---

#### 🔹 Time Propagation

$$
T_j \ge T_i + sd_i + dist_{ij}

* M_{ij} \left(1 - \sum_{k \in K} x_{kij}\right)
  $$

---

#### 🔹 Time Windows

**Exact:**
$$
tw_{s_i} \le T_i \le tw_{e_i}
$$

**Heuristic:**
$$
tw_{s_i} \le T_i \le tw_{e_i} + S_i
$$

---

#### 🔹 Subtour Elimination (MTZ)

$$
u_j \ge u_i + 1

* |M| \left(1 - \sum_{k \in K} x_{kij}\right)
  $$

---

## 🧠 Matheuristic (Clustering)

### Feature Space

$$
(X,\ Y,\ T_{\text{midpoint}})
$$

Scaled via **MinMaxScaler**

---

### Overlapping Clusters

* Each machine → **top-2 trucks**
* Benefits:

  * avoids infeasibility
  * improves load balancing

---

### Algorithm

```python
Algorithm: Spatio-Temporal Overlapping Matheuristic

Input: M_set, truck_states

features = Extract(X, Y, TimeWindow_Center)
features_scaled = MinMaxScaler(features)

clusters = KMeans(n_trucks).fit(features_scaled)

for m in M_set:
    assign to nearest 2 trucks

Solve MILP (restricted)
Apply soft time windows
```

---

## ⚙️ Assumptions

* 🕛 Mid-day positions are fixed
* 🚨 Failed machines have priority
* ⏱ Time ensures no subtours
* 🔄 Soft time windows allowed (penalized)

---

## 🚀 Summary

* MILP → optimality
* Matheuristic → scalability
* Clustering → robustness

---
