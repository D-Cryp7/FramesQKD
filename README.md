# FramesQKD

_by Daniel Espinoza (D-Cryp7)_

This repository contains the proofs of concepts of the Pairs-reuse, Conjugate-Pais reuse and Avalanche-Effect attacks on LL20, LLS21, LL21 and L23 frame-based reconciliation QKD protocols.

## Requirements
* Qiskit (for QKD execution)
* pandas (for dataframe results)

## Considerations
* We assume that the classical channel is authenticated.
* Each protocol is implemented up to the sifting stage, because the reconciliation stage is a black box for the attacker's perspective.
* The secret key is equivalent to the Measurement Results (MR).

## Content

* `qkd.py`: Generic function of the QKD protocol execution.
* `metrics.py`: Generic function for the metrics calculation. In this script, the QKD protocol is executed, as well as the specific attack, returning the double matchings, bits recovered, total bits, fraction of recovered bits and SS (CSS) left (not recovered).
* `latex_tables.ipynb`: Tables generation for Pairs-reuse attack on LLS21.

Each folder contains the following files:
* `alice.py`: Alice behaviour. The quantum states preparation, computation of usable frames and secret key derivation is made. For L23, the usable frames are not defined.
* `bob.py`. Bob behaviour. The quantum states measure, computation of SS (CSS) and secret key derivation is made. For L23, Bob computes the lists of frames $L_1$ and $L_2$.
* `helpers.py`: LUTs for usable frames computation and secret key derivation.
* `partial_key_recovery.py` / `key_recovery.py`: Implemented attacks.
* `run.ipynb`: Jupyter Notebook for QKD protocol execution, attack execution and metrics calculation.
* `more_results`: Folder with additional results, without time execution.
* `results_with_time.csv`: Results with time execution.
* `figures`: Folder with graphs of fraction of bits recovered and time execution with respect of the double matchings.


